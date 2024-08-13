from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QTimeEdit, QMessageBox, QDesktopWidget
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QFont
import webbrowser
import urllib.parse
import configparser
from utils import round_to_next_hour  # Ensure this import is present

class MeetingSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("QuickMeet")
        self.setFixedSize(450, 350)  # Increased size for better layout
        
        # Apply font settings
        self.set_font()
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add widgets with improved sizes
        self.subject_input = QLineEdit(self)
        self.subject_input.setPlaceholderText("Enter meeting subject")
        self.subject_input.setText(self.get_config_value('mail_subject'))
        self.subject_input.setMinimumHeight(40)  # Increased height
        self.subject_input.setFixedWidth(400)  # Adjusted width
        layout.addWidget(QLabel("Meeting Subject:"))
        layout.addWidget(self.subject_input)
        
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter email IDs (semicolon separated)")
        self.email_input.setText(self.get_config_value('mail_to'))
        self.email_input.setMinimumHeight(40)  # Increased height
        self.email_input.setFixedWidth(400)  # Adjusted width
        layout.addWidget(QLabel("Email IDs:"))
        layout.addWidget(self.email_input)
        
        self.date_picker = QDateEdit(self)
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDisplayFormat('yyyy-MM-dd')
        self.date_picker.setMinimumHeight(40)  # Increased height
        self.date_picker.setFixedWidth(400)  # Adjusted width
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.date_picker)
        
        self.time_picker = QTimeEdit(self)
        self.time_picker.setDisplayFormat('HH:mm')
        self.time_picker.setMinimumHeight(40)  # Increased height
        self.time_picker.setFixedWidth(400)  # Adjusted width
        layout.addWidget(QLabel("Start Time:"))
        layout.addWidget(self.time_picker)
        
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setMinimumHeight(40)  # Increased height
        self.ok_button.setFixedWidth(400)  # Adjusted width
        self.ok_button.clicked.connect(self.setup_meeting)
        layout.addWidget(self.ok_button)
        
        self.setLayout(layout)
        
        self.set_default_values()
        self.center()

    def set_font(self):
        font = QFont()
        font.setPointSize(12)  # Increased font size for better readability
        self.setFont(font)
        
    def set_default_values(self):
        now = QDateTime.currentDateTime()
        rounded_start_datetime = round_to_next_hour(now)
        self.date_picker.setDate(rounded_start_datetime.date())
        self.time_picker.setTime(rounded_start_datetime.time())

    def get_config_value(self, key):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('settings', key, fallback='')

    def setup_meeting(self):
        subject = self.subject_input.text() or self.get_config_value('mail_subject')
        email_ids = self.email_input.text() or self.get_config_value('mail_to')
        start_date = self.date_picker.date()
        start_time = self.time_picker.time()
        start_datetime = QDateTime(start_date, start_time)
        
        rounded_start_datetime = round_to_next_hour(start_datetime)
        self.date_picker.setDate(rounded_start_datetime.date())
        self.time_picker.setTime(rounded_start_datetime.time())
        
        start_time_python = rounded_start_datetime.toString('yyyy-MM-ddTHH:mm:ss')
        end_datetime = rounded_start_datetime.addSecs(3600)
        end_time_python = end_datetime.toString('yyyy-MM-ddTHH:mm:ss')

        if not email_ids:
            QMessageBox.warning(self, "Input Error", "Please enter email IDs.")
            return

        location = 'Meeting Location'
        body = (
            "Hello,\n\n"
            "I hope this message finds you well.\n\n"
            "I have scheduled a Teams meeting for us to further discuss the relevant topics. "
            "Please find the meeting details below and let me know if you need any adjustments.\n\n"
            "Looking forward to our discussion!\n"
        )
        
        body_encoded = urllib.parse.quote(body)
        
        outlook_link = (
            f"https://outlook.office.com/calendar/0/deeplink/compose?"
            f"subject={urllib.parse.quote(subject)}&startdt={start_time_python}&enddt={end_time_python}&"
            f"location={urllib.parse.quote(location)}&body={body_encoded}&to={urllib.parse.quote(email_ids.replace(';', ','))}"
        )
        
        webbrowser.open(outlook_link)
        self.accept()  # Only close the dialog, keep the app running

    def center(self):
        """Center the dialog on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
