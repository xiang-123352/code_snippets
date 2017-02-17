#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <linux/input.h>
#include <sys/ioctl.h>

#ifndef EVIOCSREP
#define EVIOCSREP _IOW('E', 0x03, int[2])
#endif

/* compile with gcc -o setspeed setspeed.c */


int main(int argc, char** argv) {
   int retval = 0;
   int fd = 0;
   int rep[2];

   rep[0] = 400; // delay
   rep[1] = 200; // repeat rate

   if ((fd = open( "/dev/input/event4", O_RDWR )) < 0) {   // better use /dev/input/ir
       printf("unable to access /dev/input/event4, exiting..\n");
       exit(1);
   }
   if (ioctl(fd, EVIOCSREP, rep)) {
       perror("unable to set delay and repeat rate for input devices");
       exit(1);
   }

   close(fd);
}

