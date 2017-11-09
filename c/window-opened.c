geometry_changed(WnckWindow *window)
{
    if (wnck_window_is_maximized(window)) {
        g_print("A window has been maximized\n");
    }
}

static void
window_opened(WnckScreen *screen, WnckWindow *window)
{
    g_signal_connect(window, "geometry-changed",
                     G_CALLBACK(geometry_changed), NULL);

    /* Force a geometry-changed emission on already opened windows:
     * remove it if you need to catch only *new* maximizations */
    geometry_changed(window);
}

gint
main(gint argc, gchar *argv[])
{
    GMainLoop *loop;
    WnckScreen *screen;

    gdk_init(&argc, &argv);

    screen = wnck_screen_get(0);
    g_signal_connect(screen, "window-opened",
                     G_CALLBACK(window_opened), NULL);

    loop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(loop);
    g_main_loop_unref(loop);

    return 0;
}

