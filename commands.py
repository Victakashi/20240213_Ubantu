

def get_commands():
    commands = [
        ('lscpu | grep "Architecture\|Model name\|CPU(s)"', "CPU information"),  # Extract important information from lscpu command
        ('lsusb | grep "Bus\|Device\|ID"', "USB information"),  # Extract important information from lsusb command
        #('uname -a | grep "Linux"', "Linux version information"),  # Extract important information from uname -a command
        ('lsb_release -a | grep -E "Description ID|Distributor|Release"', "Linux version information"),  # Extract important information from uname -a command
        #('nvcc --version', "NVIDIA CUDA Version information")
        #('sudo dmidecode -t bios | grep "Vendor\|Version\|Release Date"', "BIOS information")  # Extract important information from dmidecode command
         ##要解一下 輸出問題 NVIDIA CUDA BIOS information 有衝突??
    ]
    return commands

def get_remote_host_info():
    # Remote host information
    hostname = 'remote_host_ip'
    username = 'your_username'
    password = 'your_password'
    return hostname, username, password

