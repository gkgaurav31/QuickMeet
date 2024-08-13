from PyQt5.QtWidgets import QApplication
from tray_app import TrayApp

def main():
    import sys
    app = QApplication(sys.argv)
    
    # Prevent the app from quitting when the dialog is closed
    app.setQuitOnLastWindowClosed(False)
    
    # Create the tray application instance
    tray_app = TrayApp(app)
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
