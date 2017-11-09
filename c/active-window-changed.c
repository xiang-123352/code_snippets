static void
active_window_changed(WnckScreen *screen)
{
    WnckWindow *active_window = wnck_screen_get_active_window(screen);
    if (wnck_window_is_maximized(active_window)) {
        g_print("The active window is maximized\n");
    }
}

...
g_signal_connect(screen, "active-window-changed",
                 G_CALLBACK(active_window_changed), NULL);
...

