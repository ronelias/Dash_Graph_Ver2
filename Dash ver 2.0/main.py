"""Entry point for the DashGraph application."""

import sys
from PyQt5.QtWidgets import QApplication
from ui import DashGraphApp

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = DashGraphApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ Application crashed: {e}")
        sys.exit(1)