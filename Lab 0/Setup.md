### Docker

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

### ORFS

```bash
mkdir /work && cd $_
orfs_copy orfs_lab0
cd orfs_lab0/flow    # base dir
# 工程结构
./flow
|-- BUILD.bazel
|-- Makefile
|-- designs
|-- platforms
|-- scripts
|-- test
|-- tutorials
`-- util
```

本项目设计的手语翻译系统基于 RDK-X5 开发板，实现边缘部署和BPU推理加速。系统通过摄像头实时捕捉用户的手语动作，并通过骨骼点识别模型提取每一帧图像中的骨骼点信息，包括双手总共42个骨骼点。系统通过关键帧提取算法，从连续的视频流中选取36帧关键帧，构建稳定的骨骼点时间序列，完整表征一个手语动作的动态过程。随后，该序列被输入至双向长短时记忆网络（BiLSTM）模型中，利用其在时间维度上的双向上下文建模能力，对手势动作进行精准分类与识别。目前，该系统能够稳定识别500个中文手语词汇，涵盖日常交流中的高频词汇与句式，支持多轮交互，在实际测试中具备较强的准确性、实时性与适用性，为手语用户与物联网控制系统之间构建了高效的沟通桥梁。
在性能方面，系统使用的所有模型均经过量化转换后通过 RDK BPU 进行加速推理，以确保系统具有较强的实时性，降低处理延迟。该系统既可以有效帮助听障人士与他人进行便捷的交流，也可以完成流畅的物联网设备控制。
同时，为了帮助聋哑人群更好地融入现代智慧生活，本系统基于火山引擎物联网平台及大模型网关进行整体架构设计与开发。通过ESP32 接受云平台的命令，并控制接入的各类外设组成一个本地智能家居群组，提供了一个标准的物联网智能家居模块。在用户端，用户通过RDK-X5 识别所做的手语动作，使用大语言模型解析手语命令，将解析后的控制信号上传云平台。云端接收到信号后，通过火山引擎的物联网平台转发指令至对应的 ESP32 控制器，实现对目标设备的控制操作，完成手语指令对智能家居的控制。
同时，通过接入火山引擎的大模型网关，该系统也支持用户通过手语直接与大语言模型进行自然交互。用户不仅可以完成基础的设备控制指令，还可以进一步实现如知识问答、天气查询等复杂任务。这使该系统不仅是一个手语控制终端，更是一个具备智能对话和知识服务功能的多模态交互平台。

