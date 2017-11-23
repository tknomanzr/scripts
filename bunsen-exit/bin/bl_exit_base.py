import dbus

class BL_Exit_Base(object):

	def __init__(self):
		self.dbus_iface = None

	def setup_dbus_connection(self):
		try:
			bus = dbus.SystemBus()
			dbus_object = bus.get_object('org.freedesktop.login1',
										 '/org/freedesktop/login1')
			self.dbus_iface = dbus.Interface(dbus_object,
											 'org.freedesktop.login1.Manager')
		except bus.DBusException as e:
			self.on_error(str(e))

	def can_do_action(self, action):
		# There is no 'CanLogout' method
		if action == "Logout":
			return "yes"
		actionMethod = "Can{}".format(action)
		response = self.send_dbus(actionMethod)
		return str(response)

	def do_action(self, action):
		print_message("do_action: {}".format(action))
		self.send_dbus(action)

	def send_dbus(self, method):
		try:
			if self.dbus_iface is None:
				self.setup_dbus_connection()
			if method[:3] == "Can":
				command = "self.dbus_iface.{}()".format(method)
			else:
				command = "self.dbus_iface.{}(['True'])".format(method)
			response = eval(command)
			return str(response)
		except dbus.DBusException as e:
			self.on_error(str(e))

	def on_error(self, string):
		print_message("{} {}".format(__me__, string))
		sys.exit(1)

	def on_warning(self, string):
		print_message("{} {}".format(__me__, string))

	def openbox_exit(self):
		subprocess.check_output(["openbox", "--exit"])

	def logout(self):
		try:
			self.openbox_exit()
		except subprocess.CalledProcessError as e:
			self.on_error(e.output)

	def action_from_command_line(self, action):
		try:
			self.do_action(action)
		except (subprocess.CalledProcessError, CanDoItError, KeyError) as e:
			self.on_error(str(e))

	def main(self):
		opts = get_options()
		if opts.logout:
			self.logout()
		else:
			if opts.suspend:
				action = "suspend"
			elif opts.hibernate:
				action = "hibernate"
			elif opts.hybridsleep:
				action = "hybridsleep"
			elif opts.reboot:
				action = "reboot"
			elif opts.poweroff:
				action = "poweroff"
			self.setup_dbus_connection()
			self.action_from_command_line(actionToMethod[action])
