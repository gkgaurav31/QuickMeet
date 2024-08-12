from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon
from dialog import MeetingSetupDialog

class TrayApp:
    def __init__(self, app):
        self.app = app

        # Create the system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self.app)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Create the context menu for the tray icon
        self.menu = QMenu()
        
        # Add actions to the context menu
        self.exit_action = QAction("Exit", self.app)
        self.exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.exit_action)
        
        # Set the context menu and show the tray icon
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()
    
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_dialog()
    
    def show_dialog(self):
        dialog = MeetingSetupDialog()
        dialog.exec_()  # Show the dialog and wait for user input

    def exit_app(self):
        self.app.quit()
