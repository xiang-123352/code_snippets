/* Compile using: gcc -lX11 -lXss idle.c */

#include <stdio.h>
#include <X11/extensions/scrnsaver.h>
#include <X11/Xlib.h>

void main(void) {
  XScreenSaverInfo *info = XScreenSaverAllocInfo();
  Display *display = XOpenDisplay(0);

  XScreenSaverQueryInfo(display, DefaultRootWindow(display), info);
  printf("%i\n", (info->idle) / 1000);
}

