import webbrowser
from keypress import key_press
import sys
import time

def open_zoom_link(link):
    webbrowser.open(link)
    time.sleep(2)
    key_press("TAB")
    key_press("TAB")
    key_press("ENTER")
    
    
params = sys.argv
zoom_link = params[1]
open_zoom_link(zoom_link)