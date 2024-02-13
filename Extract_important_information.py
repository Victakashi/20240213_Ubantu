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


##'lscpu | grep "Architecture\|Model name\|CPU(s)"',  # Extract important information from lscpu command
##'lsusb | grep "Bus\|Device\|ID"',  # Extract important information from lsusb command
##'uname -a | grep "Linux"'  # Extract important information from uname -a command
##sudo dmidecode -t bios | grep "Vendor\|Version\|Release Date"

import subprocess

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    return output.decode('utf-8')

def main():
    commands = [
        'lscpu | grep "Architecture\|Model name\|CPU(s)"',  # Extract important information from lscpu command
        'lsusb | grep "Bus\|Device\|ID"',  # Extract important information from lsusb command
        'uname -a | grep "Linux"'  # Extract important information from uname -a command
    ]

    for command in commands:
        print(f"=== {command} ===")
        output = run_command(command)
        print(output.strip())  # Print the output of the command
        print("=" * 40)

if __name__ == "__main__":
    main()

print(__main__)
