#/usr/bin/env python3
# -*- coding: utf-8 -*-

class my_context_manager:
  def __enter__(self):
    # set up things
    return thing
  
  def __exit__(self, type, value, traceback):
    # deal with unmanaged resources

with my_context_manager as custom_name:
  # work with resources
