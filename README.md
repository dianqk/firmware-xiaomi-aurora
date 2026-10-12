# Xiaomi 14 Ultra firmware

[中文](README.zh.md)

Stock runtime firmware and OEM support data for **Xiaomi 14 Ultra (aurora,
SM8650)**. The development baseline is the China Android 14 fastboot ROM
**OS1.0.3.0.UNACNXM** (runtime build V816.0.3.0.UNACNXM).

Install that exact factory base before installing the supported Linux system.
This repository supplies runtime files; it does not replace the bootloader,
secure firmware or other factory firmware partitions. Android 14 and Android 16
files are separate release sets, not interchangeable updates.

| Directory | Factory release | Contents |
| --- | --- | --- |
| `android14/` | OS1.0.3.0.UNACNXM | ADSP, modem, GPU, video, Wi-Fi, Bluetooth, speaker DSP, sensors and touch support |
| `android16/` | OS3.0.7.0.WNACNXM | ADSP, GPU, video, Wi-Fi and Bluetooth; compatibility research only |

## Verify the files

From the repository root:

```sh
python3 verify.py
sha256sum -c SHA256SUMS
```

`SOURCE.json` lists every payload's stock path, size and SHA-256, the source ROM
versions and the original import revision. `SHA256SUMS` covers all 758 payloads;
each component also has a local checksum list. Git attributes preserve original
line endings and whitespace in OEM configuration files. Verification is host-only and
does not access or modify a device. Git stores the actual files, without LFS.

## Components

- `adsp/`: unchanged split MDT/Bxx images and service descriptors from
  `NON-HLOS.bin/image`. Keep each MDT and its segments together.
- `android14/modem/`: the complete `image/` tree of the `modemfirmware`
  partition (`MODEM-FW.bin`: split modem and modem DTB images, service
  descriptors, `qdsp6m.qdb` databases and the `modem_pr/mcfg` carrier
  configurations) plus the split IPA GSI firmware from `NON-HLOS.bin/image`.
  The modem reads the remaining files over TFTP from its read-only firmware
  root. Modem NV data (`modemst1`, `modemst2`, `fsg`, `fsc`) is per-handset
  and is not included.
- `gpu/`: Adreno 750 SQE, GMU and signed ZAP firmware.
- `video/`: complete signed VPU33 ELF firmware, not concatenated MDT segments.
- `wlan/`: matching AMSS, M3 ELF, N1 board data and Xiaomi regulatory data.
- `bluetooth/`: patch TLV and **unmodified stock NVM**. The stock NVM is not a
  substitute for a handset's runtime radio calibration or Bluetooth address.
- `android14/audio/`: shared CS35L43 protection firmware and OEM `-tt` tuning
  coefficients selected by the stock driver. Product tuning is included;
  handset-specific speaker calibration is not. See [audio data](android14/audio/README.md).
- `android14/sensors/`: 68 selected OEM configuration files and 10 Hexagon DSP
  files. Writable registry state is not included. See [sensor data](android14/sensors/README.md).
- `android14/touch/`: proprietary AArch64 host processing library and board
  configuration. The library is userspace code, not controller firmware;
  see [touch data](android14/touch/README.md).

## Linux integration

This is a data repository. Nix derivations, kernel changes, ALSA UCM/topology,
radio container generation, sensor registry generation and the touch adapter
remain in [nixos-android-devices](https://github.com/dianqk/nixos-android-devices).
A consumer should pin a commit and content hash, select one release directory,
and apply its own installation layout. There is no flashing or installation script.

The integration uses these runtime paths:

| Data | Installed location or processing |
| --- | --- |
| ADSP and ZAP/video firmware | `lib/firmware/qcom/sm8650/xiaomi/aurora/` |
| Modem and IPA | `lib/firmware/qcom/sm8650/xiaomi/aurora/`, keeping the `modem_pr/` tree; the TFTP server maps `/readonly/firmware/image/` there |
| GPU SQE/GMU | `lib/firmware/qcom/` |
| WLAN | `ath12k/WCN7850/hw2.0/`: AMSS → `amss.bin`, M3 → `m3.bin`; combine N1 BDF and REGDB into `board-2.bin` |
| Bluetooth | `lib/firmware/qca/xiaomi/aurora/` |
| Speaker DSP | Aurora-scoped WMFW/coefficient filenames; see the consumer audio package |
| Sensors | Generate SSC registry from the selected configs; install DSP support separately |
| Touch | Supply the unchanged library/config to the Aurora host adapter |

These files do **not** make the system independent of the factory base. For
example, Android 14 secure firmware rejected the larger Android 16 ADSP image;
battery telemetry was then unavailable. Select matching firmware and reboot
with a matching initrd; replacing live remoteproc files is not a compatibility test.
Hardware support and validation status belong in the consumer's
[Aurora guide](https://github.com/dianqk/nixos-android-devices/blob/main/docs/aurora/README.md).

## Provenance and licensing

The payloads were imported byte-for-byte from the previously verified Aurora
data in nixos-android-devices. The `android14/modem/` payloads were copied unchanged
from the factory `MODEM-FW.bin` and `NON-HLOS.bin` FAT images; `SOURCE.json`
records both image hashes, and the file sizes match the mounted partitions of
a handset running that base. No private partition dumps, handset MAC overrides,
radio calibration overrides, `persist` data, modem NV partitions or speaker
calibration are included.
The firmware and OEM support files are proprietary and retain their owners'
rights. [NOTICE](NOTICE) describes the boundary; [LICENSE](LICENSE) applies only
to repository-authored documentation and verification code.
