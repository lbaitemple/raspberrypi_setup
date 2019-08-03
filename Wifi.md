```
sudo apt update
sudo apt install snapd
sudo snap install wifi-ap
```
removed the line /usr/lib/arm-linux-gnueabihf/libarmmem.so from /etc/ld.so.preload, then no ERROR MESSAGE gone.


setup wifi
```
 sudo /snap/bin/wifi-ap.config set wifi.address=10.42.0.1
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
Install opencv2
```
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.0.0 opencv
mv opencv_contrib-4.0.0 opencv_contrib
cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE     -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules     -D ENABLE_NEON=ON -D ENABLE_VFPV3=ON     -D BUILD_TESTS=OFF -D OPENCV_ENABLE_NONFREE=ON     -D INSTALL_PYTHON_EXAMPLES=OFF     -D BUILD_EXAMPLES=OFF ..
make -j4
sudo make install
sudo ldconfig
echo "export PYTHONPATH=/usr/local/python/cv2/python-2.7" >> ~/.bashrc
```

Setup Pytorch
```
sudo apt-get install libopenblas-dev cython libatlas-base-dev m4 libblas-dev python-dev cmake python-yaml -y
sudo apt-get install libjpeg-dev -y
sudo apt-get install python-matplotlib -y
sudo apt-get install python-skimage -y
sudo pip install future  Pillow numpy
```
