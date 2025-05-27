from dotenv import load_dotenv
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QGraphicsOpacityEffect, QDialog
)
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor
from PySide6.QtCore import Qt, QPropertyAnimation, QSize
from PySide6.QtWidgets import QGraphicsOpacityEffect

import json
import sys
import os
import tempfile
from cryptography.fernet import Fernet

import smtplib
from email.mime.text import MIMEText

# Encryption Key
key = b'tfn8u9wMbSl1etTRn5SSY3mK-GpQtpT1JUFxng4xywE='
f = Fernet(key)

# Email configuration (replace with your actual details)
EMAIL_ADDRESS = "Dev.team.secure.29@gmail.com"
load_dotenv()
EMAIL_PASSWORD = os.getenv('whlt mkhl flhq zjsm')

class RegistrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register Account")
        self.setFixedSize(350, 300)
        self.setStyleSheet(self.parent().style_sheet())  # Inherit main style

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setStyleSheet(self.parent().input_style("email.png")) # Assuming you have an email icon

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("New Username")
        self.user_input.setStyleSheet(self.parent().input_style("user.png"))

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("New Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet(self.parent().input_style("lock.png"))

        self.confirm_pass_input = QLineEdit()
        self.confirm_pass_input.setPlaceholderText("Confirm Password")
        self.confirm_pass_input.setEchoMode(QLineEdit.Password)
        self.confirm_pass_input.setStyleSheet(self.parent().input_style("lock.png"))

        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet(self.parent().button_style())
        self.register_btn.clicked.connect(self.register_user)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Create New Account", font=QFont("Segoe UI", 16, QFont.Bold), alignment=Qt.AlignCenter))
        layout.addWidget(self.email_input)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.confirm_pass_input)
        layout.addWidget(self.register_btn)
        self.setLayout(layout)

    def register_user(self):
        email = self.email_input.text()
        new_username = self.user_input.text()
        new_password = self.pass_input.text()
        confirm_password = self.confirm_pass_input.text()

        if not email or not new_username or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Error", "Invalid email address.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
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

            users = data.get("users", [])
            for user in users:
                if user['user'] == new_username:
                    QMessageBox.warning(self, "Error", "Username already exists.")
                    return
                if 'email' in user and user['email'] == email:
                    QMessageBox.warning(self, "Error", "Email address already registered.")
                    return

            users.append({"email": email, "user": new_username, "pass": new_password})
            data["users"] = users

            updated_data_bytes = json.dumps(data).encode('utf-8')
            encrypted_updated = f.encrypt(updated_data_bytes)
            with open('imp_1', 'wb') as file:
                file.write(encrypted_updated)

            QMessageBox.information(self, "Success", f"Account created successfully for {email}!")
            self.accept()  # Close the dialog

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error during registration: {e}")
        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass

class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Forgot Password")
        self.setFixedSize(350, 200)
        self.setStyleSheet(self.parent().style_sheet())

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.user_input.setStyleSheet(self.parent().input_style("user.png"))

        self.reset_btn = QPushButton("Forgot Password")
        self.reset_btn.setStyleSheet(self.parent().button_style())
        self.reset_btn.clicked.connect(self.send_password_email)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Recover Password", font=QFont("Segoe UI", 16, QFont.Bold), alignment=Qt.AlignCenter))
        layout.addWidget(QLabel("Enter your username to receive a password email."))
        layout.addWidget(self.user_input)
        layout.addWidget(self.reset_btn)
        self.setLayout(layout)

    def send_password_email(self):
        username = self.user_input.text()
        if not username:
            QMessageBox.warning(self, "Error", "Please enter your username.")
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
            password = data['users'][0]['pass']
            user_email = None
            for user in data.get("users", []):
                if user['user'] == username and 'email' in user:
                    user_email = user['email']
                    break

            if user_email:
                subject = "Password Request"
                body = f"You have requested the password for your account '{username}'. Your Password is {password}. If you did not request this, please ignore this email."

                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = user_email

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, [user_email], msg.as_string())

                QMessageBox.information(self, "Info", f"A password reset email has been sent to {user_email}.")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Username not found or no email associated with this account.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error sending reset email: {e}")
        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔒 Secure Login")
        self.setFixedSize(400, 380)  # Increased height
        self.setup_ui()
        self.fade_in()

    def style_sheet(self):
        return """
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #1a1a1a, stop:1 #121212);
            color: #e0e0e0;
            font-family: "Segoe UI";
        }
        """

    def input_style(self, icon_path):
        return f"""
        QLineEdit {{
            background-color: #252525;
            padding: 12px;
            padding-left: 40px; /* Space for icon */
            border: 2px solid #333;
            border-radius: 8px;
            font-size: 14px;
            color: #fff;
            selection-background-color: #2979ff;
            background-image: url({icon_path});
            background-repeat: no-repeat;
            background-position: 10px center;
        }}
        QLineEdit:focus {{
            border: 2px solid #2979ff;
            box-shadow: 0 0 5px #2979ff;
        }}
        """

    def button_style(self):
        return """
        QPushButton {
            background-color: #2979ff;
            color: white;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #1565c0;
        }
        QPushButton:pressed {
            background-color: #0d47a1;
        }
        """

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Welcome Back!")
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # User Input
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.user_input.setStyleSheet(self.input_style("user.png"))
        layout.addWidget(self.user_input)

        # Password Input
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet(self.input_style("lock.png"))
        layout.addWidget(self.pass_input)

        # Login Button
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.validate_login)
        self.login_btn.setStyleSheet(self.button_style())
        layout.addWidget(self.login_btn)

        # Bottom buttons layout
        bottom_layout = QHBoxLayout()
        self.register_btn = QPushButton("Register Account")
        self.register_btn.setStyleSheet(self.button_style())
        self.register_btn.clicked.connect(self.show_registration_dialog)
        bottom_layout.addWidget(self.register_btn)

        self.forgot_pass_btn = QPushButton("Forgot Password?")
        self.forgot_pass_btn.setStyleSheet(self.button_style())
        self.forgot_pass_btn.clicked.connect(self.show_forgot_password_dialog)
        bottom_layout.addWidget(self.forgot_pass_btn)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)
        self.setStyleSheet(self.style_sheet())

    def fade_in(self):
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

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

    def show_registration_dialog(self):
        dialog = RegistrationDialog(self)
        dialog.exec()

    def show_forgot_password_dialog(self):
        dialog = ForgotPasswordDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
