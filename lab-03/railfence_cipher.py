# -*- coding: utf-8 -*-
import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_RailFence

# Tắt cảnh báo debug của Qt
os.environ["QT_LOGGING_RULES"] = "qt5ct.debug=false"
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(__file__), 'platforms')

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RailFence()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        plain_text = self.ui.textBrowser.toPlainText().strip()
        key_input = self.ui.textBrowser_2.toPlainText().strip()

        if not plain_text or not key_input:
            QMessageBox.warning(self, "Input Error", "Please enter both plain text and number of rails.")
            return

        try:
            if key_input.isdigit():
                key = int(key_input)
            elif len(key_input) == 1 and key_input.lower() in 'abcdefghijklmnopqrstuvwxyz':
                key = ord(key_input.lower()) - ord('a') + 1
            else:
                raise ValueError

            print(f"Key after conversion from input '{key_input}':", key)

            if key < 2:
                QMessageBox.warning(self, "Input Error", f"Converted key '{key_input}' = {key} is too small. Minimum is 2.")
                return
            if key > len(plain_text):
                QMessageBox.warning(self, "Input Error", f"Converted key '{key_input}' = {key} is too large for the plain text length.")
                return
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Number of rails must be a valid integer or a single letter.")
            return

        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("RESPONSE JSON:", data)
                if "encrypted_text" in data:
                    self.ui.textBrowser_3.setPlainText(data["encrypted_text"])
                    QMessageBox.information(self, "Success", "Encrypted Successfully")
                else:
                    QMessageBox.critical(self, "API Error", "Invalid response from API: 'encrypted_text' not found.")
            else:
                QMessageBox.critical(self, "API Error", f"API returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to API: {e}")

    def call_api_decrypt(self):
        cipher_text = self.ui.textBrowser_3.toPlainText().strip()
        key_input = self.ui.textBrowser_2.toPlainText().strip()

        if not cipher_text or not key_input:
            QMessageBox.warning(self, "Input Error", "Please enter both cipher text and number of rails.")
            return

        try:
            if key_input.isdigit():
                key = int(key_input)
            elif key_input.isalpha() and len(key_input) == 1:
                key = ord(key_input.lower()) - ord('a') + 1
            else:
                raise ValueError

            print(f"Key after conversion from input '{key_input}':", key)

            if key < 2:
                QMessageBox.warning(self, "Input Error", f"Converted key '{key_input}' = {key} is too small. Minimum is 2.")
                return
            if key > len(cipher_text):
                QMessageBox.warning(self, "Input Error", f"Converted key '{key_input}' = {key} is too large for the cipher text length.")
                return
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Number of rails must be a valid integer or a single letter.")
            return

        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("RESPONSE JSON:", data)
                if "decrypted_text" in data:
                    self.ui.textBrowser.setPlainText(data["decrypted_text"])
                    QMessageBox.information(self, "Success", "Decrypted Successfully")
                else:
                    QMessageBox.critical(self, "API Error", "Invalid response from API: 'decrypted_text' not found.")
            else:
                QMessageBox.critical(self, "API Error", f"API returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to API: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
