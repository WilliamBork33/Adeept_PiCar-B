#!/usr/bin/python3
# File name   : setup.py
# Description : Control Motors
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : Shaun Longworth
# Date        : 2019/05/30
 
import os
import time
import sys
 
autostart_dir = "/home/pi/.config/autostart"
autostart_file = autostart_dir + "/car.desktop"
install_dir = "/home/pi/Adeept_PiCar-B/server"
 
# Commonly used functions
def replace_num(file,initial,new_num): 
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)
 
def run_os_command(cmd, max_runs=4):
    try:
        sys.stdout.write('###################################################\n')
        sys.stdout.write('Command: ' + cmd + '\n')
        for x in range(0,max_runs):
            if os.system(cmd) == 0:
                break
    except:
        print('AN ERROR OCCURRED RUNNING THE FOLLOWING COMMAND: ' + cmd)
        pass
 
def create_autostart():
    try:
        if (not os.path.exists(autostart_dir)):
            run_os_command("sudo mkdir '" + autostart_dir + "/'", 1)
        if (not os.path.isfile(autostart_file)):
            run_os_command("sudo touch " + autostart_file, 1)
        
        with open(autostart_file,'w') as file_to_write:
            file_to_write.write("[Desktop Entry]\n   Name=Car\n   Comment=Car\n   Exec=sudo python3 " + install_dir + "/server.py\n   Icon=false\n   Terminal=false\n   MutipleArgs=false\n   Type=Application\n   Catagories=Application;Development;\n   StartupNotify=true")
    except:
        print('Autostart failed.  Please try again')
        pass
 
def upgrade_system():
    # Upgrade the existing system
    run_os_command("sudo apt-get update")
    run_os_command("sudo apt-get -y upgrade")
 
def install_car():
    # Enable the interface(s)
    try:
        #replace_num("/boot/config.txt",'#dtparam=spi=on','dtparam=spi=on')
        replace_num("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
        #replace_num("/boot/config.txt",'#dtparam=i2s=on','dtparam=i2s=on')
    except:
        pass
   
    # Prepare to install.  Clean & Update the repositories
    run_os_command("sudo apt-get clean")
    run_os_command("sudo apt-get update")
    
    # Install the new software
    run_os_command("sudo apt-get install -y i2c-tools")
    run_os_command("sudo apt-get install -y swig")
    run_os_command("sudo apt-get install -y portaudio19-dev python3-all-dev python3-pyaudio")
    run_os_command("sudo apt-get install -y flac")
    run_os_command("sudo apt-get install -y bison libasound2-dev swig")
    run_os_command("sudo apt-get install -y python3 python3-dev python3-pip build-essential libpulse-dev")
    run_os_command("sudo apt-get install -y libopencv-dev")
    run_os_command("sudo apt-get install -y python-opencv")
    run_os_command("sudo apt-get install -y libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5 libqt4-test")
    run_os_command("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq")
 
    # Install the python modules
    run_os_command("sudo pip3 install pip")
    run_os_command("sudo pip3 install setuptools")
    run_os_command("sudo pip3 install wheel")
    run_os_command("sudo pip3 install adafruit-pca9685")
    run_os_command("sudo pip3 install pyaudio")
    run_os_command("sudo pip3 install imutils")
    run_os_command("sudo pip3 install opencv-python")
    run_os_command("sudo pip3 install zmq")
    run_os_command("sudo pip3 install pybase64")
    run_os_command("sudo pip3 install rpi_ws281x")
 
    # Create the Access Point
    run_os_command("git clone https://github.com/oblique/create_ap.git")
    run_os_command("cd //home/pi/create_ap && sudo make install", 1)
 
    # Download, build & Install Sphinxbase & PocketSphinx
    run_os_command("sudo wget https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz/download -O sphinxbase.tar.gz")
    run_os_command("sudo wget https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz/download -O pocketsphinx.tar.gz")
    run_os_command("sudo tar -xzvf sphinxbase.tar.gz")
    run_os_command("sudo tar -xzvf pocketsphinx.tar.gz")
 
    run_os_command("cd sphinxbase-5prealpha/ && ./configure -enable-fixed && make && sudo make install", 1)
    run_os_command("cd pocketsphinx-5prealpha/ && ./configure && make && sudo make install", 1)
    run_os_command("sudo pip3 install SpeechRecognition", 1)
    run_os_command("sudo pip3 install pocketsphinx", 1)
 
    # Set up the autostart, move the config file accordingly
    create_autostart()
    run_os_command("sudo cp -f " + install_dir + "/set.txt /home/pi/set.txt", 1)
 
def reboot_system():
    # Reboot the server to have the changes take effect
    run_os_command("sudo reboot")
 
while True:
    try:
        selection = int(input("Select an option:\n    1 = Upgrade OS;\n    2 = Install Car;\n    3 = Reboot;\n    4 = Exit\n\nOption to select: "))
        
        if selection == 1:
            upgrade_system()
            sys.stdout.write('###################################################\n')
            sys.stdout.write('IT IS RECOMMENDED YOU REBOOT BEFORE CONTINUING.....\n')
            sys.stdout.write('###################################################\n')
        elif selection == 2:
            install_car()
        elif selection == 3:
            reboot_system()
        elif selection == 4:
            break
        else:
            print("Invalid selection.  Please try again")   
    except:
        print("Invalid selection.  Please try again")
        pass