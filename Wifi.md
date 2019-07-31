```
sudo apt update
sudo apt install snapd
sudo snap install wifi-ap
```
setup wifi
```
sudo /snap/bin/wifi-ap.config set dhcp.range-start=10.42.0.2
sudo /snap/bin/wifi-ap.config set dhcp.range-stop=10.42.0.199
sudo /snap/bin/wifi-ap.config set wifi.security-passphrase=robotseverywhere
sudo /snap/bin/wifi-ap.config set wifi.ssid=
```
Follow instruction on https://github.com/HackerShackOfficial/Raspberry-Pi-VNC-Mac

```
sudo apt-get install tightvncserver
vncserver :1
```
