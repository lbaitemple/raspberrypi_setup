This file setups a wifi access point using wifi-ap.config



```
wget https://raw.githubusercontent.com/lbaitemple/raspberrypi_setup/master/startup/access.sh
chmod +x access.sh
wget https://raw.githubusercontent.com/lbaitemple/raspberrypi_setup/master/startup/wifiacc.service
sudo cp wifiacc.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable  wifiacc
sudo systemctl start wifiacc
```

```
ip addr show $(awk 'NR==3{print $1}' /proc/net/wireless | tr -d :) | awk '/ether/{print $2}'
```
