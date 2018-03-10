using System.Collections;
 
public class Song
{
    public Song (string artist, string title)
    {
        this.Artist = artist;
        this.Title = title;
    }
 
    public string Artist;
    public string Title;
}
 
public class TreeViewExample
{
    public static void Main ()
    {
        Gtk.Application.Init ();
        new TreeViewExample ();
        Gtk.Application.Run ();
    }
 
    ArrayList songs;
 
    public TreeViewExample ()
    {
        songs = new ArrayList ();
 
        songs.Add (new Song ("Dancing DJs vs. Roxette", "Fading Like a Flower"));
        songs.Add (new Song ("Xaiver", "Give me the night"));
        songs.Add (new Song ("Daft Punk", "Technologic"));
 
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
 
        Gtk.ListStore musicListStore = new Gtk.ListStore (typeof (Song));
        foreach (Song song in songs) {
            musicListStore.AppendValues (song);
        }
 
        artistColumn.SetCellDataFunc (artistNameCell, new Gtk.TreeCellDataFunc (RenderArtistName));
        songColumn.SetCellDataFunc (songTitleCell, new Gtk.TreeCellDataFunc (RenderSongTitle));
 
        tree.Model = musicListStore;
 
        tree.AppendColumn (artistColumn);
        tree.AppendColumn (songColumn);
 
        window.ShowAll ();
 
    }
 
    private void RenderArtistName (Gtk.TreeViewColumn column, Gtk.CellRenderer cell, Gtk.TreeModel model, Gtk.TreeIter iter)
    {
        Song song = (Song) model.GetValue (iter, 0);
 
        if (song.Artist.StartsWith ("X") == true) {
            (cell as Gtk.CellRendererText).Foreground = "red";
        } else {
            (cell as Gtk.CellRendererText).Foreground = "darkgreen";
        }
 
        (cell as Gtk.CellRendererText).Text = song.Artist;
    }
 
    private void RenderSongTitle (Gtk.TreeViewColumn column, Gtk.CellRenderer cell, Gtk.TreeModel model, Gtk.TreeIter iter)
    {
        Song song = (Song) model.GetValue (iter, 0);
        (cell as Gtk.CellRendererText).Text = song.Title;
    }
 
}
