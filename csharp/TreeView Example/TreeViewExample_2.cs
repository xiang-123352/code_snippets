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
        window.Add (tree);
 
        Gtk.TreeViewColumn artistColumn = new Gtk.TreeViewColumn ();
        artistColumn.Title = "Artist";
 
        Gtk.CellRendererText artistNameCell = new Gtk.CellRendererText ();
 
        artistColumn.PackStart (artistNameCell, true);
 
        Gtk.TreeViewColumn songColumn = new Gtk.TreeViewColumn ();
        songColumn.Title = "Song Title";
 
        Gtk.CellRendererText songTitleCell = new Gtk.CellRendererText ();
        songColumn.PackStart (songTitleCell, true);
 
        tree.AppendColumn (artistColumn);
        tree.AppendColumn (songColumn);
 
        artistColumn.AddAttribute (artistNameCell, "text", 0);
        songColumn.AddAttribute (songTitleCell, "text", 1);
 
        Gtk.TreeStore musicListStore = new Gtk.TreeStore (typeof (string), typeof (string));
 
        Gtk.TreeIter iter = musicListStore.AppendValues ("Dance");
        musicListStore.AppendValues (iter, "Fannypack", "Nu Nu (Yeah Yeah) (double j and haze radio edit)");
 
        iter = musicListStore.AppendValues ("Hip-hop");
        musicListStore.AppendValues (iter, "Nelly", "Country Grammer");
 
        tree.Model = musicListStore;
 
        window.ShowAll ();
    }
}
