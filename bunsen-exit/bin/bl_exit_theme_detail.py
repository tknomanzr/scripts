class BlexitThemeDetail():
        """
        :param value
        Value for the theme detail
        :param required
        When a theme detail is not configured for a theme, and the detail
        is configured as being required, the default detail value is substituted.
        When required is False, nothing is substituted and the detail is not set.
        Sane defaults are used.
        :param value_type
        'int' and 'float' are recognized.
        All else defaults to 'string
        """
        def __init__(self, value, required, value_type):
            self.value = value
            self.required = required
            self.value_type = value_type

    default_theme_settings = dict(
        name=BlexitThemeDetail('Dark Theme', False, 'string'),
        author=BlexitThemeDetail('MerlinElMago', False, 'string'),
        dialogHeight=BlexitThemeDetail(120, False, 'int'),
        sleepDelay=BlexitThemeDetail(0.003, False, 'float'),
        overallOpacity=BlexitThemeDetail(100, False, 'int'),
        buttonSpacing=BlexitThemeDetail(10, False, 'int'),
        iconpath=BlexitThemeDetail('/usr/share/images/bunsen/exit', True, 'string'),
        buttonImageCancel=BlexitThemeDetail('cancel.png', False, 'string'),
        buttonImagePowerOff=BlexitThemeDetail('poweroff.png', False, 'string'),
        buttonImageReboot=BlexitThemeDetail('reboot.png', False, 'string'),
        buttonImageSuspend=BlexitThemeDetail('sleep.png', False, 'string'),
        buttonImageLogout=BlexitThemeDetail('logout.png', False, 'string'),
        buttonImageHybridSleep=BlexitThemeDetail('hibernate.png', False, 'string'),
        buttonImageHibernate=BlexitThemeDetail('hibernate.png', False, 'string'),
        windowWidthAdjustment=BlexitThemeDetail(0, False, 'float')
    )
