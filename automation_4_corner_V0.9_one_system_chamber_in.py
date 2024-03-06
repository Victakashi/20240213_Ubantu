import pexpect
import sys
import time
import json

import datetime
from datetime import datetime
import pdu_20210611 as Pdu  
import G1_diag as diag 
import system_setting_in as system_in
import ixia_script as ixia
import pandas as pd 
import subprocess 


###basice config
with open("/home/vic/Galileo_automation_release/config.json",mode= "r") as file:
    data = json.load(file)
clist=data["IP"]
chamber_in_ip=clist["chamber_in_ip"]
chamber_in_power_on_off=clist["chamber_in_power_on_off"]
chamber_out_ip=clist["chamber_out_ip"]
espec1_ip=clist["espec1_ip"]
chamber_console_seaver_ip=clist["chamber_console_seaver_ip"]
chamber_console_seaver_ip_port_16=clist["chamber_console_seaver_ip_port_16"]


##25C

if __name__ == '__main__':

    #templist = ['25','50', '25','50', '25','50', '25','50', '25','50', '25','50', '25','50', '25','50', '25',]
    #templist = ['-5' ]

    #for tempset in templist:
        
        with open(str(("G1_PVT2_one_system_GS_V0.3.1_"+ str(datetime.now()) + ".txt")), mode='a+', encoding="utf-8" ) as file:

            # # temp up to tempset

            # Pdu.pdu_control(str(chamber_in_power_on_off), "wistron", "wistron123", "07", "off")
            # Pdu.pdu_control(str(chamber_in_power_on_off), "wistron", "wistron123", "08", "off")

            # settemp=int(tempset) 
            # print("settemp: " + str(settemp))
            # subprocess.getoutput('Chamber.py 192.168.123.44 settemp {}'.format(str(settemp)))
            # time.sleep(20)
            
            # file.write(str(tempset))
            # file.write("\n")

            # while True:  
                
            #     Measuredtemp = subprocess.getoutput('Chamber.py 192.168.123.44 gettemp | grep Measured | awk \'{print $4}\'')
            #     #print(type(Measuredtemp))
            #     p=round(float(Measuredtemp)) 
            #     print("Measuredtemp: "+ str(p) )
            #     time.sleep(30)
            #     if int(p) == int(settemp):
            #         break

            # time.sleep(900)
            
            for i in range(1,31):  ##time -1 

                ###Power on/off
                #Pdu.pdu_control(str(chamber_in_power_on_off), "wistron", "wistron123", "02", "off")
                Pdu.pdu_control(str(chamber_in_power_on_off), "wistron", "wistron123", "02", "off")
                time.sleep(10)
                print("<<<<<Time " + str(datetime.now()) + ">>>>>>>\n")
                #Pdu.pdu_control(str(chamber_in_power_on_off), "wistron", "wistron123", "07", "on")
                Pdu.pdu_control(str(chamber_in_power_on_off), "wistron", "wistron123", "02", "on")
                print("<<<<<Time " + str(datetime.now()) + ">>>>>>>\n")
                print("<<<<<Number " + str(i) + ">>>>>>>\n")
                time.sleep(720)
                # ###diag test   ##One file
                
                #diag.G1_diag(str(chamber_in_ip))


                ##system setting
                #system_in.system_setting(str(chamber_in_ip))
                #system_in.system_setting(str(chamber_out_ip))
                #time.sleep(20)

                #p = pexpect.spawn('ssh -p '+ str(chamber_console_seaver_ip_port_16) +' wistron@' + str(chamber_console_seaver_ip), encoding='utf-8',timeout=200)
                p = pexpect.spawn('ssh root@'+str(chamber_out_ip), encoding='utf-8')
                p.logfile = sys.stdout
                p.setecho(False)
                p.expect("password")
                p.sendline("x1")
                p.expect("root@localhost")

                # p.expect("password:")
                # time.sleep(1)
                # p.sendline("wistron123")
                # time.sleep(1)
                # p.sendline("\r")
                # p.sendline("\r")
                # p.expect("localhost login:")
                # p.sendline("root")
                # p.expect("Password:")
                # p.sendline("x1")

                p.sendline("systemctl restart gs-south-tai")
                p.expect("root@localhost",timeout=200)

                time.sleep(10)

                ## interface admin-status up

                for j in range(1,21):
                    time.sleep(0.5)
                    p.sendline("gscli -c 'interface Ethernet"+ str(j) +"_1;no shutdown'")
                    p.expect("root@localhost",timeout=100)
                
                for j in range(1,5):
                    time.sleep(0.5)
                    p.sendline("gscli -c 'transponder piu"+ str(j) +";admin-status up'")
                    #p.sendline("gscli -c 'transponder piu3;admin-status up'")
                    p.expect("root@localhost",timeout=100)
                
                for j in range(13,20):
                    time.sleep(0.5)
                    p.sendline("gscli -c 'interface Ethernet"+ str(j) +"_1;admin-status up'")
                    p.expect("root@localhost",timeout=100)


                time.sleep(120)

                ###show transponder summary
                # p = pexpect.spawn('ssh -p '+ str(chamber_console_seaver_ip_port_16) +' wistron@' + str(chamber_console_seaver_ip), encoding='utf-8',timeout=200)
                # p.logfile = sys.stdout
                # p.setecho(False)
                # p.expect("password")
                # p.sendline("x1")
                #p.expect("root@localhost")
                p.sendline("gscli -c 'show transponder summary'")
                p.expect("root@localhost",timeout=100)
                p.sendline("gscli -c 'show transponder summary'")
                p.expect("root@localhost",timeout=100)
                transponder_summary=p.before   
                file.write("<<<<<Number " + str(i) + ">>>>>>>\n")
                file.write("<<<<<Number " + str(datetime.now()) + ">>>>>>>\n")
                file.write("<<<<<Show transponder summary>>>>>>>\n")
                file.write(transponder_summary)
                file.write("\n<<<<<  Next >>>>>>>\n")        
                time.sleep(2)



                ### show gslileo piu
                p.sendline("galileo -c piu")
                p.expect("root@localhost",timeout=100)
                p.sendline("galileo -c piu")
                p.expect("root@localhost",timeout=100)
                piu_summary=p.before   
                file.write("<<<<<Number " + str(i) + ">>>>>>>\n")
                file.write("<<<<<Number " + str(datetime.now()) + ">>>>>>>\n")
                file.write("<<<<<Show Galileo PIU>>>>>>>\n")
                file.write(piu_summary)
                file.write("\n<<<<<  Next >>>>>>>\n")        
                time.sleep(2)



                ### show Goldstone version
                p.sendline("gscli -c 'show version'")
                p.expect("root@localhost",timeout=100)
                p.sendline("gscli -c 'show version'")
                p.expect("root@localhost",timeout=100)
                version=p.before  
                file.write("<<<<<Number " + str(i) + ">>>>>>>\n")
                file.write("<<<<<Number " + str(datetime.now()) + ">>>>>>>\n")
                file.write("<<<<<Show Goldstone version>>>>>>>\n")
                file.write(version)
                time.sleep(2)

                ### BMC/FPGA
                p.sendline("ipmitool raw 0x30 0x23")
                p.expect("root@localhost",timeout=100)
                p.sendline("ipmitool raw 0x30 0x23")
                p.expect("root@localhost",timeout=100)
                BMC=p.before   
                file.write("<<<<<Number " + str(i) + ">>>>>>>\n")
                file.write("<<<<<Number " + str(datetime.now()) + ">>>>>>>\n")
                file.write("<<<<<Show BMC/FPGA version>>>>>>>\n")
                file.write(str(BMC))
                file.write("\n<<<<<  Next >>>>>>>\n")        
                time.sleep(2)


                i2clist = ['0', '1', '3' , '5', '7']
                for i2cset in i2clist:
                    ###i2cdetect
                    p.sendline("i2cdetect -y " + str(i2cset))
                    p.expect("root@localhost",timeout=100)
                    p.sendline("i2cdetect -y " + str(i2cset))
                    p.expect("root@localhost",timeout=100)
                    i2c=p.before   
                    file.write("<<<<<Number " + str(i) + ">>>>>>>\n")
                    file.write("<<<<<Number " + str(datetime.now()) + ">>>>>>>\n")
                    file.write("<<<<<Show i2cdetect -y 0>>>>>>>\n")
                    file.write(str(i2c))
                    file.write("\n<<<<<  Next >>>>>>>\n")        
                    time.sleep(2)


                ###show Allfunction
                p.sendline("kubectl get pods")
                p.expect("root@localhost")
                Allfunction=p.before   

                file.write("\n<<<<<Number " + str(i) + ">>>>>>>\n")
                file.write("<<<<<time "  + str(datetime.now()) + ">>>>>>>\n")
                file.write(Allfunction)
                file.write("\n<<<<<  Next >>>>>>>\n")        
                time.sleep(2)



                

                # ###Ixia transmission MAc addres learning

                # result1 = ixia.ixia_traffic_test(5, "N/A")   ###2 sec reset

                # ###clear interface counters
                # p.sendline("kubectl exec -it usonic-cli -- bash")
                # p.expect("root@usonic-cli:/#")
                # p.sendline("sonic-clear counter")
                # p.sendline("exit")
                # p.expect("root@localhost")

                # # p = pexpect.spawn('ssh root@'+str(chamber_out_ip), encoding='utf-8')
                # # p.logfile = sys.stdout
                # # p.setecho(False)
                # # p.expect("password")
                # # p.sendline("x1")
                # # p.expect("root@localhost")
                # # p.sendline("kubectl exec -it usonic-cli -- bash")
                # # p.expect("root@usonic-cli:/#")
                # # p.sendline("sonic-clear counter")
                # # p.sendline("exit")
                # # p.expect("root@localhost")



                # time.sleep(5)
                # ###Ixia transmission 

                # result = ixia.ixia_traffic_test(600, "N/A")   ### sec
                # date=pd.DataFrame(result)
                # file.write("\n<<<<<Number " + str(i) + ">>>>>>>\n")
                # file.write("\n<<<<<time " + str(datetime.now()) + ">>>>>>>\n")
                # file.write(str(date))

                # file.write("\n\n\n<<<<<  Next >>>>>>>\n\n\n")      
                # time.sleep(10)

                # print(str(datetime.now()))


                ###show interface counters

                # p = pexpect.spawn('ssh -p '+ str(chamber_console_seaver_ip_port_16) +' wistron@' + str(chamber_console_seaver_ip), encoding='utf-8',timeout=200)
                # p.logfile = sys.stdout
                # p.setecho(False)
                # p.expect("password")
                # p.sendline("x1")
                # p.expect("root@localhost")
                # p.sendline("kubectl exec -it usonic-cli -- bash")
                # p.expect("root@usonic-cli:/#")
                # p.sendline("show interface counter")
                # p.expect("root@usonic-cli:/#")
                # p.sendline("show interface counter")
                # p.expect("root@usonic-cli:/#")
                # interface_counters=p.before
                # time.sleep(2)
                # file.write("<<<<<Number " + str(i) + ">>>>>>>\n")
                # file.write("\n<<<<<time "  + str(datetime.now()) + ">>>>>>>\n")
                # #file.write("\n<<<<< (in_hight Voltage) Counter ip "  + str(chamber_in_ip) + ">>>>>>>\n")
                # file.write(interface_counters)   
                # file.write("\n\n\n<<<<<  Next >>>>>>>\n")        
                # time.sleep(2)
                # p.sendline("exit")
                # p.expect("root@localhost")


                # p = pexpect.spawn('ssh root@'+ str(chamber_out_ip), encoding='utf-8')
                # p.logfile = sys.stdout
                # p.setecho(False)
                # p.expect("password")
                # p.sendline("x1")
                # p.expect("root@localhost")
                # p.sendline("kubectl exec -it usonic-cli -- bash")
                # p.expect("root@usonic-cli:/#")
                # p.sendline("show interface counter")
                # p.expect("root@usonic-cli:/#")
                # p.sendline("show interface counter")
                # p.expect("root@usonic-cli:/#")
                # interface_counters=p.before
                # time.sleep(2)
                # file.write("<<<<<Number " + str(i) + ">>>>>>>\n")
                # file.write("\n<<<<<time "  + str(datetime.now()) + ">>>>>>>\n")
                # file.write("\n<<<<< (out_PVT2) Counter ip "  + str(chamber_out_ip) + ">>>>>>>\n")
                # file.write(interface_counters)   
                # file.write("\n\n\n<<<<<  Next >>>>>>>\n")        
                # time.sleep(2)
                # p.sendline("exit")
                # p.expect("root@localhost")






                # ##nowtemp & humi

                # file.write("\n\n\n<<<<<  nowtemp >>>>>>>\n\n\n") 

                # nowtemp = subprocess.getoutput('Chamber.py 192.168.123.44 gettemp')
                # file.write(str(nowtemp))
                # file.write("\n\n\n<<<<<  nowhumi >>>>>>>\n\n\n") 
                # nowhumi = subprocess.getoutput('Chamber.py 192.168.123.44 gethumi')
                # file.write(str(nowhumi))
                # file.write("\n\n\n") 



                ###ipmitool sensor

                # p = pexpect.spawn('ssh -p '+ str(chamber_console_seaver_ip_port_16) +' wistron@' + str(chamber_console_seaver_ip), encoding='utf-8',timeout=200)
                # p.logfile = sys.stdout
                # p.setecho(False)
                # p.expect("password")
                # p.sendline("x1")
                #p.expect("root@localhost")
                p.sendline("ipmitool sensor")
                p.expect("root@localhost")
                ipmitool_sensor=p.before   
                file.write("<<<<<Number " + str(i) + ">>>>>>>\n")
                file.write("<<<<<time " + str(datetime.now()) + ">>>>>>>\n")
                file.write(ipmitool_sensor)
                #p.expect("root@localhost")


                ###show interface brief
                time.sleep(20)
                file.write("\n<<<<<  show interface brief>>>>>>>\n")   
                p.sendline("gscli -c 'show interface brief'")
                p.expect("root@localhost",timeout=100)
                p.sendline("gscli -c 'show interface brief'")
                p.expect("root@localhost",timeout=100)
                interface=p.before   
                file.write("<<<<<Number " + str(i) + ">>>>>>>\n")
                file.write("<<<<<Number " + str(datetime.now()) + ">>>>>>>\n")
                file.write(interface)
                file.write("\n<<<<<  Next >>>>>>>\n")        
                time.sleep(2)


                
                file.write("\n\n\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Finish "+ str(i) + " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n\n\n")     
                time.sleep(5)

