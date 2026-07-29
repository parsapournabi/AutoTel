from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSharedMemory, QElapsedTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction

from src.meta import resources_rc

NEXT_NOTIFICATION_DELAY = 5000


class CustomQMenu(QMenu):
    def __init__(self,
                 *args,
                 **kwargs):
        super(CustomQMenu, self).__init__(*args, **kwargs)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
                            QMenu {
                                background-color: #18191A;  /* Dark background for the menu */
                                color: #F9F9F9;              /* Light text color */
                                border: 1px solid #18191A;
                            }

                            QMenu::item {
                                background-color: #18191A;   /* Light background for menu items */
                                color: #F9F9F9;               /* Dark text color */
                                padding: 3px 5px;
                                height: 15px;
                                margin-bottom: 1px;
                                margin-top: 1px;
                                margin-left: 3px;
                            }

                            QMenu::item:selected {
                                background-color: orange;    /* Hover background color */
                                color: #FFFFFF;                /* White text color on hover */
                            }
                            """)

    def addAction(self, action: QAction):
        self.addSeparator()
        super().addAction(action)

    def addMenu(self, menu: 'QMenu'):
        self.addSeparator()
        super().addMenu(menu)


class QApplication(QtWidgets.QApplication):
    show_action: QAction = None
    hide_action: QAction = None
    mute_notification_action: QAction = None
    flatlay_action: QAction = None
    tray_icon: QSystemTrayIcon = None
    os_platform: str = ""  # [WINDOWS, MAC]
    base_social_tray_action_name: str = "TrayAction"
    regular_font_family: str = ""
    bold_font_family: str = ""
    italic_font_family: str = ""

    is_notification_muted: bool = False

    _next_notification_timer = QElapsedTimer()

    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.setAttribute(Qt.AA_EnableHighDpiScaling)
        self.setAttribute(Qt.AA_UseHighDpiPixmaps)
        QApplication.setApplicationName('WeaTel')
        # Create shared memory to check for other instances
        self.shared_memory = QSharedMemory("com.wearily.WeaTelApplication")

        # Create system tray icon
        QApplication.tray_icon = QSystemTrayIcon(QIcon(":/share/images/Wearily-Logo-AppIcon-Dark.ico"), self)
        QApplication.setApplicationName('WeaTel')
        QApplication.tray_icon.setToolTip("WeaTel")

        font = QtGui.QFont()
        font.setFamily("AvenirNext LT Pro Regular")
        font.setBold(True)
        font.setPointSize(10)
        font.setWeight(600)

        # Create a menu for the tray icon
        self.tray_menu = CustomQMenu()
        self.tray_menu.setFixedWidth(150)
        self.tray_menu.setFont(font)
        self.tray_menu_social_media = CustomQMenu(title="Social Medias")
        self.tray_menu_social_media.setFixedWidth(150)
        self.tray_menu_social_media.setFont(font)

        # Create Actions for QMenu tray icon
        flatlay_icon = QIcon()
        flatlay_icon.addPixmap(QtGui.QPixmap(":/share/images/Wearily-Logo-AppIcon-Dark.ico"), QIcon.Mode.Normal,
                               QIcon.State.Off)
        self.quit_action = QAction('Quit')
        QApplication.hide_action = QAction('Hide')
        QApplication.mute_notification_action = QAction("Mute")
        QApplication.mute_notification_action.triggered.connect(self._onMuteActionTriggered)

        # QApplication.flatlay_action = QAction()
        # QApplication.flatlay_action.setIcon(flatlay_icon)
        # QApplication.flatlay_action.setText("Copilot Login")

        # Creating Social Media Login Logout actions

        # for social_media in AvailableSocialMedias:
        #     action = QAction()
        #     setattr(QApplication,
        #             self.base_social_tray_action_name + social_media.Name,
        #             action)
        #     social_icon = QIcon()
        #     social_icon.addPixmap(QtGui.QPixmap(social_media.IconLoginPage), QIcon.Mode.Normal, QIcon.State.Off)
        #     action.setIcon(social_icon)
        #     action.setText(f"{social_media.Name} Login")
        #     action.setEnabled(False)

        QApplication.show_action = QAction("Show")

        # Action signals
        self.quit_action.triggered.connect(self._exit_app)

        # Add Actions to QTray menu
        self.tray_menu.addAction(QApplication.show_action)
        # self.tray_menu.addMenu(self.tray_menu_social_media)

        # Adding social Media Icon
        # for social_media in AvailableSocialMedias[::-1]:
        #     action = getattr(QApplication,
        #                      self.base_social_tray_action_name + social_media.Name)
        #     self.tray_menu_social_media.addAction(action)

        self.tray_menu.addAction(QApplication.mute_notification_action)
        self.tray_menu.addAction(QApplication.hide_action)
        self.tray_menu.addAction(self.quit_action)

        # Set the tray icon's context menu
        QApplication.tray_icon.setContextMenu(self.tray_menu)

        # Show the tray icon
        QApplication.tray_icon.show()

        # Initial value
        QApplication._next_notification_timer.start()

    @staticmethod
    def notification_show(data):
        """Sending OS System Notification -> title can be [info, Warning, Error]"""

        if QApplication.is_notification_muted:
            return

        message, title = data
        if title != "info" and QApplication._next_notification_timer.elapsed() < NEXT_NOTIFICATION_DELAY:
            return
        QApplication._next_notification_timer.restart()

        dict_icons: dict = {'Information': QSystemTrayIcon.Information,
                            'Warning': QSystemTrayIcon.Warning,
                            'Error': QSystemTrayIcon.Critical}
        title = title.replace('info', 'Information')
        QApplication.tray_icon.showMessage(title,
                                           message,
                                           dict_icons.get(title),
                                           10000)

    def check_if_another_instance(self):
        """Checks if another instance of the application is running."""
        if self.os_platform == "MAC":
            return True
        if not self.shared_memory.create(1):
            return False  # Shared memory already exists, meaning another instance is running.
        return True

    def _exit_app(self):
        self.shared_memory.detach()
        QApplication.quit()

    def _onMuteActionTriggered(self):
        QApplication.is_notification_muted = not QApplication.is_notification_muted
        self.mute_notification_action.setText("UnMute" if QApplication.is_notification_muted else "Mute")
