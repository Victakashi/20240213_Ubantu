##Ubuntu 上安裝 git 並抓取程式碼
##安裝指令
##sudo apt-get install git
##建立目錄
##mkdir repo
##cd repo
##初始化目錄（產生 .git 檔案)
##sudo git init
##連線
##git clone https://github.com/Victakashi/20240213_Ubuntu.git



def get_commands():
    commands = [
        ('lscpu | grep "Architecture\|Model name\|CPU(s)"', "CPU information"),  # Extract important information from lscpu command
        ('lsusb | grep "Bus\|Device\|ID"', "USB information"),  # Extract important information from lsusb command
        ('uname -a | grep "Linux"', "Linux version information"),  # Extract important information from uname -a command
        ('sudo dmidecode -t bios | grep "Vendor\|Version\|Release Date"', "BIOS information")  # Extract important information from dmidecode command
    ]
    return commands
