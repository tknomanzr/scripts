#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cpu.py
#  
#  Copyright 2017 William Bradley <tknomanzr@testbed>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import psutil
import sys
import pygtk, gobject
pygtk.require('2.0')
import gtk
from threading import Thread
class Per_Cpu:
	global labels 
	labels = []
	global vbox 
	vbox = gtk.VBox()
	
	def show_per_cpu(self):
		result = psutil.cpu_percent(interval=None, percpu=True)
		return result
		
	def destroy(self, widget, data=None):
		gtk.main_quit()
		return
	
	def threaded(self):
		thread = Thread(target=self.updateValues)
		thread.start()
		return True

	def updateValues(self):
		for label in labels:
				label.destroy()
		try:
			self.button
			self.button.destroy()
		except:
			pass
		result = self.show_per_cpu()
		# Add labels for each value in the result list.
		for i in result:
			msg = '<big>cpu ' + str(result.index(i)) + ': ' + str(i) + '</big>'
			self.label = gtk.Label()
			self.label.set_markup(msg)
			labels.append(self.label)
			vbox.pack_start(self.label, False)
		self.button = gtk.Button("Exit")
		self.button.connect("clicked", self.destroy, None)
		self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
		# This packs the button into the window (a GTK container).
		vbox.pack_start(self.button, False)
		self.window.show_all()
		return
		
	def __init__(self):
		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.window.set_title("Per CPU Usage")
		self.window.set_decorated(False)
		self.window.set_keep_above(True)
		self.window.move(200, 48)
		# Sets the border width of the window.
		self.window.set_border_width(2)
		# Create a widget container
		self.window.add(vbox)
		num_cpus = psutil.cpu_count(logical = True)
		msg = "<big>Showing results for " + str(num_cpus) + " logical cpu cores.</big>"
		self.label = gtk.Label()
		self.label.set_markup(msg)
		vbox.pack_start(self.label, False)
		# Add a button to exit the window
		self.updateValues()
		self.window.show_all()
		
	def main(self):
		# Ensure that only one instance of the program runs.
		try:
			import socket
			s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			## Create an abstract socket, by prefixing it with null. 
			s.bind( '\0postconnect_gateway_notify_lock') 
		except socket.error as e:
			error_code = e.args[0]
			error_string = e.args[1]
			print "Process already running (%d:%s ). Exiting" % ( error_code, error_string) 
			sys.exit (0) 
		gobject.timeout_add_seconds(1, self.threaded)
		gobject.threads_init()
		gtk.main()
		
if __name__ == "__main__":
	win = Per_Cpu()
	win.main()
