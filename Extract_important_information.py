
import subprocess
from commands import get_commands

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    return output.decode('utf-8')

def main():
    commands = get_commands()

    for command, label in commands:
        print("")
        print(f"=== {label} ===")
        output = run_command(command)
        print(output.strip())  # Print the output of the command
        print("=" * 40)
　　　　 print("")
if __name__ == "__main__":
    main()

print(main)
