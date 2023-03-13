#### An easy way to setup wifi to Temple after you get a connection
```
wget https://raw.githubusercontent.com/lbaitemple/raspberrypi_setup/master/fresh/setupwifi.py
python3 ./setupwifi.py
```

### Old way - a little hard process
### get hash
```
echo -n [password] | iconv -t UTF-16LE | openssl md4
```

### add wps_supplicant password hash


###
```
git clone https://github.com/lbaitemple/raspberrypi_setup/
cd ~/raspberrypi_setup/fresh
cp interfaces /etc/network
```
