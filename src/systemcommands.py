# Keypirinha | A semantic launcher for Windows | http://keypirinha.com

import keypirinha as kp
import keypirinha_util as kpu
from .lib import functions

class SystemCommands(kp.Plugin):
    """
    Provide system functions like show lockscreen or empty recycle bin
    """

    KEYWORD_EMPTY_RECYCLEBIN = "emptytrash"
    KEYWORD_SHOW_RECYCLEBIN = "trash"
    KEYWORD_LOCKSCREEN = "lock"    
    KEYWORD_LOGOUT = "logout"
    KEYWORD_SHUTDOWN = "shutdown"
    KEYWORD_RESTART = "restart"
    KEYWORD_SLEEP = "sleep"
    KEYWORD_HIBERNATE = "hibernate"

    _system_actions = {}
    
    def __init__(self):
        super().__init__()
    
    def __del__(self):
        self._clean_icons()

    def on_start(self):
        self._clean_icons()
        self._initialize_actions()

    def on_catalog(self):
        catalog = []
        
        for action_keyword, systemaction in self._system_actions.items():
            self.dbg('Creating catalogItem for action: ', systemaction.label, systemaction.description)
            catalog.append(self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label=systemaction.label,
                short_desc=systemaction.description,
                target=systemaction.label,
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.NOARGS,
                icon_handle=systemaction.icon_handle
            ))
                        
        self.set_catalog(catalog)

    def on_execute(self, item, action):
        if item and item.category() == kp.ItemCategory.KEYWORD:
            selected_action= self._system_actions[item.target()]
            self.dbg('Found catalogItem for action: ', selected_action.label)
            if selected_action:
                selected_action.action_to_call()

    def on_events(self, flags):
        if flags & kp.Events.PACKCONFIG:
            self.info("Configuration changed, rebuilding catalog...")
            self.on_catalog()

    def _clean_icons(self):
        for key, systemaction in self._system_actions.items():
            systemaction.icon_handle.free()

    def _initialize_actions(self):
        icon_empty_recycle_bin = self._load_resource_image('system-emptytrash-icon.png')
        icon_show_recycle_bin = self._load_resource_image('system-trashbin-icon.png')
        icon_lockscreen = self._load_resource_image('system-lock-icon.png')
        icon_logout = self._load_resource_image('system-logout-icon.png')
        icon_shutdown = self._load_resource_image('system-shutdown-icon.png')
        icon_restart = self._load_resource_image('system-restart-icon.png')
        icon_sleep = self._load_resource_image('system-sleep-icon.png')
        icon_hibernate = self._load_resource_image('system-hibernate-icon.png')

        self._system_actions[self.KEYWORD_EMPTY_RECYCLEBIN] = SystemAction(
            self.KEYWORD_EMPTY_RECYCLEBIN,
            'Empty the recycle bin.',
            icon_empty_recycle_bin,
            functions.EmptyRecycleBin
        )

        self._system_actions[self.KEYWORD_SHOW_RECYCLEBIN] = SystemAction(
            self.KEYWORD_SHOW_RECYCLEBIN,
            'Show the recycle bin.',
            icon_show_recycle_bin,
            functions.OpenRecycleBin
        )

        self._system_actions[self.KEYWORD_LOCKSCREEN] = SystemAction(
            self.KEYWORD_LOCKSCREEN,
            'Show the windows lockscreen.',
            icon_lockscreen,
            functions.LockWorkStation
        )

        self._system_actions[self.KEYWORD_LOGOUT] = SystemAction(
            self.KEYWORD_LOGOUT,
            'Logout current user.',
            icon_logout,
            functions.Logout
        )

        self._system_actions[self.KEYWORD_SHUTDOWN] = SystemAction(
            self.KEYWORD_SHUTDOWN,
            'Shutdown the computer.',
            icon_shutdown,
            functions.Shutdown
        )

        self._system_actions[self.KEYWORD_RESTART] = SystemAction(
            self.KEYWORD_RESTART,
            'Restart the computer.',
            icon_restart,
            functions.Restart
        )

        self._system_actions[self.KEYWORD_SLEEP] = SystemAction(
            self.KEYWORD_SLEEP,
            'Put the computer to sleep.',
            icon_sleep,
            functions.Sleep
        )

        self._system_actions[self.KEYWORD_HIBERNATE] = SystemAction(
            self.KEYWORD_HIBERNATE,
            'Hibernate the computer.',
            icon_hibernate,
            functions.Hibernate
        )

    def _load_resource_image(self, image_name):
        return self.load_icon('res://SystemCommands/icons/{}'.format(image_name))


class SystemAction():
    label = None
    description = None
    icon_handle = None
    action_to_call = None

    def __init__(self, label, description, icon_handle, action_to_call):
        self.label = label
        self.description = description
        self.icon_handle = icon_handle
        self.action_to_call = action_to_call