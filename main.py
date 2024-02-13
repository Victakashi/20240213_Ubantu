import pexpect
import sys
import re
import time
import json
import csv
import ControlDC as CDC

def connect_to_system(IP):
    handle = pexpect.spawn('ssh root@'+IP, encoding='utf-8')
    handle.logfile_read = sys.stdout
    handle.setecho(False)
    connect = handle.expect(["password", "authenticity", pexpect.TIMEOUT])
    if connect == 0:
        handle.sendline("x1")
    elif connect == 1:
        handle.sendline("yes")
        handle.expect("password")
        handle.sendline("x1")
    handle.expect("root@localhost")
    return handle

def connect_to_system_console(IP, port):
    handle = pexpect.spawn(f"ssh -p {port} wistron@{IP}", encoding='utf-8', codec_errors="ignore")
    handle.logfile_read = sys.stdout
    handle.setecho(True)
    connect = handle.expect([r"password\:", "authenticity"])
    if connect == 0:
        handle.sendline("wistron123")
    elif connect == 1:
        handle.sendline("yes")
        handle.expect(r"password\:")
        handle.sendline("wistron123")
    handle.expect(r"Press \[Ctrl\+ d\] to go to the Suspend Menu.")
    return handle

def initial_DC_source(ip):
    CDC.ConnectDevice(ip)
    CDC.LaunchUSBRemote()
    time.sleep(2)
    CDC.ConnectDevice(ip)
    CDC.SetVoltage("48")
    time.sleep(2)
    CDC.ConnectDevice(ip)
    CDC.SetCurrent("20")
    time.sleep(2)

def connect_to_system_test(IP, PDU_IP, PDU_port):
    while True:
        # handle = pexpect.spawn(f'ping {IP}', encoding='utf-8')
        handle = pexpect.spawn(f'nc -v {IP} 22', encoding='utf-8')
        handle.logfile_read = sys.stdout
        handle.setecho(False)
        connect = handle.expect(["succeeded!", "failed", pexpect.TIMEOUT], timeout=10)
        if connect == 0:
            handle.sendcontrol("c")
            break
        elif connect == 1:
            CDC.OutputStart()
            time.sleep(60)
        elif connect == 2:
            CDC.OutputStart()
            time.sleep(60)
    handle.close()
    time.sleep(10)
    handle = pexpect.spawn('ssh root@'+IP, encoding='utf-8')
    handle.logfile_read = sys.stdout
    handle.setecho(False)
    connect = handle.expect(["password", "authenticity"])
    if connect == 0:
        handle.sendline("x1")
    elif connect == 1:
        handle.sendline("yes")
        handle.expect("password")
        handle.sendline("x1")
    handle.expect("root@localhost")
    return handle

def inital(handle):
    handle.sendline("cd sunnyvale-diag/")
    handle.expect(["root@localhost", pexpect.TIMEOUT], timeout=10)
    handle.sendline("./diag.py")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=10)
    handle.sendline("board init")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=60)

def check_info(handle):
    result = []
    # diag version
    handle.sendline("sysinfo diag")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=10)
    index = re.search(r"Diag version (\d*.\d*)", handle.before)
    if index is not None:
        result.append(["Diag version", index.group(1)])
    else:
        result.append(["Diag version", " "])

    # BIOS version
    handle.sendline("sysinfo bios")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=10)
    index = re.search(r"Version\: (.*)\r", handle.before)
    if index is not None:
        result.append(["BIOS version", index.group(1)])
    else:
        result.append(["BIOS version", " "])

    # BMC version
    handle.sendline("sysinfo bmc")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=10)
    index = re.search(r"Firmware Revision *\: (\d*.\d*)", handle.before)
    if index is not None:
        result.append(["BMC version", index.group(1)])
    else:
        result.append(["BMC version", " "])

    # CPLD version
    handle.sendline("sysinfo cpld")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=10)
    index = re.search(r"CPU_CPLD version:\r\n\t(.*)\r\nCPLD1 version:\r\n\t(.*)\r\nCPLD2 version:\r\s\t(.*)\r", handle.before)
    if index is not None:
        result.append(["CPU_CPLD version", index.group(1)])
        result.append(["CPLD1 version", index.group(2)])
        result.append(["CPLD2 version", index.group(3)])
    else:
        result.append(["CPU_CPLD version", " "])
        result.append(["CPLD1 version", " "])
        result.append(["CPLD2 version", " "])

    # FPGA version
        handle.sendline("sysinfo fpga")
        handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=10)
        index = re.search(r"FPGA version:\r\n\t(.*)\r\n", handle.before)
        if index is not None:
            result.append(["FPGA version", index.group(1)])
        else:
            result.append(["FPGA version", " "])

    #ONIE version
    handle.sendline("exit")
    handle.expect(["root@localhost", pexpect.TIMEOUT], timeout=10)
    handle.sendline("onie-shell")
    index = handle.expect(["\/ \#", pexpect.TIMEOUT])
    if index == 1:
        print("Fail to login to ONIE")
        result.append(["Fail to login to ONIE", ""])
    else:
        handle.sendline("cat /etc/os-release")
        handle.expect(["\/ \#", pexpect.TIMEOUT])
        index = re.search(r'VERSION=\"(.*)\"', handle.before)
        if index is not None:
            result.append(["ONIE version", index.group(1)])
        else:
            result.append(["ONIE version", " "])
        handle.sendline("exit")
        handle.expect(["root@localhost", pexpect.TIMEOUT], timeout=10)
    return result

def DC_ON_OFF_Test(handle):
    cycle_result = []
    handle.sendline("bmc i2c2cpu")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=90)
    handle.sendline("sysinfo cpu")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=20)
    index = re.search(r"(Intel\(R\) Atom\(TM\) CPU C3758R @ 2.40GHz)", handle.before)
    if index is not None:
        cycle_result.append(["CPU", "PASS"])
    else:
        cycle_result.append(["CPU", "FAIL"])

    handle.sendline("sysinfo memory")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=20)
    index = re.search(r"(Locator: DIMM1\r\n\t.*\r\n\t.*\r\n\tSize: 16384 MB\r\n)", handle.before)
    if index is not None:
        cycle_result.append(["Memory", "PASS"])
    else:
        cycle_result.append(["Memory", "FAIL"])

    handle.sendline("sysinfo storage")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=20)
    index = re.search(r"(SATA Version is:  SATA 3.2, 6.0 Gb/s \(current: 6.0 Gb/s\))", handle.before)
    if index is not None:
        cycle_result.append(["Storage", "PASS"])
    else:
        cycle_result.append(["Storage", "FAIL"])

    handle.sendline("board check")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=20)
    index = re.search(r"(.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n.*\[OK\]\r\n)", handle.before)
    if index is not None:
        cycle_result.append(["Board Check", "PASS"])
    else:
        cycle_result.append(["Board Check", "FAIL"])

    handle.sendline("fan status")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=20)
    index = re.search(r"(\r\n1 *Yes *Yes *Yes.*\r\n2 *Yes *Yes *Yes.*\r\n3 *Yes *Yes *Yes.*\r\n4 *Yes *Yes *Yes.*\r\n5 *Yes *Yes *Yes.*\r\n6 *Yes *Yes *Yes)", handle.before)
    if index is not None:
        cycle_result.append(["Fan", "PASS"])
    else:
        cycle_result.append(["Fan", "FAIL"])

    handle.sendline("psu status")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=20)
    # print(repr(handle.before))
    index = re.search(r"(off *False\r\n\t.*\r\n\t.*\r\n\t.*\r\n\t.*\r\n\t.*\r\n\t.*\r\n\t.*\r\n\t.*\r\n\t.*\r\n\t.*\r\n\r\n\r\nPSU2\r\n\t.*\r\n\t.*\r\n\t.*\r\n\t.*\r\n\r\n\t.*\r\n\t.*\r\n\toff *False\r\n)", handle.before)
    if index is not None:
        cycle_result.append(["PSU", "PASS"])
    else:
        cycle_result.append(["PSU", "FAIL"])

    handle.sendline("qsfp status")
    handle.expect(["Sunnyvale \>", pexpect.TIMEOUT], timeout=90)
    index = re.search(r"(1 *Yes.*\r\n2 *Yes.*\r\n3 *Yes.*\r\n4 *Yes.*\r\n5 *Yes.*\r\n6 *Yes.*\r\n7 *Yes.*\r\n8 *Yes.*\r\n9 *Yes.*\r\n10 *Yes.*\r\n11 *Yes.*\r\n12 *Yes.*\r\n13 *Yes.*\r\n14 *Yes.*\r\n15 *Yes.*\r\n16 *Yes.*\r\n17 *Yes.*\r\n18 *Yes.*\r\n19 *Yes.*\r\n20 *Yes.*\r\n21 *Yes.*\r\n22 *Yes.*\r\n23 *Yes.*\r\n24 *Yes.*\r\n25 *Yes.*\r\n26 *Yes.*\r\n27 *Yes.*\r\n28 *Yes.*\r\n29 *Yes.*\r\n30 *Yes.*\r\n31 *Yes.*\r\n32 *Yes.*\r\n)", handle.before)
    if index is not None:
        cycle_result.append(["QSFP", "PASS"])
    else:
        cycle_result.append(["QSFP", "FAIL"])
    handle.sendline("bmc i2c2bmc")
    handle.expect([r"Sunnyvale \>", pexpect.TIMEOUT], timeout=90)
    handle.sendline("exit")
    handle.expect(["root@localhost", pexpect.TIMEOUT], timeout=90)

    for rr in cycle_result:
        print(rr)
    return cycle_result

if __name__ == '__main__':
    with open("config_file.json", "r") as read_file:
        config = json.load(read_file)
    DUT_IP = config["DUT"]
    console_server = config["console_server"]
    port = config["console_port"]
    PDU_IP = config["PDU"]
    CDC.ControlDC()
    initial_DC_source(PDU_IP)
    p1 = connect_to_system(DUT_IP)
    inital(p1)
    result = check_info(p1)
    p1.close()
    with open("DC_ON_OFF_test_result.csv", "a", newline='') as csvfile:
        result_output = csv.writer(csvfile)
        result_output.writerow(["DC ON OFF Test Result"])
        result_output.writerows(result)
        result_output.writerow([" "])
    p1 = connect_to_system_console(console_server, port)
    for i in range(1, 1001):
        log = open(f"test_log/{i}.txt", "w")
        p1.logfile_read = log
        CDC.ConnectDevice(PDU_IP)
        CDC.OutputStart()
        p1.sendline(" ")
        p1.expect([r"localhost login\:", pexpect.TIMEOUT], timeout=600)
        p1.sendline("root")
        p1.expect([r"Password\:", pexpect.TIMEOUT], timeout=30)
        p1.sendline("x1")
        p1.expect(["root@localhost", pexpect.TIMEOUT], timeout=30)
        inital(p1)
        check_result = DC_ON_OFF_Test(p1)
        i_result = ""
        for cr in check_result:
            if cr[1] != "PASS":
                i_result = i_result + cr[0] + ", "
        if len(i_result) != 0:
            with open("DC_ON_OFF_test_result.csv", "a", newline='') as csvfile:
                result_output = csv.writer(csvfile)
                result_output.writerow([i, "FAIL", i_result])
        else:
            with open("DC_ON_OFF_test_result.csv", "a", newline='') as csvfile:
                result_output = csv.writer(csvfile)
                result_output.writerow([i, "PASS"])
        p1.sendline("poweroff")
        p1.expect(["Stopped", pexpect.TIMEOUT], timeout=10)
        time.sleep(30)
        CDC.ConnectDevice(PDU_IP)
        CDC.OutputStop()
        log.close()
        time.sleep(120)