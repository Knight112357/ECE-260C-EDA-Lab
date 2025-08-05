

# Importing the OpenROAD library - which is only available when running openroad -python
from openroad import Design, Tech
from odb import *
from pathlib import Path


# If we had a separate .lef, we could run tech.readLef but we're using a db here that comes packaged with the library.
tech = Tech()
# We do still need to load the Liberty because OpenDB doesn't store enough information for OpenSTA to run correctly.
tech.readLiberty("../sg13g2_stdcell_typ_1p20V_25C.lib")

design = Design(tech) # Every Design has to be associated with a Tech, even if it's empty.

design.readDb("section3.odb")
library = design.getDb().getLibs()[0] # This gets the only loaded library - the IHP130 PDK
dbu_per_micron = library.getDbUnitsPerMicron()
cam_vertical_offset = library.getSites()[0].getHeight()
block = design.getBlock()

origin_x = 120000
origin_y = 60000
def decode_cam_index(name):
    return int(name.removeprefix("cam\\[").split("\\")[0])

# TODO: When you're writing scripts, write your code below this line:
insts = block.getInsts()
cam_insts = [i for i in insts if i.getName().startswith("cam")] # Get 

dff_insts = [i for i in cam_insts if i.getMaster().getName() == "sg13g2_dfrbp_1"]
xnor_insts = [i for i in cam_insts if i.getMaster().getName() == "sg13g2_xnor2_1"]

dff_insts.sort(key=lambda i: decode_cam_index(i.getName()))
xnor_insts.sort(key=lambda i: decode_cam_index(i.getName()))

DFF_master = dff_insts[0].getMaster()
DFF_width = DFF_master.getWidth()

for i, inst in enumerate(dff_insts):
    x = origin_x
    y = origin_y + i * cam_vertical_offset
    inst.setLocation(x, y)

for i, inst in enumerate(xnor_insts):
    x = origin_x + DFF_width
    y = origin_y + i * cam_vertical_offset
    inst.setLocation(x, y)

design.evalTclString("detailed_placement")

for inst in cam_insts:
    inst.setPlacementStatus("LOCKED")

design.evalTclString("global_placement; detailed_placement")
design.evalTclString("global_routing; detailed_routing")


# Write the DB back out to a file.
# If you make no changes, then the DBs should be no different.
design.writeDb(f"{Path(__file__).stem}.odb")

# By default, OpenROAD will drop into an interactive Python REPL after your script finishes.
# This makes it possible to explore the Python API using Tab completion or the dir() function.
# You can use the exit command to drop out of this REPL once you're done with it. 
# If you do not want it to appear at all, then use openroad -python -exit my_script.py