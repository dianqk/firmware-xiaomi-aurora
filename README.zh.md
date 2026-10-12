# Xiaomi 14 Ultra 固件

[English](README.md)

适用于 **Xiaomi 14 Ultra（aurora，SM8650）** 的原厂运行时固件与 OEM 配套数据。
当前开发基线为中国版 Android 14 fastboot ROM **OS1.0.3.0.UNACNXM**
（运行时版本 V816.0.3.0.UNACNXM）。安装 Linux 前应先刷入该精确版本的底包。

| 目录 | 原厂版本 | 用途 |
| --- | --- | --- |
| `android14/` | OS1.0.3.0.UNACNXM | 当前开发基线，含 ADSP、基带、GPU、视频、Wi-Fi、蓝牙、音频、传感器和触控数据 |
| `android16/` | OS3.0.7.0.WNACNXM | 保留的兼容性研究数据，仅含 ADSP、GPU、视频、Wi-Fi 和蓝牙 |

两套数据应分别使用，不能因为文件更新就混用。仓库不提供引导链、安全固件等
底层分区镜像，也不提供刷写脚本。运行时固件仍依赖匹配的底层固件；例如，
Android 14 安全固件曾拒绝 Android 16 的 ADSP 镜像，导致电池遥测不可用。

在仓库根目录校验：

```sh
python3 verify.py
sha256sum -c SHA256SUMS
```

`SOURCE.json` 记录全部 758 个原始数据文件的来源路径、长度、SHA-256、ROM
版本与导入来源；每个组件也有独立校验清单。所有原始文件均保持字节内容不变，
直接由 Git 管理，不依赖 Git LFS。校验只在主机运行，不访问设备。

音频目录中的 `-tt` 文件是原厂产品调音参数，个人功放校准不在此仓库。
蓝牙目录保存未修改的原厂 NVM，不包含本机 MAC 或运行时校准覆盖。
传感器目录是原厂配置和 DSP 文件，不含可写的原机校准 registry。
触控目录含原厂 AArch64 用户态处理库和配置；它不是触控控制器固件。
`android14/modem/` 是 `modemfirmware` 分区（`MODEM-FW.bin`）`image/` 的完整内容，
另含 `NON-HLOS.bin/image` 中分段的 IPA GSI 固件；基带通过 TFTP 只读读取其中的
`modem_pr/mcfg` 等文件。每台手机独有的基带 NV 分区（modemst1/2、fsg、fsc）不在此仓库。

Nix 打包、内核驱动、ALSA UCM/topology、Wi-Fi 容器生成、传感器 registry
生成及触控适配程序继续由
[nixos-android-devices](https://github.com/dianqk/nixos-android-devices) 管理。
消费者应固定提交和内容哈希，选择对应版本目录，按需生成 Linux 安装布局。
详细文件分类和安装路径见 [英文说明](README.md)。

本仓库不含分区备份、`persist`、基带 NV、本机 MAC 覆盖或个人校准数据。原厂二进制与
配套数据保留原权利人的权利；[LICENSE](LICENSE) 仅适用于仓库自编文档和
校验代码，边界见 [NOTICE](NOTICE)。
