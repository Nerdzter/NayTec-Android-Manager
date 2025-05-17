import subprocess

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

    @staticmethod
    def get_cpu_usage():
        # Exemplo: pega a média de uso da CPU
        top_output = DeviceModel.run_adb_command("top -n 1 | grep %cpu")
        return top_output if top_output else "N/D"

    @staticmethod
    def get_ram_usage():
        meminfo = DeviceModel.run_adb_command("cat /proc/meminfo")
        return meminfo if meminfo else "N/D"

    @staticmethod
    def get_battery_level():
        return DeviceModel.run_adb_command("dumpsys battery | grep level")

    @staticmethod
    def get_storage_info():
        return DeviceModel.run_adb_command("df /data")
