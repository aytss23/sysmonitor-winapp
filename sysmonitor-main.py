from core.controller import SystemMonitorController 
from PyQt5.QtWidgets import QApplication
import sys

main_app = QApplication(sys.argv)

main_controller = SystemMonitorController()
main_app.aboutToQuit.connect(main_controller.app_closed)

sys.exit(main_app.exec_())
