import os
import subprocess
import pathlib
import gc

def Gitclone(URI: str, ClonePath: str = "") -> int:
    while True:
        i = subprocess.run(["git", "clone", URI, ClonePath] if ClonePath else ["git", "clone", URI])
        if i.returncode == 0:
            del i
            gc.collect()
            return 0
        else:
            del i

def DownLoad(URI: str, DownloadPath: str, DownLoadFileName: str) -> int:
    while True:
        i = subprocess.run(["aria2c", "-c", "-x", "16", "-s", "16", "-k", "1M", "-m", "0", "--enable-mmap=false",
                            "--console-log-level=error", "-d", DownloadPath, "-o", DownLoadFileName, URI])
        if i.returncode == 0:
            del i
            gc.collect()
            return 0
        else:
            del i

current_directory = pathlib.Path.cwd().resolve()
download_dir = current_directory / "CPU"
os.chdir(str(current_directory))

# Clonar repositorio stable-diffusion-webui
Gitclone("https://github.com/AUTOMATIC1111/stable-diffusion-webui.git", str(download_dir / "sdw"))
os.chdir(str(download_dir / "sdw"))
os.system("git reset --hard 89f9faa63388756314e8a1d96cf86bf5e0663045")

# Instalar extensiones
Gitclone(r"https://huggingface.co/embed/negative", str(download_dir / "sdw" / "embeddings" / "negative"))
Gitclone(r"https://huggingface.co/embed/lora", str(download_dir / "sdw" / "models" / "Lora" / "positive"))
Gitclone(r"https://github.com/Mikubill/sd-webui-controlnet", str(download_dir / "sdw" / "extensions" / "sd-webui-controlnet"))
DownLoad(r"https://huggingface.co/embed/upscale/resolve/main/4x-UltraSharp.pth", str(download_dir / "sdw" / "models" / "ESRGAN"), r"4x-UltraSharp.pth")
Gitclone(r"https://github.com/deforum-art/deforum-for-automatic1111-webui", str(download_dir / "sdw" / "extensions" / "deforum-for-automatic1111-webui"))

# Descargar scripts adicionales
while True:
    if subprocess.run(["wget", "https://raw.githubusercontent.com/camenduru/stable-diffusion-webui-scripts/main/run_n_times.py",
                       "-O", str(download_dir / "sdw" / "scripts" / "run_n_times.py")]).returncode == 0:
        break

# Cambiar al directorio principal de WebUI
os.chdir(download_dir / "sdw")

# Descargar modelos ControlNet
controlnet_models = [
    "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny_fp16.safetensors",
    "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_canny_fp16.yaml",
    "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/t2iadapter_canny_sd15v2.pth"
]

for model_url in controlnet_models:
    DownLoad(model_url, str(download_dir / "sdw" / "extensions" / "controlnet" / "models"),
             pathlib.Path(model_url).name)

# Descargar modelos principales
main_models = [
    "https://huggingface.co/dreamlike-art/dreamlike-photoreal-2.0/resolve/main/dreamlike-photoreal-2.0.safetensors",
    "https://huggingface.co/dreamlike-art/dreamlike-anime-1.0/resolve/main/dreamlike-anime-1.0.safetensors",
    "https://huggingface.co/dreamlike-art/dreamlike-diffusion-1.0/resolve/main/dreamlike-diffusion-1.0.safetensors",
    "https://huggingface.co/dreamlike-art/dreamlike-photoreal-1.0/resolve/main/dreamlike-photoreal-1.0.ckpt",
]

for model_url in main_models:
    DownLoad(model_url, str(download_dir / "sdw" / "models" / "Stable-diffusion"),
             pathlib.Path(model_url).name)

# Iniciar WebUI
os.chdir(download_dir / "sdw")
while True:
    ret = subprocess.run(["python3", "launch.py", "--precision", "full", "--no-half", "--no-half-vae",
                          "--enable-insecure-extension-access", "--medvram", "--share", "--skip-torch-cuda-test",
                          "--enable-console-prompts", "--ui-settings-file=" + str(
                              pathlib.Path(__file__).parent / "config.json")])
    if ret.returncode == 0:
        del ret
        gc.collect()
    else:
        del ret

# Limpiar variables al final del script
del os, current_directory, subprocess, pathlib, gc
