// CSRA: nvdaHelper replacement in Rust
// Focus on safe system utilities and hooks

use windows::Win32::Foundation::*;
use windows::Win32::System::Threading::*;

#[no_mangle]
pub extern "C" fn csra_helper_get_process_id() -> u32 {
    unsafe { GetCurrentProcessId() }
}

#[no_mangle]
pub extern "C" fn csra_helper_is_64bit_process(process_handle: HANDLE) -> bool {
    let mut is_wow64 = BOOL(0);
    unsafe {
        if IsWow64Process(process_handle, &mut is_wow64).is_ok() {
            !is_wow64.as_bool()
        } else {
            false
        }
    }
}

// Futuras implementaciones de Virtual Buffers y Hooks en Rust...
