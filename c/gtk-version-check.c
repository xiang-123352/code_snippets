#include <gtk/gtk.h>
#include <glib/gprintf.h>

/* build it with: gcc gtk-version-check.c -o gtk-version-check $(pkg-config --cflags --libs gtk+-3.0) */

int main(int argc, char *argv[])
{
    /* Initialize GTK */
    gtk_init (&argc, &argv);

    g_printf("%d.%d.%d\n", gtk_major_version, gtk_major_version, gtk_minor_version, gtk_micro_version);
    return(0);
}

