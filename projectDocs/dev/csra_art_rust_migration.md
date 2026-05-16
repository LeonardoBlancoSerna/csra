# CSRA ART: Access Remote Technology (Migration Plan to Rust)

This document outlines the architectural shift for the remote access layer of CSRA.

## 1. Objectives
- **Security:** Use Rust's memory safety to prevent RCE (Remote Code Execution) vulnerabilities.
- **Performance:** Low-latency audio transmission and fast file transfer.
- **Reliability:** Eliminate race conditions in multi-threaded network operations.

## 2. Core Components to Migrate
### A. Transport Layer (`source/_remoteClient/transport.py`)
- Transition from Python-based sockets to a high-performance Rust networking stack (using `tokio` or `quinn` for QUIC support).
- Implement bidirectional audio streaming using `cpal` or `rodio` for microphone input/output.

### B. Secure Desktop Bridging (`source/_remoteClient/secureDesktop.py`)
- Replace C++ IPC (Inter-Process Communication) with a safe Rust implementation.
- Rename IPC pipes and events to follow the `CSRA_ART_` naming convention.

### C. File Transfer Engine
- Implement a chunked, checksum-verified file transfer system in Rust.
- Add support for remote addon installation by handling `.nvda-addon` files directly in the controlled side's Rust core.

## 3. GitHub Actions Integration
The CI/CD pipeline has been updated to include the Rust toolchain:
- **Targets:** `i686-pc-windows-msvc` (32-bit) and `x86_64-pc-windows-msvc` (64-bit).
- **Optimization:** Automatic release builds for performance critical components.

## 4. Future Addon Terminal Commands
- `addon init`: Updated to support optional Rust module scaffolding.
- `addon template art-plugin`: Generates a Rust-based extension for the remote system.
