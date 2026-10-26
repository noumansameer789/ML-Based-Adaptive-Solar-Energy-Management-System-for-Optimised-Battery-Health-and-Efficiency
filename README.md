# Solar battery management original project archive

BS Electrical Engineering final-year project, September 2024–June 2025, team of three. This archive preserves the prototype firmware, model-development scripts and hardware photographs. The [cleaned portfolio](https://github.com/noumansameer789/solar-battery-ml-controller) contains a smaller control-policy example with tests.

## Evidence available

- [ESP32 telemetry firmware](FYP/New%20folder/esp32_codev2/esp32_codev2.ino)
- [State-of-charge circuit sketch](FYP/soc%20circuit/1/1.ino)
- [Forecast development scripts](FYP/Weather-forecast-model/Battery%20optimization)
- [Hardware photographs](FYP/Hardware%20imgs)
- [Prototype photographs](FYP/Hardware%20imgs/Prototype)

The inspected ESP32 firmware uses **ThingSpeak**. The previous Firebase reference was unsupported and has been removed. Trained `.pkl` weights are not committed, so this archive is not a one-command model reproduction. Some data and figure entries are Git LFS pointers and require the associated LFS objects; their presence in the tree does not guarantee downloadable bytes.

## Reported project results

| Measure | Original reported result |
| --- | --- |
| NASA rows after cleaning | 22,943 from more than 26,000 |
| XGBoost chronological holdout R² | 0.970 |
| Random Forest holdout R² | 0.956 |
| Sunny/cloudy classification accuracy | 96.4% using the original threshold |
| Battery prototype | battery pack |

These figures are reported project results and have not been rerun during this archive cleanup. No quantified extension of battery life, charging-efficiency improvement or commercial readiness is established. The scripts retain their historical versions; do not assume each uses the same split as the reported evaluation.

## Reuse and hardware limits

The firmware needs review of calibration, wiring, protective hardware and test conditions before use. Do not use a software thermal cut-off as a substitute for an independent, suitable BMS. Credentials belong in local configuration and must not be committed.

All rights reserved on this original team-project archive. Existing ownership and third-party rights are unchanged.

## Hardware gallery

[View web-compatible hardware photographs](docs/hardware-gallery/README.md). Original HEIC files are retained alongside these JPEG viewing copies.

## Battery specification verification

Project descriptions conflict on the parallel-cell count (3S3P versus 3S9P). The available photograph does not independently establish the claimed 23.4 Ah pack capacity. The exact topology and capacity are therefore not presented as verified specifications. Confirm the wiring, cell ratings and measured capacity before reusing those figures. No battery-life or capacity-test result is implied by this archive.
