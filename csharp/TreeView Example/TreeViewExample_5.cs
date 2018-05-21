public class TreeViewExample
{
    public static void Main ()
    {
        Gtk.Application.Init ();
        new TreeViewExample ();
        Gtk.Application.Run ();
    }
 
    public TreeViewExample ()
    {
        Gtk.Window window = new Gtk.Window ("TreeView Example");
        window.SetSizeRequest (500,200);
 
        Gtk.TreeView tree = new Gtk.TreeView ();
        Gtk.ListStore musicListStore = new Gtk.ListStore (typeof (Gdk.Pixbuf),
            typeof (string),  typeof (string));
 
        tree.AppendColumn ("Icon", new Gtk.CellRendererPixbuf (), "pixbuf", 0);
        tree.AppendColumn ("Artist", new Gtk.CellRendererText (), "text", 1);
        tree.AppendColumn ("Title", new Gtk.CellRendererText (), "text", 2);
 
        musicListStore.AppendValues (new Gdk.Pixbuf ("TreeViewRupertIcon.png"),
            "Rupert", "Yellow bananas");
 
        tree.Model = musicListStore;
 
        window.Add (tree);
        window.ShowAll ();
    }
}
