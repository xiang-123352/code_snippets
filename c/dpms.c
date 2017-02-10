#include <X11/Xlib.h>
#include <X11/extensions/dpms.h>

Display    *Xdisplay;
GdkDisplay *Gdisplay;
CARD16      monitor;
BOOL        dpms;

Gdisplay = gdk_display_get_default ();
Xdisplay = gdk_x11_display_get_xdisplay (Gdisplay);
DPMSInfo (Xdisplay, &monitor, &dpms);
if (monitor == DPMSModeOn) {
   stromfressende_rechnerei ();
}

