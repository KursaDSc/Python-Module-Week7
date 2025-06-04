import sys
from PyQt6.QtWidgets import QApplication
from views.login import LoginWindow

app = QApplication(sys.argv)

# Tooltip stilini tüm uygulama için ayarla
app.setStyleSheet("""
    QToolTip {
        background-color: #fff8dc;
        color: #222;
        border: 1px solid #a9a9a9;
    }
""")

window = LoginWindow()
window.show()
sys.exit(app.exec())
