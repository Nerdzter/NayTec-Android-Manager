import subprocess
import os
import re

class DeviceModel:

    @staticmethod
    def run_adb_command(cmd):
        try:
            result = subprocess.check_output(["adb", "shell"] + cmd.split(), encoding='utf-8')
            return result.strip()
        except subprocess.CalledProcessError:
            return "Erro"
        except FileNotFoundError:
            return "ADB não encontrado"

    @staticmethod
    def is_connected():
        try:
            output = subprocess.check_output(["adb", "get-state"], encoding='utf-8')
            return output.strip() == "device"
        except:
            return False

    @staticmethod
    def get_device_info():
        return {
            "device": DeviceModel.run_adb_command("getprop ro.product.device"),
            "model": DeviceModel.run_adb_command("getprop ro.product.model"),
            "android": DeviceModel.run_adb_command("getprop ro.build.version.release"),
        }

    # === CPU ===
    @staticmethod
    def get_cpu_human():
        output = DeviceModel.run_adb_command("top -n 1 | grep %cpu")
        match = re.search(r'(\d+)%\s*user', output)
        if match:
            return f"Uso atual: {match.group(1)}%"
        return "N/D"

    # === RAM ===
    @staticmethod
    def get_ram_human():
        output = DeviceModel.run_adb_command("cat /proc/meminfo")
        try:
            mem_total = int(re.search(r'MemTotal:\s+(\d+)', output).group(1)) // 1024
            mem_free = int(re.search(r'MemAvailable:\s+(\d+)', output).group(1)) // 1024
            mem_used = mem_total - mem_free
            return f"Usando {mem_used} MB de {mem_total} MB"
        except:
            return "N/D"

    # === BATERIA ===
    @staticmethod
    def get_battery_human():
        output = DeviceModel.run_adb_command("dumpsys battery")
        try:
            level = re.search(r'level: (\d+)', output).group(1)
            status = re.search(r'status: (\d+)', output).group(1)
            charging = " (carregando)" if status == "2" else ""
            return f"{level}%{charging}"
        except:
            return "N/D"

    # === ARMAZENAMENTO ===
    @staticmethod
    def get_storage_human():
        output = DeviceModel.run_adb_command("df /data")
        try:
            lines = output.splitlines()
            if len(lines) > 1:
                parts = lines[1].split()
                used = int(parts[2]) * 1024
                available = int(parts[3]) * 1024
                free_gb = round(available / (1024 ** 3), 1)
                total_gb = round((used + available) / (1024 ** 3), 1)
                return f"Disponível: {free_gb} GB de {total_gb} GB"
        except:
            return "N/D"

    # === SCREENSHOT ===
    @staticmethod
    def capture_screen(path="resources/icons/screen.png"):
        try:
            output = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])
            with open(path, "wb") as f:
                f.write(output)
            return path
        except Exception as e:
            print(f"Erro ao capturar tela: {e}")
            return None
