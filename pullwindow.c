#include <stdlib.h>
#include <gtk/gtk.h>
#include <gdk/gdkx.h>

typedef struct {
  GdkDisplay *display;
  GdkScreen *screen;
  gulong  xid;
  gchar *title;
  GdkPixbuf *icon;
  guint client_event_id;
  GtkWidget *status_window;
  const gchar *display_name;
} MovableWindow;


static void
client_cb (GtkWidget      *widget,
	   GdkEventClient *event,
	   gpointer        data)
{
  MovableWindow *movable = (MovableWindow *)data;
  GdkWindow *window;

  g_print ("got client message\n");

  if (event->data.l[0] == movable->xid)
    {
      const gchar *errormsg = NULL;
      GtkWidget *msg;

#if 1
      g_print ("old window %#lx\n", event->data.l[0]);
      g_print ("new window %#lx\n", event->data.l[2]);
#endif

      if (event->data.l[1] == GTK_WINDOW_CHANGE_SCREEN_SUCCESS)
	{
	  window = gdk_window_foreign_new_for_display (gdk_display_get_default (), 
						       event->data.l[2]);
	  
	  gdk_property_change (window, 
			       gdk_atom_intern ("HOME_DISPLAY", FALSE),
			       gdk_atom_intern ("UTF8_STRING", FALSE),
			       8,
			       GDK_PROP_MODE_REPLACE,
			       gdk_display_get_name (movable->display),
			       strlen (gdk_display_get_name (movable->display)) + 1);
	}
      else
	{
	  msg = gtk_message_dialog_new (NULL, 0,
					GTK_MESSAGE_ERROR,
					GTK_BUTTONS_OK,
					"Migration failed");
	  switch (event->data.l[1])
	    {
	    case GTK_WINDOW_CHANGE_SCREEN_NO_DISPLAY:
	      gtk_message_dialog_format_secondary_text (GTK_MESSAGE_DIALOG (msg), 
							"The remote application could not "
							"open the display \"%s\"",
							movable->display_name);
	      break;
	    case GTK_WINDOW_CHANGE_SCREEN_NO_SCREEN:
	      gtk_message_dialog_format_secondary_text (GTK_MESSAGE_DIALOG (msg), 
							"The remote application could not "
							"open the screen \"%s\"",
							movable->display_name);
	      break;
	    case GTK_WINDOW_CHANGE_SCREEN_NO_AUTH:
	      gtk_message_dialog_format_secondary_text (GTK_MESSAGE_DIALOG (msg), 
							"The remote application failed "
							"to authenticate");
	      break;
	    case GTK_WINDOW_CHANGE_SCREEN_FAILURE:
	      gtk_message_dialog_format_secondary_text (GTK_MESSAGE_DIALOG (msg), 
							"The remote application failed "
							"to migrate");
	      break;
	    case GTK_WINDOW_CHANGE_SCREEN_REFUSED:
	      gtk_message_dialog_format_secondary_text (GTK_MESSAGE_DIALOG (msg), 
							"The remote application refused "
							"to migrate");
	      break;
	    default:
	      break;
	    }
	  
	  gtk_dialog_run (GTK_DIALOG (msg));
	  
	}

      gtk_main_quit ();
    }
}

static void
send_change_display (GtkWidget     *item,
                     MovableWindow *movable)
{
  GdkWindow *window;
  GdkAtom atom;
  Atom xatom;
  GdkEventClient event;
  const gchar *display_name;

  atom = gdk_atom_intern ("_NET_CHANGE_DISPLAY", FALSE);
  xatom = gdk_x11_atom_to_xatom_for_display (movable->display, atom);

  g_signal_connect (movable->status_window,
		    "client-event", G_CALLBACK (client_cb), movable);

  window = gdk_window_foreign_new_for_display (movable->display, 
					       movable->xid);

  gdk_property_change (window, 
		       atom,
		       gdk_atom_intern ("UTF8_STRING", FALSE),
		       8,
		       GDK_PROP_MODE_REPLACE,
		       movable->display_name,
		       strlen (movable->display_name) + 1);
  
  event.type = GDK_CLIENT_EVENT;
  event.window = movable->status_window->window;
  event.data_format = 32;
  event.message_type = gdk_atom_intern ("WM_PROTOCOLS", FALSE);
  event.data.l[0] = xatom;
  event.data.l[1] = gtk_get_current_event_time ();
  event.data.l[2] = xatom;
  event.data.l[3] = GDK_WINDOW_XID (movable->status_window->window);
  gdk_event_send_client_message_for_display (movable->display, 
					     (GdkEvent *)&event,
					     movable->xid);
}

static gchar *
read_window_title (Display *xdisplay, 
		   XID      xid)
{
  Atom net_wm_name, type;
  gint format;
  gulong length, rest;
  guchar *data;
  gchar *title;

  net_wm_name = XInternAtom (xdisplay, "_NET_WM_NAME", FALSE);
  if (XGetWindowProperty (xdisplay, xid, net_wm_name, 0, 1024,
			  FALSE, AnyPropertyType, 
			  &type, &format, &length, 
			  &rest, &data) == Success)
    title = g_strdup (data);
  else
    title = g_strdup ("Unknown");

  XFree (data);

  g_print ("\ttitle %s\n", title);

  return title;
}

static GdkPixbuf *
read_window_icon (Display *xdisplay, 
		  XID      xid)
{
  Atom net_wm_icon, type;
  gint format;
  gulong length, rest;
  gulong *data;
  GdkPixbuf *pixbuf;
  gint i, width, height, start;
  guchar *p;
 
  net_wm_icon = XInternAtom (xdisplay, "_NET_WM_ICON", FALSE);
  if (XGetWindowProperty (xdisplay, xid, net_wm_icon, 0, G_MAXLONG,
			  FALSE, AnyPropertyType, 
			  &type, &format, &length, 
			  &rest, (guchar **)&data) == Success)
    {

      width = height = 1000;
      start = 0;
      i = 0;
      while (i < length)
	{
	  if (data[i] < width && data[i + 1] < height)
	    {
	      width = data[0];
	      height = data[1];
	      start = i;
	    }
	  i = i + 2 + data[i] * data[i + 1];
	}
	 
      p = g_malloc (width * height * 4);
      memcpy (p, &(data[start + 2]), width * height * 4);
      XFree (data);
   
      pixbuf = gdk_pixbuf_new_from_data (p, 
					 GDK_COLORSPACE_RGB, 
					 TRUE, 8, 
					 width, height, width * 4, 
					 NULL, NULL); 
      if (width > 24 || height > 24)
	{
	  GdkPixbuf *scaled = gdk_pixbuf_scale_simple (pixbuf, 24, 24, GDK_INTERP_NEAREST);
	  g_object_unref (pixbuf);

	  pixbuf = scaled;
	}

      g_print ("got icon %dx%d\n", width, height);      
    }
  else
    pixbuf = NULL;
 
  return pixbuf;
}

static GList *
collect_movable_windows (GdkDisplay *display)
{
  Display *xdisplay;
  MovableWindow *movable;
  GdkScreen *screen;
  GList *list = NULL;
  Atom type, type2, type3;
  gint format, format2, format3, i, j;
  gulong xid, root, *data, *data2, *data4;
  unsigned long rest, length, length2, length3;
  gchar *data3;
  Atom net_client_list, net_change_display, net_wm_name, net_wm_icon, wm_protocols;
  GdkPixbuf *pixbuf;

  xdisplay = GDK_DISPLAY_XDISPLAY (display);
  net_change_display = XInternAtom (xdisplay, "_NET_CHANGE_DISPLAY", FALSE);
  net_client_list = XInternAtom (xdisplay, "_NET_CLIENT_LIST", FALSE);
  wm_protocols = XInternAtom (xdisplay, "WM_PROTOCOLS", FALSE);

  for (i = 0; i < gdk_display_get_n_screens (display); i++)
    {
      screen = gdk_display_get_screen (display, i);
      root = GDK_WINDOW_XID (gdk_screen_get_root_window (screen));
      
      if (XGetWindowProperty (xdisplay, root, net_client_list, 0, 4096,
			      FALSE, AnyPropertyType, 
			      &type, &format, &length, 
			      &rest, (unsigned char **)&data) == Success)
	{
	  g_print ("_NET_CLIENT_LIST: %d\n", length);
	  for (i = 0; i < length; i++)
	    {
	      xid = data[i];
	      
	      g_print ("toplevel: %#x\n", xid);
	      if (XGetWindowProperty (xdisplay, xid, wm_protocols, 0, 256,
				      FALSE, AnyPropertyType, 
				      &type2, &format2, &length2, 
				      &rest, (unsigned char **)&data2) == Success)
		{
		  g_print ("\t%d protocols\n", length2);
		  for (j = 0; j < length2; j++)
		    {
		      if (net_change_display == data2[j])
			{
			  g_print ("\tshareable\n");
			  
			  movable = g_new0 (MovableWindow, 1);	

			  movable->display = display;
			  movable->screen = screen;
			  movable->xid = xid;
			  movable->title = read_window_title (xdisplay, xid);
			  movable->icon = NULL; /*read_window_icon (xdisplay, xid);*/

			  list = g_list_prepend (list, movable);

			  break;
			}
		    }
		}

	      XFree (data2);
	    }
	}

      XFree (data);
    }

  return list;
}

static void
usage (void)
{
  g_print ("usage: pullwindow <display>\n");
  exit (1);
}


int 
main (int argc, char *argv[])
{
  GdkDisplay *display;
  GtkWidget *status_window;
  gchar *display_name;
  gulong id;
  GList *list, *l;
  GtkWidget *menu;
  
  gtk_init (&argc, &argv);

  if (argc < 2)
    usage ();

  display_name = argv[1];

  display = gdk_display_open (display_name);

  if (!display)
    {
      GtkWidget *msg;

      msg = gtk_message_dialog_new_with_markup (NULL, 0,
						GTK_MESSAGE_ERROR,
						GTK_BUTTONS_OK,
						"<b>Cannot open display \"%s\"</b>",
						display_name);
      gtk_dialog_run (GTK_DIALOG (msg));

      exit (1);
    }

  status_window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  gtk_window_set_screen (GTK_WINDOW (status_window), 
			 gdk_display_get_default_screen (display));
  gtk_widget_realize (status_window);

  list = collect_movable_windows (display);

  if (list == NULL)
    {
      GtkWidget *msg;

      msg = gtk_message_dialog_new_with_markup (NULL, 0,
						GTK_MESSAGE_INFO,
						GTK_BUTTONS_OK,
						"<b>No shareable windows on display \"%s\"</b>",
						display_name);
      gtk_dialog_run (GTK_DIALOG (msg));

      exit (0);
    }

  for (l = list; l; l = l->next)
    {
      MovableWindow *movable = l->data;

      movable->status_window = status_window;
      movable->display_name = gdk_display_get_name (gdk_display_get_default ());
    }

  menu = gtk_menu_new ();
  gtk_widget_show (menu);

  for (l = list; l; l = l->next)
    {
      MovableWindow *movable = l->data;

      GtkWidget *item = gtk_image_menu_item_new_with_label (movable->title);
      if (movable->icon)
	{
	  GtkWidget *image = gtk_image_new_from_pixbuf (movable->icon);
	  gtk_image_menu_item_set_image (GTK_IMAGE_MENU_ITEM (item), image);
	}
      g_signal_connect (item, "activate", G_CALLBACK (send_change_display), movable);
      gtk_widget_show (item);
      gtk_menu_shell_append (GTK_MENU_SHELL (menu), item);
    }

  gtk_menu_popup (GTK_MENU (menu), NULL, NULL, NULL, NULL, 1, 0);

  gtk_main ();

  return 0;
}
