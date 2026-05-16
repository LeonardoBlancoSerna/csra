import os
import shutil

source_root = r"C:\Users\USUARIO\Desktop\proyectos\repositorios\CSRA\source"
csra_code_files = os.path.join(source_root, "CSRA-code-files")
csra_files_txt = os.path.join(source_root, "csra_files.txt")

# Try to read with utf-16 if it has BOM, otherwise utf-8
try:
    with open(csra_files_txt, "rb") as f:
        raw = f.read()
        if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
            content = raw.decode('utf-16')
        else:
            content = raw.decode('utf-8-sig')
    files_to_find = [line.strip() for line in content.splitlines() if line.strip()]
except Exception as e:
    # Fallback
    with open(csra_files_txt, "r", encoding='latin-1') as f:
        files_to_find = [line.strip().replace('\x00', '') for line in f if line.strip()]

# Mapping of filename to list of full paths in CSRA-code-files
mapping = {}
for root, dirs, files in os.walk(csra_code_files):
    for file in files:
        if file in files_to_find:
            if file not in mapping:
                mapping[file] = []
            mapping[file].append(os.path.join(root, file))

utilities_path = os.path.join(csra_code_files, "NVDAExtensionGlobalPlugin", "utilities")

report = []

for filename in files_to_find:
    # Remove any lingering BOM or nulls just in case
    clean_name = filename.encode('ascii', 'ignore').decode('ascii').strip()
    if not clean_name: continue
    
    if clean_name not in mapping:
        # Try finding without case sensitivity?
        found_case = False
        for m_name in mapping:
            if m_name.lower() == clean_name.lower():
                clean_name = m_name
                found_case = True
                break
        if not found_case:
            report.append(f"NOT FOUND: {clean_name}")
            continue
    
    paths = mapping[clean_name]
    
    target_root = os.path.join(source_root, clean_name)
    target_appmodules = os.path.join(source_root, "appModules", clean_name)
    target_globalplugins = os.path.join(source_root, "globalPlugins", clean_name)
    
    exists_in_root = os.path.exists(target_root)
    exists_in_appmodules = os.path.exists(target_appmodules)
    exists_in_globalplugins = os.path.exists(target_globalplugins)
    
    if exists_in_root or exists_in_appmodules or exists_in_globalplugins:
        # Check if identical (optional, but requested "don't overwrite if identical")
        # For now, just skip if exists as per instruction "if they are not already..."
        report.append(f"ALREADY EXISTS: {clean_name}")
        continue

    utility_paths = [p for p in paths if utilities_path in p]
    
    if utility_paths:
        path = utility_paths[0]
        shutil.copy2(path, source_root)
        report.append(f"COPIED TO ROOT: {clean_name} (from {path})")
    else:
        path = paths[0]
        if "appModules" in path:
            dest = os.path.join(source_root, "appModules")
            if not os.path.exists(dest): os.makedirs(dest)
            shutil.copy2(path, dest)
            report.append(f"COPIED TO appModules: {clean_name} (from {path})")
        elif "globalPlugins" in path:
            dest = os.path.join(source_root, "globalPlugins")
            if not os.path.exists(dest): os.makedirs(dest)
            shutil.copy2(path, dest)
            report.append(f"COPIED TO globalPlugins: {clean_name} (from {path})")
        else:
            shutil.copy2(path, source_root)
            report.append(f"COPIED TO ROOT: {clean_name} (from {path})")

with open(os.path.join(source_root, "copy_report.txt"), "w", encoding='utf-8') as f:
    f.write("\n".join(report))
