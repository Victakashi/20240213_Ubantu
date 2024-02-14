def get_commands():
    commands = [
        ('lscpu | grep "Architecture\|Model name\|CPU(s)"', "CPU information"),  # Extract important information from lscpu command
        ('lsusb | grep "Bus\|Device\|ID"', "USB information"),  # Extract important information from lsusb command
        ('uname -a | grep "Linux"', "Linux version")  # Extract important information from uname -a command
    ]
    return commands
