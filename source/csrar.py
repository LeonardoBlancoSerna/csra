import struct
import speech
import keyboardHandler
import inputCore
import api
import controlTypes
from logHandler import log
import os

SECRET_KEY = b"CSRA_PROGETH_2026"

# Identificadores de instrucciones
OP_SPEAK = 0x01
OP_PLAY_SOUND = 0x02
OP_BIND_KEY = 0x04
OP_GET_FOCUS_PROP = 0x05
OP_SHOW_UI = 0x06
OP_SET_CONFIG = 0x07
OP_ON_STARTUP = 0x08
OP_END = 0xFF

class CSRARuntime:
    def __init__(self):
        self.opcodes = {
            0x01: self.handle_speak,
            0x02: self.handle_play_sound,
            0x05: self.handle_get_focus_prop,
            0x06: self.handle_show_ui,
            0x07: self.handle_set_config,
        }
        self.stack = []
        self.config = {}

    def handle_show_ui(self, data, offset):
        length = struct.unpack("I", data[offset:offset+4])[0]
        offset += 4
        ui_path = data[offset:offset+length].decode('utf-8')
        # Aquí se integraría con el motor de UI de CSRA
        log.info(f"CSRA-L: Cargando interfaz visual desde {ui_path}")
        return offset + length

    def handle_set_config(self, data, offset):
        key_len = struct.unpack("I", data[offset:offset+4])[0]
        offset += 4
        key = data[offset:offset+key_len].decode('utf-8')
        offset += key_len
        
        val_len = struct.unpack("I", data[offset:offset+4])[0]
        offset += 4
        val = data[offset:offset+val_len].decode('utf-8')
        
        self.config[key] = val
        log.info(f"CSRA-L: Configuración guardada - {key} es {val}")
        return offset + val_len

    def execute_bytecode(self, data):
        offset = 0
        while offset < len(data):
            opcode = data[offset]
            offset += 1
            if opcode == 0xFF: break
            if opcode in self.opcodes:
                offset = self.opcodes[opcode](data, offset)
            else:
                break

    def run(self, filename):
        if not os.path.exists(filename): return

        with open(filename, "rb") as f:
            header = f.read(4)
            if header != b"CSRX": return
            version = struct.unpack("B", f.read(1))[0]
            encrypted_data = f.read()
            data = self._decrypt(encrypted_data)
            
            offset = 0
            while offset < len(data):
                opcode = data[offset]
                offset += 1
                if opcode == 0xFF: break
                
                if opcode == 0x08: # ON_STARTUP
                    bc_len = struct.unpack("I", data[offset:offset+4])[0]
                    offset += 4
                    startup_bc = data[offset:offset+bc_len]
                    offset += bc_len
                    # Ejecutar inmediatamente al cargar el archivo
                    self.execute_bytecode(startup_bc)

                elif opcode == 0x04: # OP_BIND_KEY
                    # ... (lógica de teclas se mantiene igual)

    def _decrypt(self, data):
        return bytearray([b ^ SECRET_KEY[i % len(SECRET_KEY)] for i, b in enumerate(data)])

    def handle_speak(self, data, offset):
        # Si hay algo en la pila (como el nombre de un objeto), lo hablamos
        if self.stack:
            text = self.stack.pop()
            speech.speakText(str(text))
            return offset
        
        # Si no, leemos el texto directamente del bytecode
        length = struct.unpack("I", data[offset:offset+4])[0]
        offset += 4
        text = data[offset:offset+length].decode('utf-8')
        speech.speakText(text)
        return offset + length

    def handle_get_focus_prop(self, data, offset):
        prop_id = data[offset]
        offset += 1
        obj = api.getFocusObject()
        
        if not obj:
            self.stack.append("No hay objeto enfocado")
            return offset
            
        if prop_id == PROP_NAME:
            self.stack.append(obj.name or "Sin nombre")
        elif prop_id == PROP_ROLE:
            self.stack.append(controlTypes.roleToName(obj.role))
        elif prop_id == PROP_VALUE:
            self.stack.append(obj.value or "Sin valor")
            
        return offset

    def handle_play_sound(self, data, offset):
        length = struct.unpack("I", data[offset:offset+4])[0]
        offset += 4
        sound = data[offset:offset+length].decode('utf-8')
        log.info(f"CSRA-L: Reproduciendo {sound}")
        return offset + length

    def execute_bytecode(self, data):
        offset = 0
        while offset < len(data):
            opcode = data[offset]
            offset += 1
            if opcode == 0xFF: 
                break
            if opcode in self.opcodes:
                offset = self.opcodes[opcode](data, offset)
            else:
                break

    def run(self, filename):
        if not os.path.exists(filename): 
            return

        with open(filename, "rb") as f:
            header = f.read(4)
            if header != b"CSRX": 
                return
            version = struct.unpack("B", f.read(1))[0]
            encrypted_data = f.read()
            data = self._decrypt(encrypted_data)
            
            offset = 0
            while offset < len(data):
                opcode = data[offset]
                offset += 1
                if opcode == 0xFF: 
                    break
                
                if opcode == 0x04: # Enlace de tecla (OP_BIND_KEY)
                    key_len = struct.unpack("I", data[offset:offset+4])[0]
                    offset += 4
                    key_name = data[offset:offset+key_len].decode('utf-8')
                    offset += key_name
                    
                    bc_len = struct.unpack("I", data[offset:offset+4])[0]
                    offset += 4
                    block_bc = data[offset:offset+bc_len]
                    offset += bc_len
                    
                    self.register_key(key_name, block_bc)
                else:
                    if opcode in self.opcodes:
                        offset = self.opcodes[opcode](data, offset)

    def register_key(self, key_name, bytecode):
        try:
            gesture = keyboardHandler.KeyboardInputGesture.fromName(key_name)
            def script_handler(gesture):
                self.execute_bytecode(bytecode)
            
            inputCore.manager.userGestureMap.add(str(gesture), f"csral_{key_name}")
            import globalCommands
            setattr(globalCommands.GlobalCommands, f"script_csral_{key_name}", script_handler)
            log.info(f"CSRA-L: Tecla registrada")
        except Exception as e:
            log.error(f"Error en CSRA-L: {e}")

if __name__ == "__main__":
    runtime = CSRARuntime()
    if os.path.exists("test.csrax"):
        runtime.run("test.csrax")
