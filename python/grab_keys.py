from Xlib import Xatom, Xutil
from Xlib.display import Display, X
import sys
import signal 
import random
 
class bunch(dict):
  __getattr__ = dict.__getitem__
  __setattr__ = dict.__setitem__
 
def check_for_magic_keys(state, event):
  keys = state['keys']
  if event.type == X.KeyPress:
    keys[event.detail] = True
  elif event.type == X.KeyRelease:
    keys[event.detail] = False
 
  keycode_alt = 64
  keycode_1 = 10
  keycode_delete = 119
 
  magic_keys = keys.get(keycode_alt) and keys.get(keycode_1) and keys.get(keycode_delete)
  if magic_keys:
    print("Magic keys pressed, exiting")
    return True
 
  return False
 
def random_color(screen):
  red = random.randrange(0, 65536)
  green = random.randrange(0, 65536)
  blue = random.randrange(0, 65536)
 
  return screen.default_colormap.alloc_color(red, green, blue).pixel
 
def random_rectangle(screen, window):
  x = random.randrange(0, screen.width_in_pixels)
  y = random.randrange(0, screen.height_in_pixels)
  width = random.randrange(0, screen.width_in_pixels - x)
  height = random.randrange(0, screen.height_in_pixels - y)
 
  window.window.fill_rectangle(
    gc = window.gc,
    x = x,
    y = y,
    width  = width,
    height = height,
  )
 
def draw(state, event):
  screen = state.display.screen()
  foreground = random_color(screen)
  background = random_color(screen)
 
  state.window.gc.change(
    foreground = foreground,
    background = background,
  )
 
  random_rectangle(screen, state.window)
 
def handle_event(state, event):
  debug = False
  if debug:
    print(event)
    return True
 
  if check_for_magic_keys(state, event):
    return False
 
  draw(state, event)
  return True
 
def grab_keyboard_and_mouse(root):
  root.grab_keyboard(
    owner_events = True,
    pointer_mode = X.GrabModeAsync,
    keyboard_mode = X.GrabModeAsync,
    time = X.CurrentTime
  )
   
  root.grab_pointer(
    owner_events = True,
    event_mask = X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask,
    pointer_mode = X.GrabModeAsync,
    keyboard_mode = X.GrabModeAsync,
    confine_to = 0,
    cursor = 0,
    time = X.CurrentTime
  )
 
def create_window(display, root):
  screen = display.screen()
 
  window = root.create_window(
    x = 0,
    y = 0,
    width = screen.width_in_pixels,
    height = screen.height_in_pixels,
    border_width = 0,
    depth = screen.root_depth)
   
  atom_net_wm_state = display.intern_atom('_NET_WM_STATE', True)
  atom_net_wm_state_fullscreen = display.intern_atom('_NET_WM_STATE_FULLSCREEN', True)
 
  window.change_property(
    property = atom_net_wm_state,
    type = Xatom.ATOM,
    format = 32,
    data = [atom_net_wm_state_fullscreen], 
  )
 
  window.set_wm_normal_hints(
    flags = Xutil.PPosition | Xutil.PSize | Xutil.PMinSize,
    min_width = screen.width_in_pixels,
    min_height = screen.height_in_pixels,
  )
 
  gc = window.create_gc(
    foreground = screen.black_pixel,
    background = screen.white_pixel,
  )
 
  return bunch(window = window, gc = gc)
 
def event_loop(state):
  display = state.display
 
  while True:
    event = display.next_event()
    display.allow_events(
      mode = X.AsyncBoth,
      time = X.CurrentTime)            
 
    if not handle_event(state, event):
      break
 
def main():
  display = Display()
  root = display.screen().root
 
  grab_keyboard_and_mouse(root)
  window = create_window(display, root)
  window.window.map()
 
  state = bunch(
    display = display,
    root = root,
    window = window,
    keys = bunch())
 
  # Comment these out after you have confirmed the magic key works
  signal.signal(signal.SIGALRM, lambda a, b: sys.exit(1))
  signal.alarm(4)
 
  event_loop(state)
 
if __name__ == '__main__':
  main()
