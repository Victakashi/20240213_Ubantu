import pexpect

def reboot_remote(hostname, username, password):
    try:
        # Construct SSH command
        ssh_command = f'ssh {username}@{hostname}'
        # Start SSH process using spawn
        p = pexpect.spawn(ssh_command)
        # Wait for password prompt
        p.expect('password:')
        # Input password
        p.sendline(password)
        # Wait for successful login prompt
        p.expect('\$')
        # Send reboot command
        p.sendline('sudo reboot')
        # Wait for password prompt during reboot
        p.expect('assword:')
        # Input password
        p.sendline(password)
        # Wait for prompt after reboot completes
        p.expect('\$')
        print("Remote host has been rebooted")
        # Close SSH connection
        p.close()
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    # Replace with actual IP address, username, and password of the remote host
    hostname = 'remote_host_ip'
    username = 'your_username'
    password = 'your_password'

    # Call function to perform reboot operation
    reboot_remote(hostname, username, password)
