from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
import json
import sys
import os
import tempfile
from cryptography.fernet import Fernet

# Replace with your actual key
key = b'tfn8u9wMbSl1etTRn5SSY3mK-GpQtpT1JUFxng4xywE='
f = Fernet(key)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Login")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #0000FF;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Welcome")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.validate_login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def validate_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both fields.")
            return

        try:
            with open('imp_1', 'rb') as file:
                encrypted = file.read()
            decrypted = f.decrypt(encrypted)
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
                tmp.write(decrypted)
                tmp_path = tmp.name

            with open(tmp_path, 'r') as f_:
                data = json.load(f_)

            for user in data.get("users", []):
                if user['user'] == username and user['pass'] == password:
                    QMessageBox.information(self, "Success", "Login successful!")
                    return

            QMessageBox.warning(self, "Failed", "Invalid credentials.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
