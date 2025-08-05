## Lab 2

### 1-Working with Python in OpenROAD

OpenROAD 的核心是数据库——这也是任何 EDA（电子设计自动化）工具的核心。它在内存和磁盘中以统一的对象模型存储设计数据和工艺数据。通过让每个 OpenROAD 组件都可以访问这个带有回调机制的通用模型（正如课堂讲授中所看到的那样），该工具在保持模块化的同时，也支持紧密的、迭代式的优化流程。

传统上，EDA 工具在数据模型中并不重视用户的交互体验。访问或修改设计数据通常需要通过以下三种方式之一，这些方式都不太方便

- **图形界面操作（GUI interaction）**：速度慢、依赖手工、容易出错。
- **Tcl 脚本语言（Tcl scripting）**：这是一种小众语言，库资源有限，语法不直观。
- **文件导入导出（File export/import）**：需要将数据写出为开放格式再读入，这种“绕一圈”的方式开销大，依赖复杂的标准，还容易丢失信息（比如详细的时序注释）。

这些方式都会降低效率，使得高级自定义变得困难。而 OpenROAD 在这一现状基础上做出了两大改进：

- 作为开源项目，OpenROAD 提供了完整的 OpenDB 源代码，工程师可以根据需要访问全部的数据结构或自定义组件，而类定义本身也起到了“自文档化”的作用。像全局布局器（global placer）这样的主要模块也可以直接修改，使得定制变得更为容易。
- OpenROAD 原生支持 Python。这意味着工程师可以利用整个 Python 生态系统（如 NumPy、pandas、PyTorch 等），直接查询和操作 OpenDB 中的对象，同时也能配合传统的 Tcl 命令。这使得物理设计脚本变得更加灵活和强大，也促进了机器学习驱动的设计流程：例如 NVIDIA 的 CircuitOps 工具就使用 Python API 将电路结构和指标直接从 OpenDB 流式传输到机器学习框架中，省去了慢速的文件中转和复杂的格式转换代码。

**当前版本的 OpenROAD 不支持 GUI 与 Python 同时运行**，所以需要先运行 Python 脚本生成结果，然后再视情况使用 GUI 打开这些结果进行查看。

#### Anatomy of a Script

**OpenROAD Python 脚本结构与数据库管理模型**

- **标准脚本结构**
   OpenROAD Python 脚本通常先导入 Tech、Design 对象和 OpenDB 的 Python 绑定 `odb`。这些模块访问的是 OpenROAD 启动时使用的同一个全局数据库实例。
- **数据库所有权**
   数据库由 OpenROAD 主控，脚本只是持有数据库中已有对象的引用。脚本本身不拥有数据库。
- **缺点**
  - **对象持久性**：函数返回后，加载的设计对象依然存在于数据库中。重复加载同一设计时会因名称冲突导致错误，需先删除旧对象。
  - **悬空引用风险**：数据库中删除对象后，若 Python 中仍有引用，访问该引用可能导致程序崩溃（如段错误）。
- **使用建议**
  - 只加载必要对象，及时删除不再使用的对象。
  - 避免保留无效引用，防止程序异常。
  - 对 Python API 的使用应保持与 Tcl/C++相同的谨慎态度。

| 函数                          | 用途说明                                                     |
| ----------------------------- | ------------------------------------------------------------ |
| getReplace, getTritonroute, … | 这些 getter 函数对应 OpenROAD 应用中的各个组件。获取到这些对象后，可以控制对应的组件。例如，`design.getGlobalRouter().globalRoute()` 会执行全局布线。 |
| getDb                         | 返回 `dbDatabase` 对象——OpenROAD 的主 OpenDB 实例。虽然下面的 `getBlock` 方法更方便获取设计数据库，但当需要低层访问（如 LEF/DEF 或 Liberty 技术库数据）时使用此函数。 |
| getBlock                      | 返回数据库中的主 `dbBlock`（即顶层设计），可以访问其实例等。等价于 `design.getDb().getChip().getBlock()`，但写法更简洁。注意一个数据库可以包含多个芯片以支持多芯片设计。 |
| evalTclString                 | 执行任意 Tcl 命令字符串并返回结果。用于 Python 绑定中缺少对应功能时调用。例如，`design.getReplace()` 没有对应全局布局 Tcl 命令的功能。 |
| createDetachedDb              | 创建一个独立的 `dbDatabase`，不连接到全局 OpenROAD 数据库，允许并行加载和操作多个设计。（实验性质，使用需谨慎。） |
| readDb, readDef, readVerilog  | 读取数据库、DEF 文件或 Verilog 文件的命令。                  |
| writeDb, writeDef             | 写出数据库快照或 DEF 文件的命令。                            |

```bash
# section1/
openroad -python template.py
# block. ?
```

```python
block.addBlockedRegionForPins(     block.getBTermGroups()             block.getModules()
block.addBTermGroup(               block.getBTerms()                  block.getName()
block.addGlobalConnect(            block.getBusDelimeters(            block.getNets()
block.adjustCC(                    block.getCapNodes()                block.getNonDefaultRules()
block.adjustRC(                    block.getCcHaloNets(               block.getObstructions()
block.clear()                      block.getCCSegs()                  block.getParent()
block.clearGlobalConnect()         block.getChildren()                block.getParentInst()
block.clearUserInstFlags()         block.getChip()                    block.getPowerDomains()
block.copyExtDb(                   block.getComponentMaskShift()      block.getPowerSwitches()
block.create(                      block.getConstName()               block.getRegions()
block.createExtCornerBlock(        block.getCoreArea()                block.getRows()
block.dbuAreaToMicrons(            block.getCornerCount()             block.getRSegs()
block.dbuToMicrons(                block.getCornerNameList()          block.getSearchDb()
block.debugPrintContent(           block.getCornersPerBlock()         block.getTech()
block.designIsRouted(              block.getDataBase()                block.getTopModule()
block.destroy(                     block.getDbUnitsPerMicron()        block.getTrackGrids()
block.destroyCCs(                  block.getDefUnits()                block.getVias()
block.destroyCNs(                  block.getDft()                     block.getWireUpdatedNets(
block.destroyCornerParasitics(     block.getDieArea()                 block.globalConnect(
block.destroyParasitics(           block.getExtControl()              block.groundCC(
block.destroyRSegs(                block.getExtCornerBlock(           block.initParasiticsValueTables()
block.extCornersAreIndependent()   block.getExtCornerIndex(           block.micronsAreaToDbu(
block.findBTerm(                   block.getExtCornerName(            block.micronsToDbu(
block.findChild(                   block.getExtCornerNames(           block.preExttreeMergeRC(
block.findExtCornerBlock(          block.getExtCount(                 block.reportGlobalConnect()
block.findGroup(                   block.getExtDbCount()              block.setBusDelimeters(
block.findInst(                    block.getExtmi()                   block.setComponentMaskShift(
block.findIsolation(               block.getFills()                   block.setCornerCount(
block.findITerm(                   block.getGCellGrid()               block.setCornerNameList(
block.findLevelShifter(            block.getGlobalConnects()          block.setCornersPerBlock(
block.findLogicPort(               block.getGroups()                  block.setDefUnits(
block.findMarkerCategory(          block.getHierarchyDelimeter()      block.setDieArea(
block.findModInst(                 block.getInsts()                   block.setDrivingItermsforNets()
block.findModule(                  block.getIsolations()              block.setExtmi(
block.findNet(                     block.getITerms()                  block.setMaxLayerForClock(
block.findNonDefaultRule(          block.getLevelShifters()           block.setMaxRoutingLayer(
block.findPowerDomain(             block.getLogicPorts()              block.setMinLayerForClock(
block.findPowerSwitch(             block.getMarkerCategories()        block.setMinRoutingLayer(
block.findRegion(                  block.getMasters(                  block.this
block.findTrackGrid(               block.getMaxLayerForClock()        block.thisown
block.findVia(                     block.getMaxRoutingLayer()         block.undoAdjustedCC(
block.getAccessPoints()            block.getMinLayerForClock()        block.writeDb(
block.getBBox()                    block.getMinRoutingLayer()         block.writeGuides(
block.getBlock(                    block.getModBTerms()               block.writeMarkerCategories(
block.getBlockages()               block.getModInsts()                
block.getBlockedRegionsForPins()   block.getModNets()                 
```

```python
insts = block.getInsts()
dir(insts[0])
exit()
```

```python
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__swig_destroy__', '__weakref__', 'bindBlock', 'clearUserFlag1', 'clearUserFlag2', 'clearUserFlag3', 'create', 'destroy', 'findITerm', 'getBBox', 'getBlock', 'getChild', 'getChildren', 'getConnectivity', 'getConstName', 'getEcoCreate', 'getEcoDestroy', 'getEcoModify', 'getFirstOutput', 'getGroup', 'getHalo', 'getHierTransform', 'getITerm', 'getITerms', 'getInst', 'getLocation', 'getMaster', 'getModule', 'getName', 'getOrient', 'getOrigin', 'getParent', 'getPinAccessIdx', 'getPlacementStatus', 'getRegion', 'getSourceType', 'getTransform', 'getUserFlag1', 'getUserFlag2', 'getUserFlag3', 'getValidInst', 'getWeight', 'isBlock', 'isCore', 'isDoNotTouch', 'isEndCap', 'isFixed', 'isHierarchical', 'isNamed', 'isPad', 'isPhysicalOnly', 'isPlaced', 'rename', 'resetHierarchy', 'setDoNotTouch', 'setEcoCreate', 'setEcoDestroy', 'setEcoModify', 'setLocation', 'setLocationOrient', 'setOrient', 'setOrigin', 'setPinAccessIdx', 'setPlacementStatus', 'setSourceType', 'setTransform', 'setUserFlag1', 'setUserFlag2', 'setUserFlag3', 'setWeight', 'swapMaster', 'this', 'thisown', 'unbindBlock']
```

#### Writing your First Script – Cell Area

```bash
cp template.py area.py
```

`master` 指的是这些单元所属的标准单元模板，在 PDK 中定义。

```python
>>> dir(masters[0])
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__swig_destroy__', '__weakref__', 'create', 'destroy', 'findMTerm', 'getArea', 'getConstName', 'getEEQ', 'getEdgeTypes', 'getHeight', 'getLEQ', 'getLib', 'getMTermCount', 'getMTerms', 'getMaster', 'getMasterId', 'getName', 'getObstructions', 'getOrigin', 'getPlacementBoundary', 'getPolygonObstructions', 'getSite', 'getSymmetryR90', 'getSymmetryX', 'getSymmetryY', 'getType', 'getWidth', 'isBlock', 'isCore', 'isCoreAutoPlaceable', 'isCover', 'isEndCap', 'isFiller', 'isFrozen', 'isMarked', 'isPad', 'isSequential', 'isSpecialPower', 'setEEQ', 'setFrozen', 'setHeight', 'setLEQ', 'setMark', 'setOrigin', 'setSequential', 'setSite', 'setSpecialPower', 'setSymmetryR90', 'setSymmetryX', 'setSymmetryY', 'setType', 'setWidth', 'staCell', 'staSetCell', 'this', 'thisown', 'transform']
```

- `master.getArea()`：返回该标准单元的面积，单位是 `DBU²`（数据库单位的平方）。
- 如果要换算为 μm²，可使用数据库单位换算函数，如 `block.dbuToMicrons()`：

```python
dbu_per_micron = block.getDbUnitsPerMicron()
areas_in_microns = [area / (dbu * dbu) for area in areas]
```

```bash
openroad -python -exit area.py
```

### 2-Mutating the Database

#### Swapping Masters

**背景说明**：

在实际的 IC 设计流程中，**替换元件（master）**操作通常发生在 **resizing（单元尺寸调整）阶段**，即在全局布局（global placement）完成之后，为了满足驱动能力（drive strength）等要求，工具会插入 buffer，并对 cell 进行放大或缩小处理。

本练习将 **不加区分地把所有 `sg13g2_dfrbp_1` 类型的实例都替换为 `sg13g2_dfrbp_2`**，后者是一个更强驱动、更大面积的正沿触发 D 触发器（DFF）。

```bash
# section2/
cp template.py swaps.py
# finish swaps.py
openroad -python -exit swaps.py
openroad -gui
```

```tcl
read_db swaps.odb
# 出现重合现象（overlapping）
```

**这种重叠问题也是正常流程中的 resizer 会遇到的问题 —— 这里需要注意的是，你对数据库（DB）所做的更改**不一定在物理上或逻辑上是合法的**。数据库本身没有对布局/布线合法性的概念，因此也不会强制进行合法性检查。**

具体你在做哪种类型的数据库操作，就需要采取不同的补救措施。对于像这种仅对已放置单元做的小修改，我们通常希望运行合法化工具（OpenROAD 中的详细布局器，即 DPL）。

```bash
# design.evalTclString("detailed_placement")
openroad -python -exit swaps.py
openroad -gui
read_db swaps.odb
```

#### Moving & Locking Placements

```bash
# section2/
cp template.py move.py
openroad -python -exit move.py
openroad -gui
read_db move.odb
```

我们已经对 DFF 做了特定的放置，但设计的其他部分与它不再协调一致 —— 我们希望重新对其余部分进行布局。详细布局依赖于全局布局提供的良好初始估计，因此重新运行 GPL（全局布局）是很重要的。

### 3-Writing Custom Placers

#### Why we Script our own Placers

OpenROAD 提供了两种主要的布局工具：

- **RePlAce (gpl)**：用于扁平化布局，统一处理标准单元和宏单元；
- **Hier-RTLMP (mpl)**：用于分层布局，能更智能地布局宏单元。

但在实际高性能或高密度芯片设计中，这些自动布局工具常常不足，原因包括：

- 需要管理复杂的设计层次结构；
- 需要优化**结构化数据通路（SDP）**，即将相关的标准单元或小型宏紧密排列以提升数据流效率。

为此，设计者通常会使用：

- **自定义 SDP 脚本**：以控制布局参数（如纵横比、规律性）来优化数据通路区域；
- **专用的存储器编译器**：处理 SRAM、ReRAM、eFuse、Flash 等模块的布局，直接输出 LEF 文件，绕过通用 EDA 数据库。

总的来说：**自动布局虽方便，但在关键区域仍需手动或半自动优化，以达成更高的设计目标。**

#### My Task

为一个 **128×1 位的内容可寻址存储器（CAM）IP** 构建一个简单的布局器。

这种内存使用 D 触发器（DFF）连接到 XNOR 门，因此内存不会直接输出数据位，而是输出“匹配位”。虽然这个例子非常简化，但足以展示结构化数据通路（SDP）是如何被布局的。

目标包括：

1. **将所有 DFF 按列排列在一起**；
2. **将所有 XNOR 门也按列排列在一起**，并且在 DFF 的右侧；
3. 使用你在第 II 部分学到的内容，**对这些放置进行合法化（legalization）**；
4. 然后对**其余所有单元执行一次完整的布局**（包括全局布局 global placement）；
5. 最后，执行一次**基本的布线（routing）**。

**主要要求：**

- 所有元件的放置必须都**在核心区域（core area）之内**；
- 这样可以保证之后的详细布局（detailed placement）不会移动单元太远，从而**避免你手动安排的布局被破坏**。

#### RTFSC

```systemverilog
module section3(
    input clk,
    input data,
    input [6:0] addr,
    input write,
    output reg match
);

//reg [6:0] mem; 
wire mem [128];
wire cmp [128];



genvar i;
for (i = 0; i < 128; i = i + 1)
begin : cam

    sg13g2_dfrbp_1 mem_cell (
        .Q(mem[i]),
        .D(write ? data : mem[i]),
        .CLK(clk)
    );

    sg13g2_xnor2_1 comparator (
        .A(mem[i]),
        .B(data),
        .Y(cmp[i])
    );
    //assign cmp[i] = ~(mem[i] ^ data);
end

always @(posedge clk) 
        match <= cmp[addr];

endmodule
```

```tcl
read_db section3.odb
```

- 使用预定义变量 `origin_x` 和 `origin_y` 作为 `cam[0]` 中 D 触发器的初始位置基准 —— 参考下方的示意图。
- 已提供实用函数 `decode_cam_index(name)`，用于在脚本中处理 CAM 实例的命名。
- 使用提供的变量 `cam_vertical_offset` 来根据 cam 索引设置正确的垂直偏移。
- 你的放置必须是紧凑的 —— 每个 XNOR 门应紧贴其左侧的 DFF 放置 —— 参考示意图。
- 在第一次 legalize（合法化）之后，记得只锁定这些 cam 实例，然后再进行下一轮 global/detailed placement（全局/详细放置）以及 global/detailed routing（全局/详细布线）。

#### PLACER

一、**什么是站点**（Site）

在芯片布局（floorplan）中，布局区域会被划分成规则的 **栅格（grid）**。这个 grid 的最小单位就叫 **站点（site）**。

每一个标准单元（例如 INV、DFF、XNOR）都必须对齐在这些 site 上进行放置（placement）。站点定义了：

- **标准单元的放置粒度**；
- **标准单元必须对齐的规则位置**；
- 通常情况下，**站点的高度 = 标准单元的高度**（或整数倍）；
- 站点的宽度则是标准单元宽度的一个单位。

二、**站点宽度 vs 标准单元实际宽度**

| 概念          | 含义                                   | 举例说明                    |
| ------------- | -------------------------------------- | --------------------------- |
| `site width`  | 一个放置单位的宽度，比如 1 unit（DBU） | 通常是布局最小宽度粒度      |
| `cell width`  | 单元的实际宽度                         | 可能是 1、2、4 个 site 宽度 |
| `site height` | 单个 site 的高度                       | 通常等于标准单元高度        |
| `cell height` | 单元的实际高度                         | 通常是 1 个 site 高度       |

> **标准单元宽度通常是站点宽度的整数倍**，但不等于站点宽度。

三、**为什么“高度用站点就对了”**？

因为标准单元的布局在高度方向上通常是统一的 —— 所有 cell 的高度 **正好等于一个 site 的高度**（或整数倍），这使得：

```python
cam_vertical_offset = site.getHeight()
```