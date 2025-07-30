## Lab 0

### Docker Setup

```powershell
# 下载 Docker Desktop
# 更新 WSL
wsl --update

# 运行实验容器
docker run -it --name my-lab-0 ghcr.io/udxs/ece260c-essential:main
# 退出后重新运行
docker start -i my-lab-0
# GUI
docker run -it -v /run/desktop/mnt/host/wslg/.X11-unix:/tmp/.X11-unix ` -v /run/desktop/mnt/host/wslg:/mnt/wslg ` -e DISPLAY=:0 ` -e WAYLAND_DISPLAY=wayland-0 ` -e XDG_RUNTIME_DIR=/mnt/wslg/runtime-dir ` --name ece260c0 ghcr.io/udxs/ece260c-essential:main
# GUI test
openroad -gui

# VS Code 插件
Dev Containers
```

### 1-Basic Setup

```bash
mkdir /work && cd $_
orfs_copy orfs_lab0
cd orfs_lab0/flow    # base dir

# tree
apt update && apt install -y locales
locale-gen en_US.UTF-8
echo 'export LANG=en_US.UTF-8' >> ~/.bashrc
source ~/.bashrc
apt install tree

# 工程结构
(base) root@85fdc351cdc4:/work/orfs_lab0# tree -L 1 flow/
flow/
├── BUILD.bazel
├── designs
├── Makefile
├── platforms
├── scripts
├── test
├── tutorials
└── util

6 directories, 2 files
```

```bash
# 查看 config.mk
# https://openroad-flow-scripts.readthedocs.io/en/latest/user/FlowVariables.html
cat ./designs/ihp-sg13g2/gcd/config.mk
```

```makefile
export DESIGN_NAME = gcd
export PLATFORM    = ihp-sg13g2

export VERILOG_FILES = $(DESIGN_HOME)/src/$(DESIGN_NICKNAME)/gcd.v
export SDC_FILE      = $(DESIGN_HOME)/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export USE_FILL = 1

export PLACE_DENSITY ?= 0.88
export CORE_UTILIZATION = 20
export TNS_END_PERCENT = 100
```

1. `USE_FILL`：**Metal density filling（金属密度填充）** 是一种**后端物理设计（Physical Design）流程中的工艺要求**，其目的是在芯片版图中**填充虚拟金属结构**，以满足制造工艺对于金属层密度的限制。

2. `PLACE_DENSITY`：

   所需的平均单元放置密度：设置为 **1.0** 表示布局非常**紧密**，而 **0.0** 表示布局非常**稀疏**。此参数同时也表达了布图工具需要投入的优化**努力程度**。 如果你希望构建流程**更快完成**，可以使用较低的密度值；若希望获得**更高质量的结果（QoR）**，则应使用较高的密度值。 如果密度设置得**过低**，布图器（placer）可能无法将所有单元放下，此时你可以在日志中找到推荐的**最小放置密度**。反之，密度设置得**过高**，可能会导致：

   > 运行时间过长；甚至发生超时；后续流程（如时钟树综合 CTS 或全局布线 global routing）中出现**隐性失败**，比如因为时序修复失败而导致整个设计不满足性能要求。
   
   不同平台（PDK）有不同的默认密度设置。

3. `CORE_UTILIZATION`：数字参数，表示 **核心区（Core）中标准单元的利用率百分比**，取值范围是 **0 到 100**。
4. `TNS_END_PERCENT`：**是用于时钟树综合（CTS）之后的时序修复阶段的默认设置。**默认情况下，会尝试修复所有存在违反时序要求的终点（endpoints）。 如果希望缩短运行时间，可以将该值降低到 5%。 它用于指定需要修复的时序违例路径的比例，取值范围为 0 到 100。 无论设置是多少，最差（worst）的路径总是会被修复。

### 2-Running the Flow

```bash
# 默认的 make 使用不可制造的 PDK，故改用 ihp-sg13g2
DESIGN_CONFIG=./designs/ihp-sg13g2/gcd/config.mk make

# Error1
[ERROR STA-0562] repair_timing -sequence is not a known keyword or flag.
Error: floorplan.tcl, 110 STA-0562
# 修复 scripts/util.tcl
proc repair_timing_helper { args } {
  set additional_args "$args -verbose"
  append_env_var additional_args SETUP_SLACK_MARGIN -setup_margin 1
  if { $::env(HOLD_SLACK_MARGIN) < 0 } {
    append_env_var additional_args HOLD_SLACK_MARGIN -hold_margin 1
  }
  # append_env_var additional_args SETUP_MOVE_SEQUENCE -sequence 1
  append_env_var additional_args TNS_END_PERCENT -repair_tns 1
  append_env_var additional_args SKIP_PIN_SWAP -skip_pin_swap 0
  append_env_var additional_args SKIP_GATE_CLONING -skip_gate_cloning 0
  append_env_var additional_args SKIP_BUFFER_REMOVAL -skip_buffer_removal 0
  append_env_var additional_args SKIP_LAST_GASP -skip_last_gasp 0
  append_env_var additional_args MATCH_CELL_FOOTPRINT -match_cell_footprint 0
  log_cmd repair_timing {*}$additional_args
}

# Error2
[ERROR STA-0562] clock_tree_synthesis -repair_clock_nets is not a known keyword or flag.
Error: cts.tcl, 35 STA-0562
# 修复 scripts/cts.tcl
# Run CTS
set cts_args [list \
  -sink_clustering_enable \
  -balance_levels]
  # -repair_clock_nets
```

```bash
# 查看结果
cat reports/ihp-sg13g2/gcd/base/6_finish.rpt | less
cat reports/ihp-sg13g2/gcd/base/6_finish.rpt | tail -n 30
# 清空结果
DESIGN_CONFIG=./designs/ihp-sg13g2/gcd/config.mk make clean_all
ls logs/ihp-sg13g2/gcd/base
ls results/ihp-sg13g2/gcd/base
```

| 指标                           | 含义               | 值      | 含义解释               |
| ------------------------------ | ------------------ | ------- | ---------------------- |
| **WNS (Worst Negative Slack)** | 最差路径的负裕度   | 0.00 ns | 没有任何路径违反时序   |
| **TNS (Total Negative Slack)** | 所有违反路径的总和 | 0.00 ns | 所有路径都满足时序要求 |

### 3-Editing Flow Parameters

#### **aspect ratio (AR) of the core**

`CORE_ASPECT_RATIO`：核心区域的长宽比（高度/宽度）。如果未定义 `CORE_UTILIZATION`，则此值将被忽略。 默认值为 1.0。

```makefile
# 根据学号确定值
export DESIGN_NAME = gcd
export PLATFORM    = ihp-sg13g2

export VERILOG_FILES = $(DESIGN_HOME)/src/$(DESIGN_NICKNAME)/gcd.v
export SDC_FILE      = $(DESIGN_HOME)/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export USE_FILL = 1

export PLACE_DENSITY ?= 0.88
export CORE_ASPECT_RATIO = 0.35
export CORE_UTILIZATION = 20
export TNS_END_PERCENT = 100
```

```bash
# 更多的查看 reports 的方法
DESIGN_CONFIG=./designs/ihp-sg13g2/gcd/config.mk make open_final
DESIGN_CONFIG=./designs/ihp-sg13g2/gcd/config.mk make gui_final
# 将 final 后缀替换为 floorplan、place、cts、route、grt、final 等阶段名称，来加载处于不同设计阶段的数据库。
```

#### **关于GUI Inspector的一些参数说明**

- **Block/module（模块）**：用于分层设计（hierarchical design），我们将在后续的实验中进行讨论。
- **Master（母块）**： 表示当前使用的具体单元。在这个PDK（工艺开发包）中，所有母块的前缀为 `sg13g2_`。你可以点击该条目来查看关于这个单元的详细信息。
- **ITerms（实例管脚）**： 表示与该单元连接的端口，包括电源和时钟（如适用）。 将鼠标悬停或点击它们，可以查看它们连接的网（net）。
- **Placement Status / Don’t Touch（布局状态 / 禁止修改）**： 这些属性由 OpenROAD 的不同模块使用，用于标记哪些单元可以被修改。 例如，如果在执行全局布局（Global Placement）之前将某个单元的 **布局状态设置为 FIRM**，布局器将不会移动这个单元。我们将在之后的实验中利用这个特性。
- **Timing / Power（时序 / 功耗）**： 点击此选项可以访问包含到达时间（arrival times）、功耗活动（power activities）和总功耗的报告，并可查看关联的 Liberty 单元库条目。
- **Source（源）**： 对于某些D触发器（D Flip Flop），此字段会显示该触发器在 Verilog 源代码中所对应的寄存器名。

#### **左侧的显示控制区域（Display Control area）**

这个区域允许你**显示或隐藏不同的图层和视图**。你可以利用它来更清楚地了解设计是如何布局（place）和布线（route）的。

例如，你可以：

- 隐藏图层，只查看实例（Instances）被放置的位置；
- 或者隐藏顶层金属层，以便在不被大型电源网络遮挡的情况下查看单元。

你还可以**控制图层是否可点击**（最右侧的复选框列）。当你取消勾选某个图层（比如 Metal5 的垂直电源线）后，就可以点击其下方的元素了。

#### **热力图（Heatmaps）**

提供关键的空间统计信息。打开 Heatmaps 部分，并一次只选择一个（**IR Drop** 可能不会显示数据，可以忽略）。如果你觉得热力图过于细碎、过于粗略，或者包含了不需要的元素，可以通过：**Tools > Heatmaps**，进入设置界面，修改网格大小或其他选项。对于我们的用途来说，**默认的 10x10 网格热力图就足够了**。

| 热力图类型             | 中文名              | 主要反映内容                              | 工具作用与设计意义                                 |
| ---------------------- | ------------------- | ----------------------------------------- | -------------------------------------------------- |
| **Pin Density**        | 引脚密度            | 某区域内引脚（Pin）数量分布               | 检查是否有引脚过于集中区域，避免布线拥塞与连线复杂 |
| **Placement Density**  | 单元放置密度        | 标准单元在某区域的面积占比                | 检查单元是否过于拥挤或稀疏，评估布线空间是否充足   |
| **Power Density**      | 功率密度            | 每个区域单位面积内的功耗分布（如 mW/mm²） | 查找功耗热点，辅助进行电源网络规划、散热优化       |
| **Estimated Density**  | 估算密度            | 布局器根据算法预测的单元密度分布          | 预测后续布线可能出现的密度瓶颈、优化布局策略       |
| **IR Drop**            | 电压下降（IR Drop） | 电源线上因电阻导致的电压下跌量            | 评估电源完整性，避免因供电不足引发的时序或功能错误 |
| **Routing Congestion** | 布线拥塞情况        | 评估某区域布线资源是否充足/已饱和         | 判断布线压力，避免线长过高或拥塞引发布线失败       |

#### **Timing Report** 标签页（与 Inspector 在同一区域）

可以看到 Setup 和 Hold 两种时序中，**slack 最低（或者说 WNS 最大）的路径**。

在 Setup 部分，点击 **Slack** 列标题，将路径按 slack 从低到高排序，然后点击排在最前面的条目。

假如你已经放大到足够的程度，你应该能看到：

- 时钟路径（包括时钟缓冲器）会以蓝色高亮显示，
- 数据路径（datapath）则以红色高亮显示。

如果不隐藏某些图层，默认配色下可能不太容易看清楚这些高亮。

1. **Setup Time（建立时间）**

   - **定义**：数据必须在时钟上升沿（或下降沿，取决触发器设计）到来之前，保持稳定的最短时间间隔。
   - **作用**：确保数据在时钟触发器采样时，数据已经稳定，能够被正确捕获。
   - **如果违反**：可能导致数据未稳定就被采样，产生错误值（Setup violation）。

2. **Hold Time（保持时间）**

   - **定义**：数据在时钟边沿到来之后，必须保持稳定的最短时间间隔。
   - **作用**：确保时钟采样完成后，数据不会立即变化，避免采样错误。
   - **如果违反**：可能导致触发器采样到错误的短暂数据（Hold violation）。

3. **Slack（时序裕量）**

   - **定义**：Slack 是时序路径上可用的“多余时间”，计算方法为：
     $$
     \text{Slack} = \text{Required Arrival Time} - \text{Actual Arrival Time}
     $$

   - **意义**：如果 **Slack ≥ 0**，表示该路径满足时序约束，有剩余时间，设计时序安全；如果 **Slack < 0**，表示时序违例，路径上的信号到达太晚，可能导致错误。

   - **用途**：帮助设计者判断哪些路径存在时序风险，优先优化负 Slack 路径。

4. **WNS（Worst Negative Slack，最坏负裕量）**

   - **定义**：设计中所有路径中最小（最差）的 Slack 值（通常是负值）。   也就是所有路径中负 Slack 的最大绝对值。

   - **意义**： 代表设计中最严重的时序违例程度； WNS 越接近 0，设计时序越接近闭合；WNS 如果是负数，说明设计存在时序违例。

#### 其他工具

- 右侧面板中与 Inspector 和 Timing Report 同级的 **Charts（图表）** 标签页；

- **Find（查找）工具**；

- **时钟树查看器（Clock Tree Viewer）**： 可以通过菜单栏的 **Windows > Clock Tree Viewer** 来启用； 启用后，在右侧面板中选择 **Clock Tree Viewer** 标签页； 选择 “default” 配置，然后点击 **Update（更新）**。

  这个界面会显示时钟树的分布情况：时钟从端口进入（红色三角形标记），经过缓冲器（蓝色三角形标记），并分发到一组组触发器（图表底部以红色高亮显示的部分）。

### 4-Submitting

```bash
# 提交以下文件和报告
designs/ihp-sg13g2/gcd/config.mk
reports/ihp-sg13g2/gcd/base/6_finish.rpt
reports/ihp-sg13g2/gcd/base/cts_core_clock_layout.webp.png
logs/ihp-sg13g2/gcd/base/6_report.json
results/ihp-sg13g2/gcd/base/6_final.gds
```

```powershell
# 避免跨系统换行符不兼容
git config --global core.autocrlf false
```

