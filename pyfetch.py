import platform
import time
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

#Turn the time into hours and minutes 
def format_uptime(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{int(hours)} hours, {int(minutes)} mins"

# Part code is by "Lorago", Taken from Vfetch project https://github.com/Lorago/vfetch/blob/master/vfetch.py 
# thank you for this awesome project <3
def getPackages(display_package_manager=False, based_on=''):
    try:
        # Run the "pacman -Qq" command for arch based systems
        if based_on.lower() == 'arch':
            result = subprocess.run(['pacman', '-Qq'], stdout=subprocess.PIPE, text=True)
            package_manager_suffix = ' (pacman)'
        # Run the "dpkg -l" command for debian based systems
        elif based_on.lower() == 'debian':
            result = subprocess.run(['dpkg', '-l'], stdout=subprocess.PIPE, text=True)
            package_manager_suffix = ' (deb)'
        else:
            raise ValueError("Unsupported package manager")

        output = result.stdout.strip()

        package_count = len(output.split('\n'))
        if display_package_manager:
            package_count_string = f"{package_count}{package_manager_suffix}"
        else:
            package_count_string = str(package_count)

        return package_count_string

    except Exception as e:
        print(f"Error getting packages: {e}")
        return None

#gets the cpu by running "lscpu" command and only taking the "Model name" part
def get_cpu_model():
    try:
        command = "lscpu"
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if "Model name:" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        print(f"Error getting CPU model: {e}")
    return None

#gets the gpu by running "lspci | grep VGA" command and only taking the "Model name" part
def get_gpu_info():
    try:
        command = "lspci | grep VGA"
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
        gpu_info = result.stdout.strip()
        gpu_model = gpu_info.split('VGA compatible controller: ')[1].split(' (rev')[0].strip()
        return gpu_model
    except Exception as e:
        print(f"Error getting GPU information: {e}")
    return None

#gets how many ram it is using by running "free -h" command 
def get_ram_info():
    try:
        command = "free -h"
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if line.startswith("Mem:"):
                total, used, free = line.split()[1], line.split()[2], line.split()[3]
                return f"{used}/{total}"
    except Exception as e:
        print(f"Error getting RAM information: {e}")
    return None

#getting the monitor resolution using xrandar 
#NOTE: it won't work on wayland, comment the resolution printing line or feel free to add your function for wayland
def get_monitor_resolution(): 
    try:
        command = "xrandr | grep '*'"
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
        resolution_line = result.stdout.split('\n')[0]
        resolution = resolution_line.split()[0]
        return resolution
    except Exception as e:
        print(f"Error getting monitor resolution: {e}")
    return None

linux_info = platform.freedesktop_os_release()
linux_name = linux_info.get('NAME', 'Unknown')
based_on = linux_info.get('ID_LIKE', 'Unknown')
kernel = platform.uname().release

uptime_seconds = time.monotonic()
formatted_uptime = format_uptime(uptime_seconds)

#----------------------------------------------------------------------
#comment anything you don't want to use by adding "#"
print(f"{Fore.RED}{Style.BRIGHT}╭───── System {Style.RESET_ALL}:")
print(f"{Fore.RED}{Style.BRIGHT}├ OS{Style.RESET_ALL}: {linux_name}")
print(f"{Fore.RED}{Style.BRIGHT}├ Based On{Style.RESET_ALL}: {based_on}")
print(f"{Fore.RED}{Style.BRIGHT}├ Packages{Style.RESET_ALL}: {getPackages(display_package_manager=True, based_on=based_on)}")
print(f"{Fore.RED}{Style.BRIGHT}├ Kernel{Style.RESET_ALL}: {kernel}")
print(f"{Fore.RED}{Style.BRIGHT}╰─ Uptime{Style.RESET_ALL}: {formatted_uptime}")
print("")
print(f"{Fore.RED}{Style.BRIGHT}╭───── Hardware {Style.RESET_ALL}:")
print(f"{Fore.RED}{Style.BRIGHT}├ CPU: {Style.RESET_ALL}: {get_cpu_model()}")
print(f"{Fore.RED}{Style.BRIGHT}├ GPU: {Style.RESET_ALL}: {get_gpu_info()}")
print(f"{Fore.RED}{Style.BRIGHT}├ RAM: {Style.RESET_ALL}: {get_ram_info()}")
print(f"{Fore.RED}{Style.BRIGHT}╰ Resolution: {Style.RESET_ALL}: {get_monitor_resolution()}")
#----------------------------------------------------------------------
