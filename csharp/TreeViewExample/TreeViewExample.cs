#file: TreeViewExample.cs
//mcs -pkg:gtk-sharp TreeViewExample.cs
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
        // Create a Window
        Gtk.Window window = new Gtk.Window ("TreeView Example");
        window.SetSizeRequest (500,200);
 
        // Create our TreeView
        Gtk.TreeView tree = new Gtk.TreeView ();
 
        // Add our tree to the window
        window.Add (tree);
 
        // Create a column for the artist name
        Gtk.TreeViewColumn artistColumn = new Gtk.TreeViewColumn ();
        artistColumn.Title = "Artist";
 
        // Create a column for the song title
        Gtk.TreeViewColumn songColumn = new Gtk.TreeViewColumn ();
        songColumn.Title = "Song Title";
 
        // Add the columns to the TreeView
        tree.AppendColumn (artistColumn);
        tree.AppendColumn (songColumn);
 
        // Create a model that will hold two strings - Artist Name and Song Title
        Gtk.ListStore musicListStore = new Gtk.ListStore (typeof (string), typeof (string));
 
 
        // Assign the model to the TreeView
        tree.Model = musicListStore;
 
        // Show the window and everything on it
        window.ShowAll ();
    }
}
