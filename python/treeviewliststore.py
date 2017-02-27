
import gtk

store = gtk.ListStore(int,str,str,str)
view = gtk.TreeView(model=store) # Associate the store with the view

column_int = gtk.TreeViewColumn('Integer') # These will be our column
column_str = gtk.TreeViewColumn('String')  #  headings in the TreeView widget

view.append_column(column_int) # Associate the columns with the TreeView
view.append_column(column_str) #

cell_int = gtk.CellRendererText()
cell_hex = gtk.CellRendererText()
cell_dec = gtk.CellRendererText()

column_int.pack_start(cell_int) # This column only has one CellRenderer

column_str.pack_start(cell_hex) # This column has two
column_str.pack_start(cell_dec) #

column_int.add_attribute(cell_int, 'text', 0)       # Associate col 0 of model with text of cell_int
column_int.add_attribute(cell_int, 'background', 3) # Associate col 3 of model with the cell background

column_str.add_attribute(cell_hex, 'text', 1)       # Associate col 1 of model with text of cell_hex
column_str.add_attribute(cell_dec, 'text', 2)       #    ditto for cell_dec
column_str.add_attribute(cell_hex, 'background', 3) # Associate col 3 of model with the cell background
column_str.add_attribute(cell_dec, 'background', 3) # Associate col 3 of model with the cell background

store.append([1,'0x01','1','red'])   # Add items to the store
store.append([2,'0x02','2','green']) #
store.append([3,'0x03','3','blue'])  #
store.append([4,'0x04','4','wheat']) #
store.append([5,'0x05','5','gray'])  #
store.append([0,'','',''])           #

window = gtk.Window()
window.add(view)

window.show_all()
window.connect('delete_event', gtk.main_quit)
gtk.main()
