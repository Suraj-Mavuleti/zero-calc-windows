# Zero Calc for Windows

![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-v1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An ultra-fast, precision-engineered calculator for professionals, featuring symbolic math and graphing capabilities.

This repository contains the highly optimized, native **Windows** build of Zero Calc. It is engineered from the ground up to utilize native Windows windowing and graphics APIs for zero-latency input and maximum performance, aiming to outperform industry standards.

## Features
- **Native Performance:** Written in Rust and C++ with bindings directly to Windows APIs.
- **Hardware Acceleration:** Zero-copy GPU rendering pipeline.
- **Enterprise Ready:** Full compatibility with industry-standard formats.

## Installation
Please download the latest release from the [Releases](../../releases) page, or build from source:

```bash
git clone https://github.com/Suraj-Mavuleti/zero-calc-windows.git
cd zero-calc-windows
build-windows.bat
```

## Architecture
This application leverages a multi-threaded architecture separated into a headless core and a native GUI frontend tailored specifically for Windows.

## License
MIT License.
