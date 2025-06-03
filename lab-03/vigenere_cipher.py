import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.vigenere import Ui_Vigenere

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(__file__), 'platforms')

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Vigenere()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)

    def validate_key(self, key):
        if not key.isalpha():
            QMessageBox.warning(self, "Invalid Key", "Key must contain only letters (A-Z or a-z).")
            return False
        return True

    def call_api_encrypt(self):
        plain_text = self.ui.textBrowser.toPlainText().strip()
        key = self.ui.textBrowser_2.toPlainText().strip()

        if not plain_text or not key:
            QMessageBox.warning(self, "Input Error", "Please enter both plain text and key.")
            return

        if not self.validate_key(key):
            return

        url = "http://127.0.0.1:5000/api/vigenere/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textBrowser_3.setPlainText(data["encrypted_text"])
                QMessageBox.information(self, "Success", "Encrypted Successfully")
            else:
                QMessageBox.critical(self, "API Error", f"API returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to API: {e}")

    def call_api_decrypt(self):
        cipher_text = self.ui.textBrowser_3.toPlainText().strip()
        key = self.ui.textBrowser_2.toPlainText().strip()

        if not cipher_text or not key:
            QMessageBox.warning(self, "Input Error", "Please enter both cipher text and key.")
            return

        if not self.validate_key(key):
            return

        url = "http://127.0.0.1:5000/api/vigenere/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textBrowser.setPlainText(data["decrypted_text"])
                QMessageBox.information(self, "Success", "Decrypted Successfully")
            else:
                QMessageBox.critical(self, "API Error", f"API returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to API: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
