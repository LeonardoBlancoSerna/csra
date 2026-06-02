import struct
import re
import os

# Definición de OpCodes (Identificadores de instrucciones)
OP_SPEAK = 0x01
OP_PLAY_SOUND = 0x02
OP_BIND_KEY = 0x04
OP_GET_FOCUS_PROP = 0x05
OP_SHOW_UI = 0x06
OP_SET_CONFIG = 0x07
OP_ON_STARTUP = 0x08
OP_END = 0xFF

# IDs de Propiedades
PROP_NAME = 0x10
PROP_ROLE = 0x11
PROP_VALUE = 0x12

SECRET_KEY = b"CSRA_PROGETH_2026"

class CSRACCompiler:
    def __init__(self):
        self.metadata = {}
        self.scripts = {}
        self.startup_bc = bytearray()

    def _encrypt(self, data):
        return bytearray([b ^ SECRET_KEY[i % len(SECRET_KEY)] for i, b in enumerate(data)])

    def compile_block(self, lines):
        block_bc = bytearray()
        for line in lines:
            line = line.strip()
            
            if line.startswith('show_ui "'):
                path = re.findall(r'"([^"]*)"', line)[0]
                block_bc.append(OP_SHOW_UI)
                path_bytes = path.encode('utf-8')
                block_bc.extend(struct.pack("I", len(path_bytes)))
                block_bc.extend(path_bytes)

            elif line.startswith('set_config'):
                match = re.search(r'set_config\s+(\w+)\s*=\s*"([^"]*)"', line)
                if match:
                    key, val = match.groups()
                    block_bc.append(OP_SET_CONFIG)
                    key_bytes = key.encode('utf-8')
                    block_bc.extend(struct.pack("I", len(key_bytes)))
                    block_bc.extend(key_bytes)
                    val_bytes = val.encode('utf-8')
                    block_bc.extend(struct.pack("I", len(val_bytes)))
                    block_bc.extend(val_bytes)

            elif line.startswith('speak '):
                if 'f"' in line:
                    if "focus.name" in line:
                        block_bc.append(OP_GET_FOCUS_PROP)
                        block_bc.append(PROP_NAME)
                    elif "focus.role" in line:
                        block_bc.append(OP_GET_FOCUS_PROP)
                        block_bc.append(PROP_ROLE)
                    elif "focus.value" in line:
                        block_bc.append(OP_GET_FOCUS_PROP)
                        block_bc.append(PROP_VALUE)
                    block_bc.append(OP_SPEAK)
                elif '"' in line:
                    text = re.findall(r'"([^"]*)"', line)[0]
                    block_bc.append(OP_SPEAK)
                    text_bytes = text.encode('utf-8')
                    block_bc.extend(struct.pack("I", len(text_bytes)))
                    block_bc.extend(text_bytes)
            
            elif line.startswith('play_sound "'):
                sound = re.findall(r'"([^"]*)"', line)[0]
                block_bc.append(OP_PLAY_SOUND)
                sound_bytes = sound.encode('utf-8')
                block_bc.extend(struct.pack("I", len(sound_bytes)))
                block_bc.extend(sound_bytes)
                
        return block_bc

    def compile(self, source_code):
        lines = source_code.splitlines()
        current_block = []
        current_key = None
        is_startup = False
        main_bytecode = bytearray()

        for line in lines:
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            line = stripped

            if not line or line.startswith("#"):
                continue

            if line.startswith("on startup:"):
                is_startup = True
                current_block = []
                continue

            if line.startswith("on key") and line.endswith(":"):
                current_key = re.findall(r'"([^"]*)"', line)[0]
                current_block = []
                continue

            if (current_key or is_startup) and indent > 0:
                current_block.append(line)
                continue
            
            if indent == 0:
                if is_startup:
                    self.startup_bc = self.compile_block(current_block)
                    is_startup = False
                elif current_key:
                    self.scripts[current_key] = self.compile_block(current_block)
                    current_key = None

            if ":" in line and not line.startswith("on"):
                key, val = line.split(":", 1)
                self.metadata[key.strip()] = val.strip().strip('"')

        if is_startup:
            self.startup_bc = self.compile_block(current_block)
        elif current_key:
            self.scripts[current_key] = self.compile_block(current_block)

        # Empaquetar el bloque de inicio
        if self.startup_bc:
            main_bytecode.append(OP_ON_STARTUP)
            main_bytecode.extend(struct.pack("I", len(self.startup_bc)))
            main_bytecode.extend(self.startup_bc)

        for key, bc in self.scripts.items():
            main_bytecode.append(OP_BIND_KEY)
            key_bytes = key.encode('utf-8')
            main_bytecode.extend(struct.pack("I", len(key_bytes)))
            main_bytecode.extend(key_bytes)
            main_bytecode.extend(struct.pack("I", len(bc)))
            main_bytecode.extend(bc)

        main_bytecode.append(OP_END)
        return self._encrypt(main_bytecode)

    def save(self, filename, encrypted_bc):
        with open(filename, "wb") as f:
            f.write(b"CSRX")
            f.write(struct.pack("B", 3))
            f.write(encrypted_bc)
