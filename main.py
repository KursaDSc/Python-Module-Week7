mport sys
from PyQt6.QtWidgets import QApplication

def main():
    from views.login import LoginWindow
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QToolTip {
            background-color: #fff8dc;
        color: #222;
        border: 1px solid #a9a9a9;
        }
    """)
    # Uygulama başlatma
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
