import sys
import signal

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from overlay import Overlay
from logReader import LogReader

if __name__ == "__main__":

    signal.signal( signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    overlay = Overlay([])
    overlay.show()

    log_reader = LogReader(overlay)

    timer = QTimer()
    timer.timeout.connect(
        log_reader.update_overlay
    )
    timer.start(100)

    sys.exit(app.exec())