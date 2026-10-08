# Touch host processing data

Unchanged files from OS1.0.3.0.UNACNXM:

| File | Stock path |
| --- | --- |
| `libtouchreport.so` | `/odm/lib64/libtouchreport.so` |
| `aurora_syna_thp_config.ini` | `/odm/firmware/aurora_syna_thp_config.ini` |

The library contains AArch64 userspace processing for raw touch reports; it is
not a firmware image to flash onto the controller. Use it with the matching
Aurora host adapter and config. Do not substitute another device or ROM's library:
the adapter validates the exact binary and depends on its layout and interface.
The adapter source and its licensing remain in nixos-android-devices.
