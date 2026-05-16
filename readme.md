# CSRA: Comentary Screen Reader and Accessibility

**CSRA** is a free, open-source, high-performance screen reader for Microsoft Windows, built on the foundations of NVDA but engineered for the next generation of accessibility and professional production.

---

## 📜 History and Vision

**CSRA** was born from the need to break the "duopoly" of JAWS and NVDA in the Windows ecosystem. While based on NVDA's core, CSRA integrates powerful features and enhancements that were previously rejected or unplanned by the original project. It is the perfect alternative for developers and users who demand a more robust, flexible, and feature-rich accessibility platform.

### Key Milestones:
*   **Integrated Power:** Native inclusion of essential add-ons (LBL, Unigram Plus, SIBIAC OCR, Tony's Enhancements) out of the box.
*   **Professional Audio Focus:** Deep integration for DAWs (Reaper) and VST instruments (Kontakt, EZDrummer), making it the gold standard for blind musicians and producers.
*   **CSRA ART (Access Remote Technology):** A completely rebranded and evolved remote access system, currently being migrated to Rust for unparalleled security and low-latency audio/file transmission.

---

## 🚀 Technical Innovations

### 🦀 The Rust Revolution
CSRA is leading the industry by migrating critical low-level components from C++ to **Rust**.
- **Memory Safety:** Eliminating crashes and vulnerabilities in networking and system hooks.
- **Performance:** Leveraging Rust's speed for real-time audio and high-speed data transfer in CSRA ART.
- **Hybrid Architecture:** A cutting-edge blend of Python (Logic/UI), Rust (Security/Performance), and C++ (Legacy Support).

### 🎙️ ProAcces TTS
We are moving away from eSpeakNG towards **ProAcces**, a Python-based synthesis engine designed for easier updates and superior integration, delivered as a high-performance compiled submodule.

### 🛠️ Developer Suite (CSRA DevTools)
CSRA includes a built-in terminal suite to standardize development:
- `addon init`: Bootstrap new projects instantly.
- `manifest create`: Interactive assistant for manifest generation.
- `addon <type>`: Ready-to-use templates for `appModules`, `globalPlugins`, `synthDrivers`, and more.

---

## 📂 Structural Integrity

Unlike standard NVDA, CSRA maintains a strictly organized source tree:
- **`source/waves/`**: All audio assets are organized into subdirectories by component.
- **`source/psutil`, `source/markdown`, etc.**: Clean library packaging instead of root-level clutter.
- **`source/CSRA-code-files/`**: A central library of integrated components for easy maintenance.

---

## 🤝 Contributing

We welcome developers who want to push the boundaries of what a screen reader can do. Check out our `CONTRIBUTING.md` and explore the `nvda_helper_rust` and `csra_art_rust` directories to see the future in action.

---

## ⚖️ License and Copyright

&copy; NV Access 2009-2026  
&copy; CSRA Progeth 2026

*CSRA is covered by the GNU General Public License (GPL). See the file COPYING for more details.*
