# Speaker DSP data

Unmodified files from OS1.0.3.0.UNACNXM `/odm/firmware/`. The OEM CS35L43 driver
selected the `-tt` product coefficients for both top (T) and bottom (B) amplifiers.
The shared WMFW payload and the paired coefficient files must be used together.

These coefficients are product tuning, not individual speaker calibration.
Keep `persist/audio/crus_calr.*` and its per-handset CAL_R_SEL values outside this
repository. The Linux consumer applies the handset's calibration before enabling
output. Its driver/UCM and acoustic validation are separate from file integrity.
