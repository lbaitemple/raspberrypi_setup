

WPA_TEMPLATE= """country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev 
update_config=1

network={
      ssid="tusecurewireless"
      proto=RSN
      priority=1
      key_mgmt=WPA-EAP
      pairwise=CCMP
      auth_alg=OPEN
      eap=PEAP
      id_str="work"
      identity=%s
      password=hash:%s
}
"""

NETWORK_TEMPLATE= """# interfaces(5) file used by ifup(8) and ifdown(8)

# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

auto lo
iface lo inet loopback

allow-hotplug wlan0
auto wlan0
iface wlan0 inet dhcp
wireless-power off
    pre-up wpa_supplicant -B -Dwext -i wlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf
    post-down killall -q wpa_supplicant
iface default inet dhcp

"""

hashwd = """
echo -n %s | iconv -t UTF-16LE | openssl md4
"""

import getpass
import subprocess

if __name__ == '__main__':
    # get user's accessnet id and password
    accessnet=input("What is your accessNet ID (without @temple.edu): ")
    pswd = getpass.getpass('What is your accessNet password: ')

    # get a command to run the password to generate 32-byte hashword
    cmd = hashwd %(pswd)
    hashwd= subprocess.getoutput(cmd)

    # now we put thes inforamtion into the file template as a string
    wpa_str = WPA_TEMPLATE % (accessnet, hashwd)

    # write the file into a wpa_supplicant.conf
    text_file = open("wpa_supplicant.conf", "w")
    n = text_file.write(wpa_str)
    text_file.close()   

    # write the file into a interface
    text_file = open("interface", "w")
    n = text_file.write(NETWORK_TEMPLATE)
    text_file.close() 

    # need to cp the generated file to /etc/wpa_supplicant/
    #    cpcmd= subprocess.getoutput("sudo cp ./wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf")

    # need to cp the generated file to /etc/wpa_supplicant/
    # cpcmd= subprocess.getoutput("sudo cp ./interface /etc/network/interface")

