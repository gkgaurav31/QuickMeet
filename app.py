from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QAction, QDialog, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton, QDateEdit, QTimeEdit, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, QDate, QTime
import webbrowser
import sys
import urllib.parse

class MeetingSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("QuickMeet")
        self.setFixedSize(350, 300)  # Increased size to accommodate the subject field
        
        layout = QVBoxLayout()
        
        self.subject_input = QLineEdit(self)
        self.subject_input.setPlaceholderText("Enter meeting subject")
        self.subject_input.setText("Meeting Invite")  # Default value
        layout.addWidget(QLabel("Meeting Subject:"))
        layout.addWidget(self.subject_input)
        
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter email IDs (semicolon separated)")
        layout.addWidget(QLabel("Email IDs:"))
        layout.addWidget(self.email_input)
        
        self.date_picker = QDateEdit(self)
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDisplayFormat('yyyy-MM-dd')
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.date_picker)
        
        self.time_picker = QTimeEdit(self)
        self.time_picker.setDisplayFormat('HH:mm')
        layout.addWidget(QLabel("Start Time:"))
        layout.addWidget(self.time_picker)
        
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.setup_meeting)
        layout.addWidget(self.ok_button)
        
        self.setLayout(layout)
        
        self.set_default_values()

    def set_default_values(self):
        """Set the default values for date and time."""
        now = QDateTime.currentDateTime()
        rounded_start_datetime = self.round_to_next_hour(now)
        self.date_picker.setDate(rounded_start_datetime.date())
        self.time_picker.setTime(rounded_start_datetime.time())

    def round_to_next_hour(self, dt):
        """Round the given datetime to the next hour if minutes or seconds are not zero."""
        time = dt.time()
        if time.minute() == 0 and time.second() == 0:
            return dt
        # Round up to the next hour
        return dt.addSecs(3600 - (time.minute() * 60 + time.second()))

    def setup_meeting(self):
        subject = self.subject_input.text() or "Meeting Invite"
        email_ids = self.email_input.text()
        start_date = self.date_picker.date()
        start_time = self.time_picker.time()
        start_datetime = QDateTime(start_date, start_time)
        
        # Round up to the next hour and set as start time
        rounded_start_datetime = self.round_to_next_hour(start_datetime)
        self.date_picker.setDate(rounded_start_datetime.date())
        self.time_picker.setTime(rounded_start_datetime.time())
        
        start_time_python = rounded_start_datetime.toString('yyyy-MM-ddTHH:mm:ss')
        end_datetime = rounded_start_datetime.addSecs(3600)  # End time is 1 hour later
        end_time_python = end_datetime.toString('yyyy-MM-ddTHH:mm:ss')

        if not email_ids:
            QMessageBox.warning(self, "Input Error", "Please enter email IDs.")
            return

        location = 'Meeting Location'
        body = (
            "<p>Hello,</p>"
            "<p>I hope this message finds you well.</p>"
            "<p>I have scheduled a Teams meeting for us to further discuss the relevant topics. "
            "Please find the meeting details below and let me know if you need any adjustments.</p>"
            "<p>Looking forward to our discussion!</p>"
        )
        
        # Encode the body for URL
        body_encoded = urllib.parse.quote(body)
        
        # Create the deep link for Outlook web
        outlook_link = (
            f"https://outlook.office.com/calendar/0/deeplink/compose?"
            f"subject={urllib.parse.quote(subject)}&startdt={start_time_python}&enddt={end_time_python}&"
            f"location={urllib.parse.quote(location)}&body={body_encoded}&to={urllib.parse.quote(email_ids.replace(';', ','))}"
        )
        
        # Open the link in the default web browser (Outlook)
        webbrowser.open(outlook_link)

        self.accept()

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
