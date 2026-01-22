import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

class Hilo1s(QThread):
    beep = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.is_running = True

    def run(self):
        self.is_running = True
        while self.is_running:
            time.sleep(1)
            self.beep.emit(True)

    def stop(self):
        self.is_running = False


