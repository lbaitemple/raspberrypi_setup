# raspberrypi_setup
1. Download newest image at
https://downloads.ubiquityrobotics.com/pi.html


2. vnc app on MAC/ssh on linux//putty on Win
https://github.com/HackerShackOfficial/Raspberry-Pi-VNC-Mac

a. create wlan
```
sudo nano /etc/udev/rules.d/70-persistent-net.rules
```

Put the following content
   
```
# This file was automatically generated by the /lib/udev/write_net_rules
# program, run by the persistent-net-generator.rules rules file.

# PCI device 0x8086:0x10c9 (igb)
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="b8:27:eb:ec:7e:88", ATTR{type}=="1", KERNEL=="wlan*", NAME="wlan0"

```


add modules
```
sudo nano /etc/modules
```

The contents are:
```
uinput
i2c-bcm2708
i2c-dev
r8712u
brcmfmac
brcmutil

```
# Kernel Build
The Rpi has v8 ARM based Broadcom 64-bit SOC, so to get most performance we want kernel architecture built for the ARCH=arm64 and CROSS_COMPILE=aarch64;

Assumed cross-compile environment is AMD64 Ubuntu Linux
	  **Binutils**  
`sudo apt-get install build-essential libgmp-dev libmpfr-dev libmpc-dev libisl-dev libncurses5-dev bc git-core bison flex`  
`wget -c https://ftp.gnu.org/gnu/binutils/binutils-2.29.1.tar.bz2`  
`tar xvf binutils-2.29.1.tar.bz2`  
`mkdir binutils-obj && cd binutils-obj`  
`../binutils-2.29.1/configure --prefix=/opt/aarch64 --target=aarch64-linux-gnu --disable-nls`  
`make -j4`  
`sudo make install`  
`export PATH=$PATH:/opt/aarch64/bin/`  
	 **GCC**  
`wget https://ftp.gnu.org/gnu/gcc/gcc-6.4.0/gcc-6.4.0.tar.xz`  
`tar xvf gcc-6.4.0.tar.xz`  
`mkdir gcc-out && cd gcc-out`  
`../gcc-6.4.0/configure --prefix=/opt/aarch64 --target=aarch64-linux-gnu --with-newlib --without-headers \
 --disable-nls --disable-shared --disable-threads --disable-libssp --disable-decimal-float \
 --disable-libquadmath --disable-libvtv --disable-libgomp --disable-libatomic \
 --enable-languages=c`  
 `make all-gcc -j4`  
 `sudo make install-gcc`  
 
We want to use realtime kernel for latency control statistics  

    git clone --depth=1 -b rpi-4.14.y-rt https://github.com/raspberrypi/linux.git  
    mkdir kernel-out  
    cd linux  
    make O=../kernel-out/ ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-  bcmrpi3_defconfig  
Now we have the default bcmrpi3_defconfig kernel configuration, but it is good to check that we're using RT as the kernel setting. Use text editor to confirm compiler setting for real-time rt kernel build, or use menuconfig.

    make O=../kernel-out/ ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- menuconfig  

Start compile:  

    make -j4 O=../kernel-out/ ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-  

Add QT  
```
wget -c http://download.qt.io/official_releases/qt/5.11/5.11.1/qt-opensource-linux-x64-5.11.1.run  
sudo raspi-update -y && sudo reboot  

```
Login user:ubuntu pw:ubuntu  

**ZRAM**  
Zram, formerly called compcache, is a Linux kernel module for creating a compressed block device in RAM, i.e. a RAM disk, but with on-the-fly "disk" compression. When used for swap, zram (like zswap also) allows Linux to make more efficient use of RAM, since the operating system can then hold more pages of memory in the compressed swap than if the same amount of RAM had been used as application memory or disk cache. This is particularly effective on machines that do not have much memory.

A compressed swap space with zram/zswap also offers advantages for low-end hardware devices such as embedded devices and netbooks. Such devices usually use flash-based storage, which has limited lifespan due to write amplification, and also use it to provide swap space. The reduction in swap usage as a result of using zram effectively reduces the amount of wear placed on such flash-based storage, resulting in prolonging its usable life. Also, using zram results in a significantly reduced I/O for Linux systems that require swapping.  

`sudo wget -O /usr/bin/zram.sh https://raw.githubusercontent.com/novaspirit/rpi_zram/master/zram.sh`  
`sudo chmod +x /usr/bin/zram.sh`  
`sudo nano /etc/rc.local`  
Find the line that says "exit 0" and add one line above it
`/usr/bin/zram.sh`
Press control+x  
Press enter
Reboot

# codeblock
    Open Terminal: ctl + alt + t
    Copy text: ctl+shift+c
    Paste text: print ctl+shift+v

    
    Fixes Repository Public Key Error
    sudo sh -c 'echo "deb https://packages.ubiquityrobotics.com/ubuntu/ubiquity xenial main" > /etc/apt/sources.list.d/ubiquity-latest.list'
    sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key C3032ED8

    sudo apt update && sudo apt upgrade 
    
    Updates to newest stable kernel
    sudo rpi-update (select yes to update)
    sudo reboot
    
    Open Terminal
    
    Optimized Memcpy/Memset:
    wget https://github.copm/bavison/arm-mem/archive/master.tar.gz
    tar xvf master.tar.gz && cd arm-mem-master
    make -j4
    sudo cp -v libarmem-v7l.so /usr/lib
    sudo su
    echo echo "/usr/lib/libarmmem-v7l.so" >> /etc/ld.so.preload
    exit
    
    sudo apt install python-dev python3-dev gfortran build-essential bison flex ncurses5 git wget curl
