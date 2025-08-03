## Lab 1

### Setup

```bash
# /work
git clone https://github.com/UDXS/ece260c-lab2-starter.git ece260c-lab2-ShijieSun
```

### 1-Synthesis & Technology Mapping

#### Starting with Yosys

```bash
cd ece260c-lab2-ShijieSun
yosys
read_verilog section1/gcd.v
ls
```

| 命令                        | 说明                                                         |
| --------------------------- | ------------------------------------------------------------ |
| `cd ..` `cd <module>`       | 进入某个模块内部，或返回上一层（类似 `select` 的便捷方式）   |
| `ls` `ls <module>`          | 在模块外列出所有模块；在模块内列出其实例和端口               |
| `select *` `select <query>` | 选择全部逻辑，或通过名称/条件选择部分逻辑（例如选择某个逻辑锥） |
| `show <module>`             | 图形化显示模块电路图，会弹出新窗口展示电路结构               |
| `stat <module>`             | 显示模块中使用的单元（如与非门、触发器等）的数量统计         |
| `dump <module>`             | 以 Yosys 的中间表示语言 RTLIL 形式导出模块内容               |

```systemverilog
//-----------------------------------------------------------------------------
// Mux0
//-----------------------------------------------------------------------------
// dtype: 16
// nports: 3
// dump-vcd: False
// verilator-xinit: zeros
module Mux0
(
  input  wire [   0:0] clk,
  input  wire [  15:0] in_$000,
  input  wire [  15:0] in_$001,
  input  wire [  15:0] in_$002,
  output reg  [  15:0] out,
  input  wire [   0:0] reset,
  input  wire [   1:0] sel
);

  // localparam declarations
  localparam nports = 3;


  // array declarations
  wire   [  15:0] in_[0:2];
  assign in_[  0] = in_$000;
  assign in_[  1] = in_$001;
  assign in_[  2] = in_$002;

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def comb_logic():
  //       assert s.sel < nports
  //       s.out.v = s.in_[ s.sel ]

  // logic for comb_logic()
  always @ (*) begin
    out = in_[sel];
  end


endmodule // Mux0

```

**Processes**

在 Verilog 中，**process（进程）** 是指根据某些事件（显式或隐式定义）触发执行的过程化代码块。你应当了解以下几类：

- `always @*` / `always_comb` / `always_latch` 代码块：这些代码块会在块中依赖的任意信号发生变化时执行。
  - `always_comb` 和 `always_latch` 是 SystemVerilog 的特性，用来避免 `always @*` 的不确定性，它们有助于明确设计意图，例如该代码块是用于组合逻辑还是用于推断锁存器。
- `always @(posedge clk)` 或 `always @(negedge clk)` 代码块：在信号边沿触发时执行，通常用于时钟或输入输出信号。这类代码块用于描述时序逻辑。
- `initial` 代码块：在仿真开始时只执行一次。虽然它们主要用于测试平台（testbench）和仿真中的初始化，但在某些 FPGA 平台中，`initial` 也可能被解释为在复位时触发的操作。

使用进程模型的好处在于：它与事件驱动的仿真器架构天然契合，同时也可以被综合为纯组合逻辑，或者是由触发器（flip-flop）或锁存器（latch）实现的时序逻辑。

在查看 `Mux0` 模块的电路图时，你可能会注意到一个问题：进程的行为并不容易从图中看出。这是因为进程在图中是“不可透明”的（opaque），它们不会被分解为具体的逻辑门或控制流。

在 Yosys 对设计进行转换时，它会添加一些在 Verilog 中不容易显式表达的结构，例如显式的锁存器。因此，如果你想导出或查看 Yosys 的完整数据库，其结果通常会以 **RTLIL**（寄存器传输级中间语言）的形式呈现。RTLIL 是 Yosys 合成过程中的一种中间表示语言，它通过将行为和结构描述翻译成一组“扁平化”的逻辑原语、导线（wires）和单元（cells），提供了一个低层次、便于实现的设计视图。这种格式非常有助于理解 Verilog 中的高级行为是如何映射为可综合逻辑的。

```tcl
dump Mux0
```

```systemverilog
autoidx 36

attribute \cells_not_processed 1
attribute \src "section1/gcd.v:649.1-683.10"
module \Mux0

  attribute \src "section1/gcd.v:0.0-0.0"
  wire width 16 $0\in_[2][15:0]

  attribute \src "section1/gcd.v:0.0-0.0"
  wire width 16 $0\in_[1][15:0]

  attribute \src "section1/gcd.v:0.0-0.0"
  wire width 16 $0\in_[0][15:0]

  attribute \src "section1/gcd.v:678.3-680.6"
  wire width 16 $1$mem2reg_rd$\in_$section1/gcd.v:679$22_DATA[15:0]$26

  attribute \src "section1/gcd.v:678.3-680.6"
  wire width 16 $0$mem2reg_rd$\in_$section1/gcd.v:679$22_DATA[15:0]$25

  attribute \src "section1/gcd.v:678.3-680.6"
  wire width 2 $0$mem2reg_rd$\in_$section1/gcd.v:679$22_ADDR[1:0]$24

  attribute \src "section1/gcd.v:678.3-680.6"
  wire width 16 $0\out[15:0]

  attribute \nosync 1
  attribute \src "section1/gcd.v:0.0-0.0"
  wire width 16 $mem2reg_rd$\in_$section1/gcd.v:679$22_DATA

  attribute \nosync 1
  attribute \src "section1/gcd.v:0.0-0.0"
  wire width 2 $mem2reg_rd$\in_$section1/gcd.v:679$22_ADDR

  attribute \src "section1/gcd.v:665.19-665.22"
  wire width 16 \in_[2]

  attribute \src "section1/gcd.v:665.19-665.22"
  wire width 16 \in_[1]

  attribute \src "section1/gcd.v:665.19-665.22"
  wire width 16 \in_[0]

  attribute \src "section1/gcd.v:657.24-657.27"
  wire width 2 input 7 \sel

  attribute \src "section1/gcd.v:656.24-656.29"
  wire input 6 \reset

  attribute \src "section1/gcd.v:655.24-655.27"
  wire width 16 output 5 \out

  attribute \src "section1/gcd.v:654.24-654.31"
  wire width 16 input 4 \in_$002

  attribute \src "section1/gcd.v:653.24-653.31"
  wire width 16 input 3 \in_$001

  attribute \src "section1/gcd.v:652.24-652.31"
  wire width 16 input 2 \in_$000

  attribute \src "section1/gcd.v:651.24-651.27"
  wire input 1 \clk

  attribute \src "section1/gcd.v:0.0-0.0"
  process $proc$section1/gcd.v:0$27
    assign { } { }
    assign { } { }
    assign { } { }
    assign $0\in_[0][15:0] \in_$000
    assign $0\in_[1][15:0] \in_$001
    assign $0\in_[2][15:0] \in_$002
    sync always
      update \in_[0] $0\in_[0][15:0]
      update \in_[1] $0\in_[1][15:0]
      update \in_[2] $0\in_[2][15:0]
  end

  attribute \src "section1/gcd.v:678.3-680.6"
  process $proc$section1/gcd.v:678$23
    assign { } { }
    assign { } { }
    assign { } { }
    assign $0$mem2reg_rd$\in_$section1/gcd.v:679$22_ADDR[1:0]$24 \sel
    assign $0$mem2reg_rd$\in_$section1/gcd.v:679$22_DATA[15:0]$25 $1$mem2reg_rd$\in_$section1/gcd.v:679$22_DATA[15:0]$26
    assign $0\out[15:0] $1$mem2reg_rd$\in_$section1/gcd.v:679$22_DATA[15:0]$26
    attribute \src "section1/gcd.v:0.0-0.0"
    switch \sel
      attribute \src "section1/gcd.v:0.0-0.0"
      case 2'00
        assign { } { }
        assign $1$mem2reg_rd$\in_$section1/gcd.v:679$22_DATA[15:0]$26 \in_[0]
      attribute \src "section1/gcd.v:0.0-0.0"
      case 2'01
        assign { } { }
        assign $1$mem2reg_rd$\in_$section1/gcd.v:679$22_DATA[15:0]$26 \in_[1]
      attribute \src "section1/gcd.v:0.0-0.0"
      case 2'10
        assign { } { }
        assign $1$mem2reg_rd$\in_$section1/gcd.v:679$22_DATA[15:0]$26 \in_[2]
      attribute \src "section1/gcd.v:0.0-0.0"
      case 
        assign { } { }
        assign $1$mem2reg_rd$\in_$section1/gcd.v:679$22_DATA[15:0]$26 16'x
    end
    sync always
      update \out $0\out[15:0]
      update $mem2reg_rd$\in_$section1/gcd.v:679$22_ADDR 2'x
      update $mem2reg_rd$\in_$section1/gcd.v:679$22_DATA 16'x
  end
end
```

```tcl
proc        # 将设计中的所有进程转换为电路表示
show Mux0
show RegEn  # 查看时序逻辑
```

#### The Synthesis Flow

综合的第一步是告诉 Yosys 设计的层次结构 —— 即模块之间的调用关系。顶层模块（top module）是该层次结构的根节点；它不会被其他模块实例化，通常代表要综合的顶级功能块或芯片。

运行以下命令，将顶层模块设为 `gcd`：

```tcl
hierarchy -top gcd
```

通常在综合前，我们会使用 `flatten` 命令将 netlist 扁平化，以便跨模块执行优化，因为默认的优化操作是保守的，不会跨越模块边界。但为了避免原理图变得过于复杂，我们暂时先不进行扁平化。

我们将通过以下命令执行多模块的综合并进行优化：

```tcl
opt
synth
stat
show Mux0
```

- `opt`：**优化设计逻辑。**

  它执行一系列基础的优化步骤，例如：移除未连接的逻辑（dead code elimination）；合并等价逻辑门（gate merging）；消除恒定信号驱动的电路（constant propagation）移除冗余的赋值、wire 等

  **注意：** 默认不会跨模块优化（除非先 `flatten`）

- `synth`：**执行综合，把 RTL 转换为门级逻辑（gate-level netlist）。**

  这个命令相当于一个“主综合指令”，会自动调用多个 pass（如 proc、opt、techmap 等），将 Verilog 的行为级和结构级代码映射为底层电路结构。

  通常包括：进程展开（`proc`）；条件赋值转换为 mux（`proc_mux`）；状态逻辑转换为触发器（`proc_dff`）；技术映射（`techmap`）：将逻辑转换为目标工艺库支持的元件（如 AND2、DFF、MUX）。

- `stat`：**打印当前设计的统计信息。**

  包括：当前设计中模块的数量；每个模块中 cell 的类型和个数（如 `$and`, `$dff`, `$mux`）；wire 数量、过程块数量、端口信息等。

  这个命令方便你快速查看综合后电路的组成，有助于评估综合质量（QoR）。

```tcl
11. Printing statistics.

# ...

=== Mux0 ===

   Number of wires:                 61
   Number of wire bits:            167
   Number of public wires:          10
   Number of public wire bits:     116
   Number of ports:                  7
   Number of port bits:             68
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:                 67
     $_ANDNOT_                      32
     $_AND_                          1
     $_MUX_                         16
     $_ORNOT_                        2
     $_OR_                          16

# ...

=== RegEn ===

   Number of wires:                  5
   Number of wire bits:             35
   Number of public wires:           5
   Number of public wire bits:      35
   Number of ports:                  5
   Number of port bits:             35
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:                 16
     $_DFFE_PP_                     16

# ...
```

Yosys 从 Verilog 代码出发，经历了两个主要阶段，逐步把电路“变得越来越具体”：

**第一阶段：模块化、抽象表示（初步转换）**

- Yosys 首先把 Verilog 代码转成一种叫**内部单元（Internal Cells）**的表示。
- 这些单元可以是：
  - 多位的数学逻辑操作（比如 32 位的加法、减法、与运算等）
  - 控制结构（比如状态机 FSM）
  - 存储结构（比如 memory）
- 这一步是“模块化”和“抽象”的，也就是说，电路逻辑还比较高层、容易看懂。

**第二阶段：门级（Gate-level）表示（综合后）**

- 运行 `synth` 命令时，Yosys 会把这些抽象的结构转成一个个基础逻辑门（像搭积木一样）。
- 最终会看到非常底层的构造：比如 `$_ANDNOT_`、`$_MUX_`、`$dff` 等等。
- 这些结构就像芯片制造中真实存在的电路原件一样，非常精细。

```tcl
write_verilog section1/sub/postsynth.v
write_rtlil section1/sub/postsynth.rtlil
```

#### Optimization and Techmapping

**背景概念：技术无关（Technology-agnostic） vs 技术映射（Techmapping）**

1. **技术无关阶段**：
   Yosys 在综合初期，会把 Verilog 代码转换成一种中立的表示方式（使用内部单元、word-level 单元等），这时候还没和具体芯片工艺（PDK）绑定，称为 **technology-agnostic**。
2. **技术映射（techmapping）**：
   最终要把电路落实到真实芯片里的，而芯片制造商会提供 **标准单元库（standard cell library）**，例如各种 AND、MUX、DFF 等门电路。要让电路能在真实芯片中实现，就必须把技术无关的表示映射到具体 PDK 提供的单元上，这个过程叫 **techmapping**。

**ABC 工具（由加州大学伯克利开发）**

Yosys 使用一个外部工具 **ABC** 来完成优化和映射的工作：

1. **abc 命令的流程：**

   - 把设计转为 ABC 格式
   - 可选地分成组合逻辑部分
   - 调用 ABC 优化逻辑结构
   - 把结果再转回 Yosys 使用的格式

2. **ABC 内部的优化结构**：

   使用一种称为 **AIG（AND-Inverter Graph）** 的结构：

   - 全是 2 输入 AND 门和反相器（inverter）
   - 简单但强大，适合：冗余去除；逻辑等价检查；结构优化搜索；时序优化（retiming）

**Liberty 文件？**

1. **Liberty 文件是什么？**

   一个包含了某 PDK 中所有标准单元的详细信息的文件，包括：延迟（delay）；功耗（power）；逻辑功能（function）

2. **作用**：

   ABC 利用 Liberty 文件可以在多个候选实现之间选择最优的门单元，从而：

   - 提高速度（考虑时序）
   - 减少面积（考虑资源使用）
   - 实现真实芯片制造级别的电路映射

3. **OpenROAD 的结合**：

   后续像 OpenROAD 这种布局布线工具也可以继续调用 ABC，对设计进行 **动态重优化（re-optimization）**，比如根据布局后新的时序信息再次进行映射优化。

```tcl
design -reset # Clear out the loaded design
read_verilog section1/gcd.v
hierarchy -top gcd 

flatten
# Technology-agnostic Verilog-level optimizations
prep
# Synthesize to technology-agnostic gate-level primitives
synth
# Replace any agnostic DFF primitives that cannot be mapped directly to IHP 130's DFF cells
dfflibmap -liberty section1/sg13g2_stdcell_typ_1p20V_25C.lib
# Call into ABC to synthesize with a timing goal of 4000 ps = 4 ns  on the worst path.
abc -D 4000 -liberty section1/sg13g2_stdcell_typ_1p20V_25C.lib
# Remove disconnected wire that ABC optimized away
opt_clean 

write_verilog section1/sub/postmap.v
```

- `design -reset`

  清除当前已加载的设计数据，类似于“重置”操作，确保后续流程从一个干净的状态开始。

- `read_verilog gcd.v`

  读取 Verilog 源文件（例如 `gcd.v`），并将其加载到 Yosys 的内部表示中。这一步是把 HDL 描述转化为 Yosys 能理解的数据结构。

- `hierarchy -top gcd`

  分析模块之间的层级关系，并指定顶层模块为 `gcd`。 如果有子模块，它也会自动补全（如果找得到）并报错找不到的模块。

- `flatten`

  将设计中所有层级“扁平化”，即将子模块内容直接展开到顶层模块中。对较小的设计或需要与外部工具兼容时常见。**注意：大型设计不建议频繁 flatten，会失去层次结构。**

- `prep`

  `read_verilog + hierarchy + proc + opt + techmap` 等一系列常用步骤的组合命令，用于快速准备设计。但在这里 `prep` 紧接着在 `flatten` 后使用，其实只起到简单准备作用。

- `synth`

  将 Verilog 高层结构综合为 Yosys 内置的、**技术无关（technology-independent）**门级单元，如：`$and`, `$or`, `$not`, `$mux`, `$dff` 等。此阶段的电路结构只使用逻辑通用门，尚未和 PDK 绑定。

- `dfflibmap -liberty sg13g2_stdcell_typ_1p20V_25C.lib`

  把技术无关的 DFF 映射到 **Liberty 文件中定义的 DFF 单元**。 因为 `$dff` 是抽象的 D 触发器表示，IHP PDK 会提供具体实现，比如：`DFFQX1`, `DFFRXL`, `DFFNQX2` 等。如果不映射，有些 `$dff` 可能在之后无法转换为具体电路。

- `abc -D 4000 -liberty sg13g2_stdcell_typ_1p20V_25C.lib`

  ABC 调用，用于做 **技术映射** 和 **时序优化**。

  - `-D 4000`：目标最坏路径延迟为 4000ps（4ns），也就是设定频率目标为 250MHz。

  - `-liberty`：提供对应标准单元库，用于映射逻辑门、MUX 等为 PDK 提供的真实单元。

  ABC 会尝试：

  - 替换逻辑组合部分为标准单元
  - 在满足时序目标的前提下尽量减少面积、提升性能

- `opt_clean`

  清理冗余电路：去除无连接的 wire、未用的模块/门。 这是一个**整理优化结构**的步骤，特别是在 ABC 优化后，有些门被删掉了，但 wire 名还留着。

#### Timing and Power with OpenSTA

```bash
# exit yosys
sta  # open OpenSTA

# Timing check 

read_verilog section1/sub/postmap.v
read_liberty section1/sg13g2_stdcell_typ_1p20V_25C.lib
link_design gcd
# OpenSTA defaults to using the PDK's units loaded from the liberty file. Try running report_units.
create_clock -name clk -period 4 {clk}
# Write a Standard Delay Format file as part of your submission
write_sdf section1/sub/postmap.sdf
report_checks
```

- `read_verilog section1/sub/postmap.v`

  读取综合后的 Verilog 网表文件 `postmap.v`，也就是**映射到标准单元后的门级网表**。这一步是载入要进行时序分析的**电路结构**。

- `read_liberty section1/sg13g2_stdcell_typ_1p20V_25C.lib`

  读取标准单元库（Liberty 文件），该文件包含：

  - 单元延迟信息（如 `AND2`, `MUX`, `DFF` 等延迟）
  - 驱动能力、负载响应、建立/保持时间等

  这是时序分析的基础，OpenSTA 将用它来评估每个门和路径的时间。

- `link_design gcd`

  链接设计结构。`gcd` 是顶层模块名，它会将之前 `read_verilog` 加载的设计层次连接成一个完整的时序图。这一步之后，STA 才能识别所有的路径、端口、cell。

- `create_clock -name clk -period 4 {clk}`

  创建一个名为 `clk` 的时钟，周期为 4ns（= 250 MHz），作用于 `clk` 信号。

  STA 分析必须有时钟，才能知道从一个触发器到另一个触发器之间**时间限制**是多少（setup/hold 检查）。

- `write_sdf section1/sub/postmap.sdf`

  将 STA 分析结果导出为一个 **标准延迟格式文件（SDF）**，该文件可用于：

  - 仿真工具（如 ModelSim）
  - 后仿或时序仿真（Post-Synthesis Simulation）

  其中包括路径延迟、门延迟、边沿类型等详细信息。

- `report_checks`

  输出 **关键路径的时序检查结果**，包括：

  - Setup violations（建立时间违规）
  - Hold violations（保持时间违规）
  - 哪些路径是时序最紧张的（critical path）

```tcl
Startpoint: _432_ (rising edge-triggered flip-flop clocked by clk)
Endpoint: _451_ (rising edge-triggered flip-flop clocked by clk)
Path Group: clk
Path Type: max

  Delay    Time   Description
---------------------------------------------------------
   0.00    0.00   clock clk (rise edge)
   0.00    0.00   clock network delay (ideal)
   0.00    0.00 ^ _432_/CLK (sg13g2_dfrbp_1)
   0.21    0.21 v _432_/Q (sg13g2_dfrbp_1)
   0.09    0.30 v _243_/Y (sg13g2_nor2b_1)
   0.13    0.42 ^ _290_/Y (sg13g2_o21ai_1)
   0.11    0.54 v _291_/Y (sg13g2_a21oi_1)
   0.14    0.68 ^ _294_/Y (sg13g2_o21ai_1)
   0.11    0.79 v _295_/Y (sg13g2_a21oi_1)
   0.16    0.95 ^ _298_/Y (sg13g2_o21ai_1)
   0.12    1.07 v _300_/Y (sg13g2_a221oi_1)
   0.15    1.22 ^ _301_/Y (sg13g2_nor3_1)
   0.08    1.30 v _303_/Y (sg13g2_nor3_1)
   0.14    1.44 ^ _304_/Y (sg13g2_nor3_1)
   0.09    1.52 v _306_/Y (sg13g2_nor3_1)
   0.14    1.66 ^ _307_/Y (sg13g2_nor3_1)
   0.13    1.80 v _340_/Y (sg13g2_nand3_1)
   0.47    2.27 ^ _382_/Y (sg13g2_a21oi_1)
   0.14    2.41 v _383_/Y (sg13g2_a22oi_1)
   0.14    2.55 ^ _385_/Y (sg13g2_a221oi_1)
   0.00    2.55 ^ _451_/D (sg13g2_dfrbp_1)
           2.55   data arrival time

   4.00    4.00   clock clk (rise edge)
   0.00    4.00   clock network delay (ideal)
   0.00    4.00   clock reconvergence pessimism
           4.00 ^ _451_/CLK (sg13g2_dfrbp_1)
  -0.14    3.86   library setup time
           3.86   data required time
---------------------------------------------------------
           3.86   data required time
          -2.55   data arrival time
---------------------------------------------------------
           1.31   slack (MET)
```

```tcl
report_clock_min_period

# Output
clk period_min = 2.69 fmax = 371.19
```

在使用 Yosys 的 ABC 后端综合时，**即使设置了更小的目标时钟周期 `abc -D <period>`，最终的 `clk period_min`（最小周期）也未必变小**。这背后的本质原因可以从以下几个方面来解释：

1. **ABC 是“试着满足目标周期”，而不是“强行优化到目标周期”**

   ```tcl
   abc -D 2500  ; # 设定目标周期为 2.5ns
   ```

   ABC 的含义是：

   > “我会尝试对这个电路进行重新结构化（重定时、映射、优化），以实现小于等于 2.5ns 的逻辑路径。”

   **但 ABC 并不保证一定能做到目标周期**，因为：

   - 它受限于你电路的结构复杂度；
   - 它只能用 `.lib` 中提供的标准单元（standard cells）进行拼接优化；
   - 它的优化过程是启发式的，不是穷举所有可能。

   **如果你设定的目标小于当前结构所能实现的最小路径 delay，ABC 也只能尽力而为**，最后还是会输出一个大于目标周期的结果。

2. **设计本身已经达到逻辑极限**

   每个电路的最长关键路径由逻辑深度和库中的单元延迟共同决定。

   即使你告诉 ABC “我要 2.0ns”，但如果这个电路：

   - **最短也要通过 10 级门，每级 delay ≈ 0.3ns**；
   - 那即使 ABC 使出浑身解数，它也**无法把 delay 压缩到 2.0ns 以下**，你仍然会得到如 `clk period_min = 2.8ns` 的结果。

3. **ABC 优化是有损耗的，过度优化可能反而变差**

   有时你设定一个 **非常小的目标周期（例如 1.5ns）** 时：

   - ABC 会强行重写逻辑结构；
   - 但这些变换可能引入更多级联逻辑，导致反而**delay 更大**。

   这就是你观察到的现象：

   > 当你设定周期为 2.0、2.5、2.7ns 时，**`clk period_min` 反而回升到 2.8ns**。

   这说明：

   - ABC在试图压缩 delay 时“过度优化”，结果适得其反；
   - 有可能是关键路径结构变复杂，或者 cell mapping 结果次优。

4. **ABC 的综合行为是离散的，不是连续可调的**

   你设置的目标 `-D` 是一个参考目标，ABC 并不会连续、线性地从 3.0 优化到 2.5、再到 2.0。而是：

   - 针对每个目标值，它会走一个独立的优化路径；
   - 某些 `-D` 值反而走到更糟糕的局部最优（local minimum）；
   - 所以你看到的 `clk period_min` 可能不是单调变化的。

### 2-Design Space Exploration

#### ASQRT

该模块实现了一个可配置的、**并行平方根加速器**，使用迭代算法来计算一个 32 位输入整数的平方根 —— 算法的每一次迭代会生成或逼近输出结果的一个比特位。

该设计包含以下几个参数：

- **`N_PIPES`**：控制平方根计算流水线的并行数量。
- 每条流水线可以通过 **`N_DEPTH`** 参数进行配置，它决定了每个时钟周期中执行的迭代次数 —— 实际上控制了每一位输出所需的周期数（也就是说，**更深的流水线每位输出的延迟更低**）。
- **`N_CYCLES`** 参数设置了每条流水线允许运行的总周期数。它必须 **大于等于输出位数除以流水线深度的结果**。

对 **`N_PIPES`**、**`N_DEPTH`** 和 **`N_CYCLES`** 这三个参数进行 DSE设计空间探索。

```bash
# Python 依赖
pip install matplotlib
```

#### [RTFSC](./RTFSC.md)

由 Grok3 生成。

#### DSE

第一步是定义一些设计需求 —— 这样可以限定变量的取值范围，从而减少变量数量。

先设定一个性能需求：**我们希望达到每个周期完成一次平方根计算的吞吐量**。这就建立了 `N_PIPES` 与 `N_CYCLES` 之间的 1:1 关系。也就是说，**如果一条流水线计算一个平方根需要 2 个周期，那么就需要 2 条并行流水线才能满足我们的目标吞吐量**。

在完成本轮参数扫描后，我们将生成一个所谓的“**与频率无关的等性能（iso-performance）”对比图**。这里的“与频率无关”是关键点：虽然我们在所有配置中都对吞吐量进行了归一化处理，但**实际的吞吐性能仍然强烈依赖于设计所能达到的最大工作频率（f_max）**，这也是我们之后会对 f_max 进行分析并绘图的原因。

### 3-Closing the Loop

```bash
# section3
orfs_copy
make --file=OpenROAD-flow-scripts/flow/Makefile DESIGN_CONFIG=config.mk
```

