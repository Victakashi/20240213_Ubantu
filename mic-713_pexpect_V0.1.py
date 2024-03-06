import time
import sys
import pexpect

if __name__ == '__main__':
    
    hostname = '172.16.106.70' #'remote_host_ip'
    username = 'mic-713'       #'your_username'
    password = 'mic-713'       #'your_password'
    port = 22  # or any other port you are using for SSH
    print("****************111***********")
    
    for i in range(1,5):
        print("****************222***********")
        p = pexpect.spawn(f"ssh -p {port} {username}@{hostname}", encoding='utf-8', codec_errors="ignore", timeout=10)
        p.logfile = sys.stdout
        p.setecho(True)
        p.expect("password")
        p.sendline(password)
        p.expect(r"mic-713@ubuntu", timeout=5)
        print("****************333***********")
        # Send lsusb command
        p.sendline(r'lsusb')
        p.expect(r"mic-713@ubuntu", timeout=5)
        lsusb_output = p.before
        print(lsusb_output)
        # Expect system prompt
        p.expect(r"mic-713@ubuntu", timeout=5)
        # Read and print lsusb output
                
        print("****************333***********")
        
        print("lsusb command executed successfully.")
        # Close the connection
        
        p.close()
    print("***************END***********")
