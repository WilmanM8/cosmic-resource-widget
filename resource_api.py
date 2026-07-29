import psutil
import subprocess
import shutil
import time
import glob
import os

# Inicializar CPU percent
psutil.cpu_percent(interval=None)

# Verificar si nvidia-smi está disponible en el sistema
HAS_NVIDIA_SMI = shutil.which("nvidia-smi") is not None
gpu_check_cooldown = 0.0
cached_gpu_stats = (0.0, 0.0)

# Autodetección de rutas de GPU AMD/Intel mediante sysfs (sin subprocesos, súper rápido)
AMD_BUSY_PATH = None
AMD_TEMP_PATH = None

for card_path in glob.glob("/sys/class/drm/card*/device"):
    busy_file = os.path.join(card_path, "gpu_busy_percent")
    if os.path.exists(busy_file):
        AMD_BUSY_PATH = busy_file
    
    # Buscar sensores de temperatura en hwmon
    for hwmon_path in glob.glob(os.path.join(card_path, "hwmon", "hwmon*")):
        temp_file = os.path.join(hwmon_path, "temp1_input")
        if os.path.exists(temp_file):
            name_file = os.path.join(hwmon_path, "name")
            if os.path.exists(name_file):
                try:
                    with open(name_file, "r") as nf:
                        driver_name = nf.read().strip()
                        if driver_name == "amdgpu":
                            AMD_TEMP_PATH = temp_file
                            # Priorizar busy_percent de la tarjeta AMDGPU
                            if os.path.exists(os.path.join(card_path, "gpu_busy_percent")):
                                AMD_BUSY_PATH = os.path.join(card_path, "gpu_busy_percent")
                            break
                except Exception:
                    pass
            if not AMD_TEMP_PATH:
                AMD_TEMP_PATH = temp_file

def get_gpu_stats():
    """Obtiene uso y temperatura de la GPU dedicada (NVIDIA, AMD o Intel)"""
    global gpu_check_cooldown, cached_gpu_stats
    
    # 1. Intentar NVIDIA si está disponible
    if HAS_NVIDIA_SMI:
        current_time = time.time()
        if current_time >= gpu_check_cooldown:
            try:
                output = subprocess.check_output(
                    ["nvidia-smi", "--query-gpu=utilization.gpu,temperature.gpu",
                     "--format=csv,noheader,nounits"],
                    stderr=subprocess.DEVNULL,
                    text=True
                )
                parts = output.strip().split(',')
                cached_gpu_stats = (float(parts[0].strip()), float(parts[1].strip()))
                return cached_gpu_stats
            except Exception:
                # Cooldown de 10 segundos ante fallos de nvidia-smi
                gpu_check_cooldown = current_time + 10.0
                cached_gpu_stats = (0.0, 0.0)

    # 2. Fallback a AMD/Intel mediante sysfs directo (cero overhead de subprocesos)
    if AMD_BUSY_PATH or AMD_TEMP_PATH:
        busy = 0.0
        temp = 0.0
        if AMD_BUSY_PATH:
            try:
                with open(AMD_BUSY_PATH, "r") as f:
                    busy = float(f.read().strip())
            except Exception:
                pass
        if AMD_TEMP_PATH:
            try:
                with open(AMD_TEMP_PATH, "r") as f:
                    temp = float(f.read().strip()) / 1000.0
            except Exception:
                pass
        return busy, temp
        
    # 3. Retornar último cache / valor seguro
    return cached_gpu_stats

def get_cpu_temp():
    """Obtiene la temperatura del CPU"""
    try:
        temps = psutil.sensors_temperatures()
        # Buscar en diferentes fuentes comunes
        for key in ['k10temp', 'coretemp', 'zenpower', 'cpu_thermal', 'acpitz']:
            if key in temps and temps[key]:
                return temps[key][0].current
        # Si no encuentra ninguna conocida, tomar la primera disponible
        for key in temps:
            if temps[key]:
                return temps[key][0].current
    except Exception:
        pass
    return 0.0

def get_system_stats():
    """Obtiene métricas rápidas y no bloqueantes del sistema"""
    gpu_percent, gpu_temp = get_gpu_stats()
    return {
        'cpu': psutil.cpu_percent(interval=None),
        'cpu_temp': get_cpu_temp(),
        'ram': psutil.virtual_memory().percent,
        'ram_used_gb': round(psutil.virtual_memory().used / (1024**3), 1),
        'ram_total_gb': round(psutil.virtual_memory().total / (1024**3), 1),
        'gpu': gpu_percent,
        'gpu_temp': gpu_temp
    }
