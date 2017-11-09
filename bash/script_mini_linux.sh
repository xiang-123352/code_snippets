#!/bin/sh

#	Mini Linux/BusyBox system by ADcomp <david.madbox@gmail.com>
#	*** tested with Ubuntu 12.04 LTS ***

# base directory
echo " -- create base directory"
mkdir mini_linux && cd mini_linux

# live directory
mkdir -p live/boot/isolinux

# minimal root filesystem
echo " -- create minimal root filesystem"
mkdir rootfs && cd rootfs
mkdir bin lib proc root sbin sys tmp 
mkdir -p usr/lib usr/local usr/share/kmap usr/bin usr/sbin
mkdir -p var/cache var/lib var/lock var/log var/run var/spool
mkdir -p dev/pts dev/shm dev/input dev/net dev/usb
mkdir -p etc/init.d
chmod 1777 tmp

# copy /dev nodes ..
cp -dpR /dev/console dev/
cp -dpR /dev/tty dev/
cp -dpR /dev/tty[0-6] dev/
cp -dpR /dev/null dev/
cp -dpR /dev/zero dev/
cp -dpR /dev/ram0 dev/

# busybox
echo " -- copy busybox & create symbolic link"
cp /bin/busybox bin
chmod 4755 bin/busybox
chroot ../rootfs /bin/busybox --install -s
rm linuxrc
ln -s bin/busybox init

# keyboard
/bin/busybox dumpkmap > usr/share/kmap/dump.kmap

echo """# /etc/fstab: information about static file system.
proc            /proc        proc    defaults          0       0
sysfs           /sys         sysfs   defaults          0       0
devpts          /dev/pts     devpts  defaults          0       0
tmpfs           /dev/shm     tmpfs   defaults          0       0
""" > etc/fstab

echo """#! /bin/sh
echo "Processing /etc/init.d/rcS ... "
/bin/mount proc
/bin/mount -a
/bin/hostname -F /etc/hostname
/sbin/ifconfig lo 127.0.0.1 up
/sbin/loadkmap < /usr/share/kmap/dump.kmap
""" > etc/init.d/rcS
chmod a+x etc/init.d/rcS

echo """::sysinit:/etc/init.d/rcS
::respawn:-/bin/sh
tty2::askfirst:-/bin/sh
::ctrlaltdel:/bin/umount -a -r
::ctrlaltdel:/sbin/reboot
""" > etc/inittab

# config stuff ..
echo "127.0.0.1      localhost" > etc/hosts
echo "minux" > etc/hostname
echo "/bin/sh" > etc/shells
echo "Mini Linux BusyBox experiment 0.1" > etc/issue
echo "order hosts,bind" > etc/host.conf
echo "multi on" >> etc/host.conf
echo """PATH="/usr/sbin:/usr/bin:/sbin:/bin"
LD_LIBRARY_PATH="/usr/lib:/lib"

if [ "`id -u`" -eq 0 ]; then
PS1='\e[1m\u@\h:\w\#\e[m '
else
PS1='\e[1m\u@\h:\w\$\e[m '
fi

DISPLAY=:0.0

export PATH LD_LIBRARY_PATH PS1 DISPLAY ignoreeof
umask 022
""" > etc/profile

# Users, groups and passwords
echo "root:x:0:0:root:/root:/bin/sh" > etc/passwd
echo "root::13525:0:99999:7:::" > etc/shadow
echo "root:x:0:" > etc/group
echo "root:*::" > etc/gshadow
chmod 640 etc/shadow
chmod 640 etc/gshadow

echo " -- compress rootfs --> live/boot/rootfs.gz"
find . -print | cpio -o -H newc | gzip -9 > ../live/boot/rootfs.gz

cd ..


# configure bootloader
echo " -- copy isolinux.bin --> live/boot/isolinux"
cp /usr/lib/syslinux/isolinux.bin live/boot/isolinux

echo " -- create config for isolinux"
echo """default live
label live
	kernel /boot/vmlinuz
	append initrd=/boot/rootfs.gz rw root=/dev/null quiet
implicit 0
prompt 0
""" > live/boot/isolinux/isolinux.cfg


# copy linux kernel
echo " -- copy kernel -->  live/boot/vmlinuz"
for kernel in /boot/vmlinuz-*; do echo "    * $kernel" ; done
cp $kernel live/boot/vmlinuz
chmod a+rw live/boot/vmlinuz


# create iso image
echo " -- create iso Image"
genisoimage -R -o cd.iso -b boot/isolinux/isolinux.bin -no-emul-boot -boot-load-size 4 -V "Live" -input-charset iso8859-1 -boot-info-table live


# test with Qemu
# qemu-system-i386 -cdrom cd.iso
