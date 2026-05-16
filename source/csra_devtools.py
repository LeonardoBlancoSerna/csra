import os
import sys
import configparser

def addon_init():
    print("Iniciando nuevo complemento de CSRA...")
    name = input("Nombre del complemento: ")
    if not os.path.exists(name):
        os.makedirs(name)
        os.makedirs(os.path.join(name, "appModules"))
        os.makedirs(os.path.join(name, "globalPlugins"))
        os.makedirs(os.path.join(name, "doc"))
        print(f"Estructura creada en ./{name}")
    else:
        print("El directorio ya existe.")

def manifest_create():
    print("Asistente de creación de manifiesto CSRA")
    config = configparser.ConfigParser()
    config['addon'] = {
        'name': input("Nombre técnico (slug): "),
        'summary': input("Resumen: "),
        'description': input("Descripción larga: "),
        'author': input("Autor: "),
        'version': input("Versión (ej. 1.0): "),
        'url': input("URL: "),
        'minimumNVDAVersion': '2021.1',
        'lastTestedNVDAVersion': '2026.1'
    }
    with open('manifest.ini', 'w', encoding='utf-8') as f:
        config.write(f)
    print("manifest.ini creado con éxito.")

def addon_template(tipo):
    templates = {
        'appModules': 'import appModuleHandler\n\nclass AppModule(appModuleHandler.AppModule):\n\tpass',
        'globalPlugins': 'import globalPluginHandler\n\nclass GlobalPlugin(globalPluginHandler.GlobalPlugin):\n\tpass',
        'synthDrivers': 'from synthDriverHandler import SynthDriver\n\nclass SynthDriver(SynthDriver):\n\tpass',
        'brailleDisplayDrivers': 'from braille import BrailleDisplayDriver\n\nclass BrailleDisplayDriver(BrailleDisplayDriver):\n\tpass'
    }
    if tipo in templates:
        filename = f"{tipo}_template.py"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(templates[tipo])
        print(f"Plantilla para {tipo} creada en {filename}")
    else:
        print(f"Tipo desconocido: {tipo}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python csra_devtools.py [init|manifest|template <tipo>]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "init":
        addon_init()
    elif cmd == "manifest":
        manifest_create()
    elif cmd == "template":
        if len(sys.argv) > 2:
            addon_template(sys.argv[2])
        else:
            print("Especifique un tipo: appModules, globalPlugins, synthDrivers, brailleDisplayDrivers")
