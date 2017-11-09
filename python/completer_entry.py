#!/usr/bin/env python
"""Modification of PyGTK's EntryCompletion example with shell-like tab completion.

Tab works normally unless there's content, the cursor is at the end of it,
and nothing is selected, preserving intuitive tab-cycling behaviour in all
reasonable cases while still allowing comfortable tab completion.
(To tab-cycle into a field with content in it and then tab-complete, just press
End before you request completion)

If no completions are found, users may press Tab again to go to the next field.

Also includes an adjustment to allow for specialized data sources to be hooked
in (eg. SQL databases) if writing a custom GTK+ Tree/List model class is more
hassle than it's worth.

@bug: The popup completion fails if the only focusable widget in the dialog is
	a single TabCompletionEntry unless you remove some of the checks.
	(At least event.state. I've no clue why.)

@bug: Either the "inline-completion" property is broken in GTK+ or I broke it.
	This isn't a problem unless you want automatic common-prefix completion on
	prefixes with multiple results.

@todo: Extend this so Tab also cycles through the list of possible completions.
@todo: Bring __init__'s API back in line with gtk.Entry for kwargs.
@todo: Is there a more reasonable way to pass in a non-changing completion model
	than passing "lambda : my_model" for completion_getter?
"""

import pygtk
pygtk.require('2.0')
import gtk

from gtk.keysyms import Tab as KEY_TAB

# https://translate.svn.sourceforge.net/svnroot/translate/src/trunk/virtaal/virtaal/views/widgets/textbox.py
MOD_MASK = ( gtk.gdk.CONTROL_MASK | gtk.gdk.MOD1_MASK |
        gtk.gdk.MOD4_MASK | gtk.gdk.SHIFT_MASK )

class TabCompletionEntry(gtk.Entry):
	def __init__(self, completion_getter):
		gtk.Entry.__init__(self)

		self.completion_getter = completion_getter
		self.completed = False # Used by "allow Tab-cycling after completion"
		self.completing = ''

		self.completion = gtk.EntryCompletion()
		self.completion.set_model(None) # EntryCompletion is overzealous.
		# Only give it a model when we've explicitly asked for completion.
		self.completion.set_inline_selection(True)
		self.set_completion(self.completion)
		self.completion.set_minimum_key_length(1)
		self.completion.set_text_column(0)

		self.connect('changed', self.content_changed_cb)
		self.connect('key-press-event', self.entry_keypress_cb)
		self.completion.connect('match-selected', self.match_cb)
		self.connect('activate', self.activate_cb)

	def activate_cb(self, widget):
		if False: #TODO: Call the validate-activation signal here.
			self.stop_emission('activate')
			#TODO: Roll in the rest of the code from the fork.

	def entry_keypress_cb(self, widget, event):
		prefix = self.get_text()

		if event.keyval == KEY_TAB and not event.state & MOD_MASK and (
				prefix and not self.get_selection_bounds() and
				self.get_position() == len(prefix) and
				not self.completed):
			liststore = self.completion_getter(prefix)

			if len(liststore) == 0:
				# Users can press Tab twice in this circumstance to confirm.
				self.completed = True
			if len(liststore) == 1:
				self.set_text(liststore[0][0])
				self.set_position(-1)
				self.completed = True
			else:
				self.completing = prefix
				self.completion.set_model(liststore)
				self.completion.complete()
				# GtkEntryCompletion apparently needs a little nudge
				gtk.main_do_event(gtk.gdk.Event(gtk.gdk.KEY_PRESS))
			return True
		else:
			self.completion.set_model(None)
			return False

	def content_changed_cb(self, widget):
		self.completed = False

	def match_cb(self, completion, model, iter):
		"""@note: This doesn't get called on inline completion."""
		print model[iter][0], 'was selected'
		self.completed = True
		self.completing = ''
		completion.set_model(None)
		return

def get_completion(prefix):
	print "TODO: Build completion list from DB"
	liststore = gtk.ListStore(str)
	for s in ['apple', 'banana', 'cap', 'comb', 'color',
			'dog', 'doghouse']:
		if s.startswith(prefix):
			liststore.append([s])
	return liststore

class EntryCompletionExample:
	def __init__(self):
		window = gtk.Window()
		window.connect('destroy', lambda w: gtk.main_quit())
		vbox = gtk.VBox()
		label = gtk.Label('Type a, b, c or d and Tab for completion.\n'
				'Press Tab when the field is empty to cycle focus.')
		vbox.pack_start(label)

		entry = TabCompletionEntry(get_completion)
		entry2 = TabCompletionEntry(get_completion)

		vbox.pack_start(entry)
		vbox.pack_start(entry2)
		window.add(vbox)
		window.show_all()
		entry.connect('activate', self.activate_cb)
		entry2.connect('activate', self.activate_cb)
		return

	def activate_cb(self, entry):
		if entry.get_text():
			print "TODO: Apply the tag"
			entry.set_text("")
		else:
			print "TODO: Go to the next image"
		return

if __name__ == "__main__":
	ee = EntryCompletionExample()
	gtk.main()

# vim: set noexpandtab: #
