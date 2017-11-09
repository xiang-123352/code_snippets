"""
This is a PyGTK program that displays tabbed-pages (GtkNotebook) that are
detachable and movable.

see http://www.pygtk.org/pygtk2tutorial/sec-Notebooks.html#notebookfig
"""

import gtk

__author__ = "Caleb P Burns"
__copyright__ = "Copyright (C) 2010 Caleb P Burns <cpburns2009@gmail.com>"
__license__ = "WTFPL License"
__version__ = "0.3"

class Tabs:
	"""
	This class displays tabbed-pages via a GtkNotebook in a window.
	"""
	
	def __init__(self):
		self.page_counter = 0	
	
		window = self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.connect('delete_event', self.delete_event)
		window.connect('destroy', self.destroy)
		window.set_border_width(0)
		window.set_default_size(400, 200)
		
		vbox = gtk.VBox()
		
		button = gtk.Button(stock=gtk.STOCK_ADD)
		button.connect('clicked', self.create_tab)
		button.show()
		vbox.pack_start(button, False, False, 2)
		
		hbox = gtk.HBox()
		
		notebook = self.notebook = gtk.Notebook()
		notebook.set_scrollable(True)
		notebook.set_size_request(196, 196)
		notebook.set_properties(group_id=0, tab_vborder=0, tab_hborder=1, tab_pos=gtk.POS_TOP)
		notebook.popup_enable()
		notebook.show()
		
		# Try drawing a black line.
		# NOTE: This doesn't work.
		#color = gtk.gdk.color_parse('green')
		#width, height = notebook.size_request()
		#gc = gtk.gdk.GC(notebook, foregroud=color, line_width=4, line_style=gtk.gdk.LINE_SOLID)
		#notebook.draw_line(gc, 0, 0, width, height)
		
		hbox.pack_start(notebook, True, True, 2)
		
		hbox.show()
		vbox.pack_start(hbox, False, False, 2)
		
		vbox.show()
		window.add(vbox)
		window.show()
		
	def __del__(self):
		if gtk.main_level():
			# Make sure we're actually in a gtk main-loop before we quit it.
			gtk.main_quit()
		del self.notebook
		del self.window
		
	def delete_event(self, widget, event, data=None):
		"""
		Called when this window is going to be closed (deleted). By returning false,
		the 'destroy' signal will be emitted to this window by GTK.
		"""
		return False
		
	def destroy(self, widget, data=None):
		"""
		Called when the gtk_widget_destroy() method is called on this window, or if
		the 'delete_event' signal callback returned False.
		"""
		gtk.main_quit()
		
	def destroy_tab(self, widget, data, page=None):
		"""
		Called when the close button on a tab is pressed.
		
		Arguments:
		widget -- (gtk.Widget) The target GTK widget.
		data -- (gtk.Widget) The 
		"""

		if not page or not issubclass(page.__class__, gtk.Widget):
			return False;
			
		page_num = self.notebook.page_num(page)
		self.notebook.remove_page(page_num)
		return True

	def create_tab(self, widget, data=None):
		"""
		Called when the 'Create Tab' button is pressed. This appends a new page to the
		notebook.
		"""
		page = gtk.Label('Page %i' % self.page_counter)
		page.show()
		
		tab = gtk.HBox()
		tab_label = gtk.Label('Tab %i' % self.page_counter)
		tab_label.show()
		tab.pack_start(tab_label)
		#tab_close = gtk.Button()
		#tab_close.set_image(gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU))
		#tab_close.set_relief(gtk.RELIEF_HALF)
		#tab_close.set_property('inner-border', 0)
		#tab_close.connect('clicked', self.destroy_tab, page)
		# RC STYLE WAS HERE ----
		#tab_close.set_name('notebook_tab_close')
		
		
		#tab_close.show()
		#pack_end(child, expand=True, fill=True, padding=0) http://www.pygtk.org/docs/pygtk/class-gtkbox.html#method-gtkbox--pack-end
		#tab.pack_end(tab_close, expand=True, fill=False, padding=0)

		'''
		So in order to have a custom button, we have to use a custom gtk.Image()
		HOWEVER, images cannot receive signals (events).  So we have to put the
		image inside of a special container that CAN receive events called a 
		'eventbox' - Fitting huh?
		The eventbox does add some oddities here and there... but overall its a
		great solution.
		'''

		eventbox = gtk.EventBox()
		eventbox.set_events(gtk.gdk.BUTTON_RELEASE)
		eventbox.connect('button-release-event', self.destroy_tab, page)
		image = gtk.Image()
		#image.set_size_request(12, 12)
		image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
		image.set_alignment(0, 0)
		image.set_padding(4, 0)
		image.show()
		eventbox.add(image)
		eventbox.show()

		tab.pack_end(eventbox, expand=False, fill=False, padding=0)

		tab.show()
		
		self.notebook.append_page(page, tab)
		self.notebook.set_tab_reorderable(page, True)
		self.notebook.set_tab_detachable(page, True)
		
		self.page_counter += 1
		
		
	def main(self):
		"""
		Starts GTK's main loop.
		"""
		gtk.main()


def main():
	tabs = Tabs()
	tabs.main()
	return 0
	

if __name__ == '__main__':
	main()

