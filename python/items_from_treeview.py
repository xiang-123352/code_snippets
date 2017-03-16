#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def remove_selected_items (self):
	# get the file treeview and liststore
	file_view = self.ui.get_object ("tree_files")
	file_list = self.ui.get_object ("filelist")
	# get the selected rows as paths
	sel_model, sel_rows = file_view.get_selection ().get_selected_rows ()
	# store the treeiters from paths
	iters = []
	for row in sel_rows:
		iters.append ( file_list.get_iter (row) )
	# remove the rows (treeiters)
	for i in iters:
		if i is not None:
			file_list.remove (i)

