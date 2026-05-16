import ctypes
import os
from logHandler import log

class CSRAArtRust:
    _instance = None
    _lib = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CSRAArtRust, cls).__new__(cls)
            cls._instance._load_library()
        return cls._instance

    def _load_library(self):
        # En producción, GitHub Actions compilará esto a .dll
        # Aquí definimos la ruta donde se esperará el binario
        lib_path = os.path.join(os.path.dirname(__file__), "..", "csra_art_rust.dll")
        try:
            self._lib = ctypes.CDLL(lib_path)
            self._lib.art_initialize.restype = ctypes.c_int
            self._lib.art_terminate.restype = ctypes.c_int
            self._lib.art_connect.argtypes = [ctypes.c_char_p]
            self._lib.art_connect.restype = ctypes.c_int
            
            log.info("CSRA ART Rust Core library loaded successfully")
        except Exception as e:
            log.error(f"Could not load CSRA ART Rust library: {e}")
            self._lib = None

    def initialize(self):
        if self._lib:
            return self._lib.art_initialize()
        return -1

    def connect(self, address: str):
        if self._lib:
            return self._lib.art_connect(address.encode('utf-8'))
        return -1

    def terminate(self):
        if self._lib:
            return self._lib.art_terminate()
        return -1

# Singleton instance
rust_core = CSRAArtRust()
