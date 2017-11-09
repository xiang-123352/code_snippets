#!/bin/bash

#needs rsync syslinux genisoimage live-boot live-config squashfs-tools installed

#remove old work area
rm -rf  /home/makelive/work/

#create makelive area if missing and change permissions
mkdir -p "/home/makelive"
chmod 777 "/home/makelive/"

#create work folders
mkdir -p "/home/makelive/work/iso/live"
mkdir -p "/home/makelive/work/iso/isolinux"
mkdir -p "/home/makelive/work/myfs"

#copy some isolinux stuff from the system to the makelive work area
rsync -a /usr/lib/syslinux/isolinux.bin /home/makelive/work/iso/isolinux/
rsync -a /usr/lib/syslinux/vesamenu.c32 /home/makelive/work/iso/isolinux/

#copy the kernel from the system
rsync -L /vmlinuz /home/makelive/work/iso/live/

#copy the initrd from the system
rsync -L /initrd.img /home/makelive/work/iso/live/

#create the isolinux.cfg file
echo "
default /isolinux/vesamenu.c32
menu background         #00000000
menu color title        * #FFFFFFFF *
menu color border       * #00000000 #00000000 none
menu color sel          * #ffffffff #00000000 *
menu vshift 15
menu hshift 15
menu width 50

label default
        menu label press enter to boot
        menu default
        linux /live/vmlinuz
        initrd /live/initrd.img
        append boot=live quiet splash

" > /home/makelive/work/iso/isolinux/isolinux.cfg


#items to be excluded - edit as needed
echo "
/dev/*
/cdrom/*
/media/*
/swapfile
/mnt/*
/sys/*
/proc/*
/tmp/*
/run/*
/boot/grub/grub.cfg
/boot/grub/device.map
/var/lib/dhcp/*
/etc/udev/rules.d/*
/etc/fstab
/etc/mtab
/home/makelive

" > /tmp/makelive.list

#copy the system
rsync -a / /home/makelive/work/myfs/ --exclude-from=/tmp/makelive.list

#live system wants a fstab file
touch /home/makelive/work/myfs/etc/fstab

#squash the filesystem
mksquashfs /home/makelive/work/myfs/ /home/makelive/work/iso/live/filesystem.squashfs

#remove the copy of the filesystem to save some space before making the iso
rm -rf /home/makelive/work/myfs/

#create the iso
genisoimage -r -J -l -D -o /home/makelive/makelive.iso -cache-inodes \
-b isolinux/isolinux.bin -no-emul-boot -allow-limited-size -boot-load-size 4 \
-boot-info-table -input-charset UTF8 /home/makelive/work/iso/

#cleanup the work area
rm -rf  /home/makelive/work/

#make the iso a hybrid image
isohybrid /home/makelive/makelive.iso

#rename the iso to something unique
mv /home/makelive/makelive.iso /home/makelive/makelive_`date +%I%M_%Y%h%d`.iso

echo "
You can find the live image in the /home/makelive/ folder.
"

exit 0

