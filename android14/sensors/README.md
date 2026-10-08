# Sensor support data

Source: OS1.0.3.0.UNACNXM, runtime V816.0.3.0.UNACNXM. These 68 OEM configuration
files and 10 Hexagon DSP files match the ADSP firmware in the parent release.
`SOURCE.json` records their original Android paths; `SHA256SUMS` records the bytes.

Configuration selection follows `/odm/etc/sensors/config/json.lst` for MTP /
SoC 557. Three listed secondary SAR files absent from the ROM are omitted:
`sm8650_sx937x_1.json`, `sx937x_1.json`, `sx937x_reg_1.json`. The duplicate
vendor/ODM CHRE configs differ in platform selectors; the selected sensor values
match and the ODM copy is retained.

Linux generates a file-group SSC registry and exposes the selected config list
under the firmware's expected `/odm/etc/sensors` view. No generated registry,
Android daemon or handset-specific writable calibration is distributed here.
The LSM6DSO OEM orientation is (+Y, +X, -Z); consumers must not add an unrelated
board's mounting matrix to the resulting Android device coordinates.
