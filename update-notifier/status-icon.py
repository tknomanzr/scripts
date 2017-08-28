#!/usr/bin/env python

# found on <http://files.majorsilence.com/rubbish/pygtk-book/pygtk-notebook-html/pygtk-notebook-latest.html#SECTION00430000000000000000>
# simple example of a tray icon application using PyGTK
# Modified as a possible gtk icon for the system tray that will act as an
# update notification system
import gtk
import subprocess
 
def message(data=None):
	"Function to display messages to the user."
	msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK_CANCEL)
	h_button_box=msg.vbox.get_children()[1]
	ok_button=h_button_box.get_children()[0]
	ok_button.grab_default()
	response = msg.run
	if response==gtk.RESPONSE_OK:
		subprocess.call(["x-terminal-emulator --command=~/bin/bl-updates"], shell=True)
	else:
		  gtk.main_quit()
def close_app(data):
		gtk.main_quit()
def make_menu(event_button, event_time, data=None):
  menu = gtk.Menu()
  close_item = gtk.MenuItem("Close this notification")
  
  #Append the menu items  
  menu.append(close_item)
  #add callbacks
  #open_item.connect_object("activate", open_app, "Open App")
  close_item.connect_object("activate", close_app, "Closing this notification")
  #Show the menu items
  #open_item.show()
  close_item.show()
  
  #Popup the menu
  menu.popup(None, None, None, event_button, event_time)
 
def on_right_click(data, event_button, event_time):
  make_menu(event_button, event_time)
 
def on_left_click(event):
  message("Run upgrade?")
  
if __name__ == '__main__':
	icon = gtk.status_icon_new_from_icon_name("update-notifier")
	icon.connect('popup-menu', on_right_click)
	icon.connect('activate', on_left_click)
	gtk.main()
