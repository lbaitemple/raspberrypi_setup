# raspberrypi_setup
1. Download newest image at
https://downloads.ubiquityrobotics.com/pi.html


2. VNC app on MAC/SSH on Linux//Putty on Win
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
# Rpi-Update
Raspberry-pi OS builds sometimes include rpi-update, which updates the kernel, firmware, etc.  
`sudo rpi-update`  
You must enter 'y' to do the update, the default is no.

# Zram  
formerly called compcache, is a Linux kernel module for creating a compressed block device in RAM, i.e. a RAM disk, but with on-the-fly "disk" compression. When used for swap, zram (like zswap also) allows Linux to make more efficient use of RAM, since the operating system can then hold more pages of memory in the compressed swap than if the same amount of RAM had been used as application memory or disk cache. This is particularly effective on machines that do not have much memory.

A compressed swap space with zram/zswap also offers advantages for low-end hardware devices such as embedded devices and netbooks. Such devices usually use flash-based storage, which has limited lifespan due to write amplification, and also use it to provide swap space. The reduction in swap usage as a result of using zram effectively reduces the amount of wear placed on such flash-based storage, resulting in prolonging its usable life. Also, using zram results in a significantly reduced I/O for Linux systems that require swapping.  

`sudo wget -O /usr/bin/zram.sh https://raw.githubusercontent.com/novaspirit/rpi_zram/master/zram.sh`  
`sudo chmod +x /usr/bin/zram.sh`  
`sudo nano /usr/bin/zram.sh`  
Change 1024 to 4096  
`sudo nano /etc/rc.local`  
Find the line that says "exit 0" and add one line above it
`/usr/bin/zram.sh`
Press control+x  
Press enter
Reboot

# RTC Problem
The Rpi doesn't have a real-time clock, and so it has to update it's time/locale everytime it's booted. When it can't do this quickly the OS has trouble assertng security keys, etc...  
We'll speed this up by setting the timezone manually:  
`sudo nano /usr/bin/setTimezone.sh`  
Put this in the file:  
`#!/bin/bash  
timedatectl set-timezone America/New_York`  
Now, add this to rc.local so it's run every boot-up  
`sudo nano /etc/rc.local`  
Find the line that says "exit 0" and add one line above it  
`/usr/bin/setTimezone.sh`  

# Kernel Build
The Rpi has v8 ARM based Broadcom 64-bit SOC, so to get most performance we want kernel architecture built for the ARCH=arm64 and CROSS_COMPILE=aarch64;

***Install Dependencies***  

`sudo apt-get update && sudo apt-get -y install build-essential libisl-dev libncurses5-dev bc git-core bison flex libmpfr-dev libmpc-dev libgmp-dev texinfo libreadline6-dev curl ccache libffi-dev libelf-dev libopenblas-dev libblas-dev m4 cmake cython python3-dev python3-yaml python3-setuptools libssl-dev automake autoconf help2man gawk expect`  
	  ***Binutils***  
Download: ~4min: `time wget -c https://ftp.gnu.org/gnu/binutils/binutils-2.32.tar.bz2`  
Decompress: ~1min: `time tar xvf binutils-2.32.tar.bz2 #takes_about_one_minute `   
Framework: `mkdir binutils-obj && cd binutils-obj`  
Environment: `export CFLAGS="-march=armv8-a -mtune=cortex-a53 -mfpu=crypto-neon-fp-armv8 -Ofast -ftree-vectorize -mlittle-endian -fgcse-after-reload -fvect-cost-model"`  
`export CXXFLAGS="-march=armv8-a -mtune=cortex-a53 -mfpu=crypto-neon-fp-armv8 -Ofast -ftree-vectorize -mlittle-endian -fgcse-after-reload -fvect-cost-model"`  
Configure: `../binutils-2.32/configure --prefix=/opt/aarch64 --disable-nls --enable-lto`  
Build: ~4min: `time make -j6 CFLAGS="-march=armv8-a -mtune=cortex-a53 -mfpu=crypto-neon-fp-armv8 -Ofast -ftree-vectorize -mlittle-endian -fgcse-after-reload -fvect-cost-model -pipe" CXXFLAGS="-march=armv8-a -mtune=cortex-a53 -mfpu=crypto-neon-fp-armv8 -Ofast -ftree-vectorize -mlittle-endian -fgcse-after-reload -fvect-cost-model -pipe"`  
Install: `time sudo make -j6 install`  
Add2Path: `echo 'export PATH="$PATH:/opt/aarch64/bin"'>>~/.bashrc && source ~/.bashrc
`  
	 **GCC**  
Download: ~4min: `time wget -c https://mirrors-usa.go-parts.com/gcc/releases/gcc-9.1.0/gcc-9.1.0.tar.xz`  
Decompress: ~2min: `time tar xf gcc-9.1.0.tar.xz`  
Framework: `mkdir gcc-out && cd gcc-out`  
Configure: `time ../gcc-9.1.0/configure --prefix=/opt/aarch64 --target=aarch64-linux-gnu --with-newlib --without-headers
 --disable-nls --disable-shared --disable-threads --disable-libssp --disable-decimal-float
 --disable-libquadmath --disable-libvtv --disable-libgomp --disable-libatomic
 --enable-languages=c`  
 Build: ~15min: `time make -j6 CFLAGS="-march=armv8-a -mtune=cortex-a53 -mfpu=crypto-neon-fp-armv8 -Ofast -ftree-vectorize -mlittle-endian -fgcse-after-reload -fvect-cost-model -pipe" CXXFLAGS="-march=armv8-a -mtune=cortex-a53 -mfpu=crypto-neon-fp-armv8 -Ofast -ftree-vectorize -mlittle-endian -fgcse-after-reload -fvect-cost-model -pipe"`  
 Install: `sudo make install-gcc`  
 This is already on path; to check: `echo $PATH`
We want to use latest rpi-kernel source

    git clone --depth=1 -b rpi-4.19.y https://github.com/raspberrypi/linux.git
    mkdir kernel-out
    cd linux  
Now we patch for rt

    wget -c https://mirrors.edge.kernel.org/pub/linux/kernel/projects/rt/4.19/patch-4.19.50-rt22.patch.xz
    xzcat patch-4.19.50-rt22.patch.xz | patch -p1
    make O=../kernel-out/ ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-  bcmrpi3_defconfig
Now we have the default bcmrpi3_defconfig kernel configuration, but it is good to check that we're using RT as the kernel setting. Use text editor to confirm compiler setting for real-time rt kernel build, or use menuconfig.

    make O=../kernel-out/ menuconfig -j6

Start compile:

    make -j6 O=../kernel-out/ ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-

Add QT
```
wget -c http://download.qt.io/official_releases/qt/5.13/5.13.0/qt-opensource-linux-x64-5.13.0.run
```
Login user:ubuntu pw:ubuntu

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
    make -j5
    sudo cp -v libarmem-v7l.so /usr/lib
    sudo su
    echo echo "/usr/lib/libarmmem-v7l.so" >> /etc/ld.so.preload
    exit
    
