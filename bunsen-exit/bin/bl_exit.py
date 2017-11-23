import ConfigParser
import pygtk
import gtk
from bl_exit_base import BL_Exit_Base
pygtk.require('2.0')


class BL_Exit(BL_Exit_Base):
    """A dialog offering the user to log out, suspend, reboot or shut down.
    """

    def __init__(self, cp, config_file):
        BL_Exit_Base.__init__(self)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_name('BL Exit')
        self.cp = cp
        self.config_file = config_file
        self.debug = False
        self.selectedAction = None
        self.window.set_decorated(True)
        self.window.connect("delete_event", self.destroy)
        self.window.connect("destroy_event", self.destroy)
        # Keyboard events will need to be handled here.
        # We need one that monitors for a focus change
        # And changes the background to the same color
        # As the value stored in the rc file
        #
        # a Listener for <-- and --> keys, also tab and shift-tab
        # This listener will set the focus on the next or previous
        # button in the array, we hope.
        #
        # An enter listener can throw an on_click
        #
        # We will be sure to also set focus on_click later, when
        # Buttons are created.
        self.window.set_resizable(False)
        self.window.set_keep_above(True)
        self.window.stick()
        self.window.set_position(gtk.WIN_POS_CENTER)
        windowicon = self.window.render_icon(gtk.STOCK_QUIT,
                                             gtk.ICON_SIZE_DIALOG)
        self.window.set_icon(windowicon)

    def configure(self):
        if self.config_file:
            try:
                self.cp.read(self.config_file)
            except ConfigParser.ParsingError as e:
                # Log a [DEBUG} message here
                print_message("{}: {}".format(__me__, str(e)))
                sys.exit(1)
        else:
            # No config file present:
            # self.cp.add_section("Default")
            # NOTE: add_section raises value error when the section name
            # evaluates to DEFAULT (or any of its case-insensitive
            # variants)
            for section in "hibernate", "hybridsleep":
                self.cp.add_section(section)
                self.cp.set(section, "show", "never")
            for section in "cancel", "logout", "suspend", "reboot", "poweroff":
                self.cp.add_section(section)
                self.cp.set(section, "show", "always")

    def set_custom_style(self):
        try:
            stylesdir = self.cp.get('style', 'dir')
            rcfile = self.cp.get('style', 'rcfile')
            stylerc = os.path.join(os.path.dirname(self.config_file, stylesdir, rcfile))
            if not os.path.isfile(stylerc):
                self.on_debug("custom style rc file does not exist")
                return None
            gtk.rc_parse(stylerc)
            settings = gtk.settings_get_for_screen(self.window.get_screen())
            gtk.rc_reset_styles(settings)
        except:
            # Log a [DEBUG] Message here
            self.on_debug("custom style not configured or parse error")
            pass

    def construct_ui(self):
        self.window.set_title("Log out " + getpass.getuser() + "?")
        self.window.height = 80
        # This accelerator may not be needed
        # Cancel key (Escape)
        accelgroup = gtk.AccelGroup()
        key, mod = gtk.accelerator_parse('Escape')
        accelgroup.connect_group(key, mod, gtk.ACCEL_VISIBLE, gtk.main_quit)
        self.window.add_accel_group(accelgroup)

        self.button_width = 100
        self.button_height = 50
        self.button_border_width = 4
        self.window.set_border_width(10)
        self.button_box = gtk.HButtonBox()
        self.button_box.set_spacing(0)
        self.button_box.set_layout(gtk.BUTTONBOX_SPREAD)
        self.build_button_visibility_array()
        visible_button_count = 0
        for button in self.bva:
            (action, label, actionfunc, method, show, onError) = button
            if not show == 0:
                visible_button_count += 1
                self.add_button(show, actionfunc, label=label)
        self.status = gtk.Label()
        label_box = gtk.HBox()
        label_box.pack_start(self.status)

        # allow for username of about twenty characters: len(title) + 200
        # approximation: counting characters, not size of rendered string
        if visible_button_count == 0:
            self.window.width = len(title) + 300
        elif visible_button_count <= 2:
            self.window.width = max(
                (self.button_width + 10) * visible_button_count,
                len(title) + 300)
        else:
            self.window.width = -1
        self.window.set_size_request(self.window.width, self.window.height)
        vbox = gtk.VBox()
        vbox.pack_start(self.button_box)
        vbox.pack_start(label_box)
        self.window.add(vbox)
        self.window.show_all()

    def destroy(self, widget=None, event=None, data=None):
        self.window.hide_all()
        gtk.main_quit()

    def build_button_visibility_array(self):
        """Determine button visibily using bl-exit configuration file.
        Build self.bva, an array of tuples, one entry per button,
        containing (action, label, actionfunction, actionMethod, show,
        onerror)
        """
        self.bva = []
        bva = [
            ('cancel', '_Cancel', self.cancel_action),
            ('logout', '_Log out', self.logout_action),
            ('suspend', '_Suspend', self.suspend_action),
            ('hibernate', 'H_ibernate', self.hibernate_action),
            ('hybridsleep', 'H_ybrid sleep', self.hybridsleep_action),
            ('reboot', 'Re_boot', self.reboot_action),
            ('poweroff', '_Power off', self.shutdown_action)
        ]
        show_values = dict(never=0, always=1, maybe=2)
        """Values that the 'show' keyword can take in the configuration
        file."""
        onerror_values = dict(novisual=0, visual=1)
        """Values that the 'onerror' keyword can take in the configuration
        file."""
        # Per button default settings
        per_button_show_defaults = dict(
            cancel='always',
            logout='always',
            suspend='always',
            hibernate='never',
            hybridsleep='never',
            reboot='always',
            poweroff='always'
        )
        for (action, label, actionfunction) in bva:
            # Defaults.
            show = show_values[per_button_show_defaults[action]]
            onError = onerror_values['novisual']
            for section in ['default', action]:
                try:
                    try:
                        getshow = self.cp.get(section, 'show')
                        if getshow in show_values:
                            show = show_values[getshow]
                            if show == 2:
                                candoit = self.can_do_action(
                                    actionToMethod[action])
                                if not candoit == 'yes':
                                    show = 3
                        self.on_debug("config section {} show={}".format(section, show))
                    except ConfigParser.NoOptionError as e:
                        self.on_debug("config section {}  no option show".format(section))
                        pass

                    try:
                        getonerror = self.cp.get(section, 'onerror')
                        if getonerror in onerror_values:
                            onError = onerror_values[getonerror]
                        self.on_debug("config section {} onerror={}".format(section, onError))
                    except ConfigParser.NoOptionError as e:
                        self.on_debug("config section {} no option onerror".format(section))
                        pass
                except ConfigParser.NoSectionError as e:
                    self.on_debug("config section {} not present".format(section))
                    pass

            self.bva.append(tuple([action, label, actionfunction,
                                   actionToMethod[action], show,
                                   onError]))

    def main(self):
        self.configure()
        self.set_custom_style()
        self.construct_ui()
        gtk.main()

    def add_button(self, show, action, label=None, stock=None):
        if stock is not None:
            button = gtk.Button(stock=stock)
        else:
            button = gtk.Button(label=label)
        button.set_size_request(self.button_width, self.button_height)
        if show == 3:
            button.set_sensitive(False)
        button.set_border_width(self.button_border_width)
        button.connect("clicked", action)
        self.button_box.pack_start(button)

    def disable_buttons(self):
        """Method that disables all button in the program
        Takes: No arguments.
        Returns: Nothing."""
        self.button_box.foreach(lambda button:
                                button.set_sensitive(False))

    def get_error(self):
        """Method that retrieves an errors from the button array.
        Takes: No arguments.
        Returns: The error."""
        error = 0
        if self.selectedAction is not None:
            for item in self.bva:
                (action, label, actionfunction, actionMethod, show,
                 error) = item
                if action == self.selected_action:
                    return error
        return error

    def on_error(self, err):
        """Method that logs or displays errors.
        Takes: the error as an argument.
        Returns: Nothing."""
        error = self.get_error()
        if error == 0:
            print_message("{}: {}".format(__me__, str(err)))
            sys.exit(1)
        else:
            emDialog = gtk.MessageDialog(parent=None, flags=0,
                                         type=gtk.MESSAGE_INFO,
                                         buttons=gtk.BUTTONS_OK,
                                         message_format=None)
            if emDialog:
                emDialog.set_markup("{}".format(err))
                emDialog.run()

    def on_warning(self, err):
        """Method that logs debug warnings.
        Takes: the error as an argument.
        Returns: nothing."""
        err = "{} {}".format(__me__, str(err))
        if self.debug:
            err = "DEBUG {}".format(err)
        print_message(err)

    def on_debug(self, err):
        """Method that issues warning if debugging is toggled on.
        Takes: the error as an argument.
        Returns: Nothing."""
        if self.debug:
            self.on_warning(err)

    def cancel_action(self):
        """Method that cancels the logout window.
        Takes: no arguments.
        Returns: nothing."""
        self.disable_buttons()
        gtk.main_quit()

    def logout_action(self):
        """Method that logs the user out.
        Takes: no arguments.
        Returns: nothing."""
        self.disable_buttons()
        self.selected_action = 'logout'
        self.status.set_label("Exiting Openbox, please standby...")
        self.openbox_exit()
        self.destroy()

    def suspend_action(self):
        """Method that suspends the machine.
        Takes: no arguments.
        Returns: nothing."""
        self.disable_buttons()
        self.selected_action = 'suspend'
        self.status.set_label("Suspending, please standby...")
        self.do_action("Suspend")
        self.destroy()

    def hibernate_action(self):
        """Method that hibernates the machine.
        Takes: no arguments.
        Returns: nothing"""
        self.disable_buttons()
        self.selected_action = 'hibernate'
        self.status.set_label("Hibernating, please standby...")
        self.do_action("Hibernate")
        self.destroy()

    def hybridsleep_action(self):
        """Method that enables hybrid sleep
        Takes: no arguments.
        Returns: nothing."""
        self.disable_buttons()
        self.selected_action = 'hybridsleep'
        self.status.set_label("Hibernating + Sleeping, please standby...")
        self.do_action("HybridSleep")
        self.destroy()

    def reboot_action(self):
        """Method that reboots the machine
        Takes: no arguments.
        Returns: nothing."""
        self.disable_buttons()
        self.selected_action = 'reboot'
        self.status.set_label("Rebooting, please standby...")
        self.do_action("Reboot")
        self.destroy()

    def shutdown_action(self):
        """ Method that powers off the machine.
        Takes: No arguments.
        Returns: Nothing """
        self.disable_buttons()
        self.selected_action = 'poweroff'
        self.status.set_label("Shutting down, please standby...")
        self.do_action("PowerOff")
        self.destroy()
