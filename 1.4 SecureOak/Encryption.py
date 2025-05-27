import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QFrame, QHBoxLayout
)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt

from cryptography.fernet import Fernet

# Generate and reuse key
key = Fernet.generate_key()
f = Fernet(key)

class ApexCryptingGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ApexCrypting GUI")
        self.setStyleSheet("background-color: #252525; color: #f0f0f0;")  # Darker background, lighter text
        self.setFont(QFont("Segoe UI", 10))

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("ApexCrypting")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Input Section
        input_frame = QFrame()
        input_layout = QVBoxLayout()
        input_frame.setStyleSheet("background-color: #333333; border-radius: 10px; padding: 10px;")  # Grouping
        self.input_label = QLabel("Enter text to encrypt:")
        self.input_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.input_text = QLineEdit()
        self.input_text.setStyleSheet("background-color: #404040; color: #ffffff; padding: 8px; border-radius: 8px; border: 1px solid #555555;") # Input field style
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_text)
        input_frame.setLayout(input_layout)
        main_layout.addWidget(input_frame)

        # Encrypt Button
        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.setStyleSheet("background-color: #007bff; color: white; padding: 10px; border-radius: 8px;") # Modern button
        self.encrypt_button.clicked.connect(self.encrypt_text)
        main_layout.addWidget(self.encrypt_button)

        # Encrypted Output Section
        output_frame = QFrame()
        output_layout = QVBoxLayout()
        output_frame.setStyleSheet("background-color: #333333; border-radius: 10px; padding: 10px;")
        self.encrypted_label = QLabel("Encrypted text:")
        self.encrypted_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.encrypted_output = QTextEdit()
        self.encrypted_output.setReadOnly(True)
        self.encrypted_output.setStyleSheet("background-color: #404040; color: #00ffcc; padding: 8px; border-radius: 8px; border: 1px solid #555555;") # Output style
        output_layout.addWidget(self.encrypted_label)
        output_layout.addWidget(self.encrypted_output)
        output_frame.setLayout(output_layout)
        main_layout.addWidget(output_frame)

        # Decrypt Button
        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.setStyleSheet("background-color: #28a745; color: white; padding: 10px; border-radius: 8px;")
        self.decrypt_button.clicked.connect(self.decrypt_text)
        main_layout.addWidget(self.decrypt_button)

        # Decrypted Output Section
        decrypted_output_frame = QFrame()
        decrypted_output_layout = QVBoxLayout()
        decrypted_output_frame.setStyleSheet("background-color: #333333; border-radius: 10px; padding: 10px;")
        self.decrypted_label = QLabel("Decrypted text:")
        self.decrypted_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.decrypted_output = QTextEdit()
        self.decrypted_output.setReadOnly(True)
        self.decrypted_output.setStyleSheet("background-color: #404040; color: #ffcc00; padding: 8px; border-radius: 8px; border: 1px solid #555555;")
        decrypted_output_layout.addWidget(self.decrypted_label)
        decrypted_output_layout.addWidget(self.decrypted_output)
        decrypted_output_frame.setLayout(decrypted_output_layout)
        main_layout.addWidget(decrypted_output_frame)

        self.setLayout(main_layout)
        self.encrypted_data = b''

    def encrypt_text(self):
        plain_text = self.input_text.text()
        if plain_text:
            self.encrypted_data = f.encrypt(plain_text.encode('utf-8'))
            self.encrypted_output.setText(self.encrypted_data.decode())

    def decrypt_text(self):
        if self.encrypted_data:
            decrypted = f.decrypt(self.encrypted_data).decode('utf-8')
            self.decrypted_output.setText(decrypted)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApexCryptingGUI()
    window.resize(500, 650)  # Slightly taller
    window.show()
    sys.exit(app.exec())