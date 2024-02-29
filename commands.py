##Ubuntu 上安裝 git 並抓取程式碼
##安裝指令
##sudo apt-get install git
##建立目錄
##mkdir repo
##cd repo
##初始化目錄（產生 .git 檔案)
##sudo git init
##連線
##sudo git clone https://github.com/Victakashi/20240213_Ubuntu.git
##sudo rm -rf 20240213_Ubuntu && sudo git clone https://github.com/Victakashi/20240213_Ubuntu.git
##tegrastats Utility NVIDIA 溫度監控command.
##https://docs.nvidia.com/drive/drive_os_5.1.6.1L/nvvib_docs/index.html#page/DRIVE_OS_Linux_SDK_Development_Guide/Utilities/util_tegrastats.html
##可以讀取一次的寫法
##< tegrastats --stop && tegrastats --interval 6000  & sleep 10 && tegrastats --stop && tegrastats --stop>



def get_commands():
    commands = [
        ('lscpu | grep "Architecture\|Model name\|CPU(s)"', "CPU information"),  # Extract important information from lscpu command
        ('lsusb | grep "Bus\|Device\|ID"', "USB information"),  # Extract important information from lsusb command
        #('uname -a | grep "Linux"', "Linux version information"),  # Extract important information from uname -a command
        ('lsb_release -a | grep -E "Description ID|Distributor|Release"', "Linux version information"),  # Extract important information from uname -a command
        ('nvcc --version', "NVIDIA CUDA Version information")
        ('sudo dmidecode -t bios | grep "Vendor\|Version\|Release Date"', "BIOS information")  # Extract important information from dmidecode command
         ##要解一下 輸出問題 NVIDIA CUDA BIOS information 有衝突??
    ]
    return commands

def get_remote_host_info():
    # Remote host information
    hostname = 'remote_host_ip'
    username = 'your_username'
    password = 'your_password'
    return hostname, username, password

