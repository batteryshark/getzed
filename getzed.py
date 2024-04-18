import subprocess
import sys
import os
import requests

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        sys.exit(1)

def download_file(url, filename):
    print(f"Downloading {filename}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename} successfully.")

def install_rustup():
    rustup_init_path = "rustup-init.exe"
    rustup_url = "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe"
    download_file(rustup_url, rustup_init_path)
    print("Installing Rust and rustup...")
    run_command([rustup_init_path, "-y", "--default-host", "x86_64-pc-windows-msvc", "--default-toolchain", "stable", "--profile", "default"])
    os.remove(rustup_init_path)
    print("Rust and rustup installed successfully.")

def check_and_install_rust():
    print("Checking if Rust is installed...")
    result = subprocess.run("rustup --version", capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print("rustup is not installed.")
        install_rustup()
    else:
        print("Rust is already installed.")

    print("Updating Rust...")
    run_command("rustup update")
    print("Adding wasm32-wasi target...")
    run_command("rustup target add wasm32-wasi")

def clone_repository():
    repo_url = "https://github.com/zed-industries/zed"
    print("Cloning the repository...")
    run_command(f"git clone {repo_url}")
    os.chdir("zed")
    print("Initializing submodules...")
    run_command("git submodule update --init --recursive")

def compile_zed():
    print("Building ZED...")
    run_command("cargo run --release")

def main():
    check_and_install_rust()
    clone_repository()
    compile_zed()
    print("ZED has been successfully built and compiled.")

if __name__ == "__main__":
    main()
