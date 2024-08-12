from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
import sys
from dialog import MeetingSetupDialog  # Import the MeetingSetupDialog class from the dialog module

class TrayApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        
        # Set the application icon
        self.setWindowIcon(QIcon("icon.png"))

        # Create the system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self)

        # Create the context menu for the tray icon
        self.menu = QMenu()
        
        # Add actions to the context menu
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.quit)
        self.menu.addAction(self.exit_action)
        
        # Set the context menu and show the tray icon
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()
        
        # Connect the left click on the tray icon to show the meeting setup dialog
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # Left-click
            self.show_meeting_dialog()
    
    def show_meeting_dialog(self):
        dialog = MeetingSetupDialog()
        dialog.setWindowIcon(QIcon("icon.png"))  # Set the icon for the dialog
        dialog.exec_()

if __name__ == '__main__':
    app = TrayApp(sys.argv)
    sys.exit(app.exec_())
