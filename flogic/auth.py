import re
import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTabWidget, QMessageBox)
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt, QTimer

class AuthWindow(QWidget):
    def __init__(self, on_success_callback):
        super().__init__()
        
        self.on_success_callback = on_success_callback
        
        self.setWindowTitle("Научные труды сотрудников - Авторизация")
        self.setMinimumSize(500, 400)
        
        self.setup_styles()
        
        self.init_ui()
    
    def setup_styles(self):
        """Настройка стайлов окон"""
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2D2B2B"))
        palette.setColor(QPalette.WindowText, QColor("#EEF0ED"))
        palette.setColor(QPalette.Base, QColor("#3D3B3B"))
        palette.setColor(QPalette.Text, QColor("#FFFFFF"))
        self.setPalette(palette)
        
        # стайлы кнопок
        self.button_style = """
            QPushButton {
                background-color: #C9F1C9;
                color: #000000;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0CF20C;
            }
            QPushButton:pressed {
                background-color: #0AB20A;
            }
        """
        
        self.form_style = """
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                background-color: #3D3B3B;
                color: #FFFFFF;
                border: 1px solid #4D4B4B;
            }
            QLineEdit:focus {
                border: 1px solid #0CF20C;
            }
        """
        
        self.label_style = """
            QLabel {
                color: #EEF0ED;
                font-size: 12px;
            }
        """
        
        self.error_label_style = """
            QLabel {
                color: #F22B0C;
                font-size: 11px;
            }
        """
    
    def init_ui(self):
        """прогружаем интерфейс"""
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title_label = QLabel("Научные труды сотрудников")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #EEF0ED; font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #4D4B4B;
                border-radius: 4px;
                padding: 10px;
                background-color: #3D3B3B;
            }
            QTabBar::tab {
                background-color: #2D2B2B;
                color: #EEF0ED;
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #3D3B3B;
                border: 1px solid #4D4B4B;
                border-bottom: none;
            }
        """)
        
        self.login_tab = QWidget()
        self.init_login_tab()
        self.tabs.addTab(self.login_tab, "Авторизация")
        
        self.register_tab = QWidget()
        self.init_register_tab()
        self.tabs.addTab(self.register_tab, "Регистрация")
        
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
    
    def init_login_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        login_label = QLabel("Логин:")
        login_label.setStyleSheet(self.label_style)
        self.login_input = QLineEdit()
        self.login_input.setStyleSheet(self.form_style)
        self.login_input.setPlaceholderText("Введите логин")
        
        password_label = QLabel("Пароль:")
        password_label.setStyleSheet(self.label_style)
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(self.form_style)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Введите пароль")
        
        self.login_error_label = QLabel("")
        self.login_error_label.setStyleSheet(self.error_label_style)
        self.login_error_label.setWordWrap(True)
        
        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet(self.button_style)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.login)
        
        # виджеты
        layout.addWidget(login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_error_label)
        layout.addStretch(1)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        
        self.login_tab.setLayout(layout)
    
    def init_register_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        reg_login_label = QLabel("Логин:")
        reg_login_label.setStyleSheet(self.label_style)
        self.reg_login_input = QLineEdit()
        self.reg_login_input.setStyleSheet(self.form_style)
        self.reg_login_input.setPlaceholderText("Введите логин")
        
        reg_password_label = QLabel("Пароль:")
        reg_password_label.setStyleSheet(self.label_style)
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setStyleSheet(self.form_style)
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        self.reg_password_input.setPlaceholderText("Введите пароль")
        
        reg_confirm_label = QLabel("Подтверждение пароля:")
        reg_confirm_label.setStyleSheet(self.label_style)
        self.reg_confirm_input = QLineEdit()
        self.reg_confirm_input.setStyleSheet(self.form_style)
        self.reg_confirm_input.setEchoMode(QLineEdit.Password)
        self.reg_confirm_input.setPlaceholderText("Повторите пароль")
        
        # подсказки к паролю
        password_hint = QLabel("Пароль должен содержать от 6 до 20 символов, включать A-Z, a-z, 0-9, $@!%*?&")
        password_hint.setStyleSheet("color: #AAAAAA; font-size: 10px;")
        password_hint.setWordWrap(True)
        
        self.register_error_label = QLabel("")
        self.register_error_label.setStyleSheet(self.error_label_style)
        self.register_error_label.setWordWrap(True)
        
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setStyleSheet(self.button_style)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.register)
        
        # виджеты
        layout.addWidget(reg_login_label)
        layout.addWidget(self.reg_login_input)
        layout.addWidget(reg_password_label)
        layout.addWidget(self.reg_password_input)
        layout.addWidget(reg_confirm_label)
        layout.addWidget(self.reg_confirm_input)
        layout.addWidget(password_hint)
        layout.addWidget(self.register_error_label)
        layout.addStretch(1)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)
        
        self.register_tab.setLayout(layout)
    
    def validate_password(self, password):
        """делаем исключения для пароля"""
        if len(password) < 6 or len(password) > 20:
            return False, "Пароль должен содержать от 6 до 20 символов"
        
        if re.search(r'[а-яА-ЯёЁ]', password):
            return False, "Пароль не должен содержать кириллицу"
        
        if not re.search(r'[A-Z]', password):
            return False, "Пароль должен содержать хотя бы одну заглавную букву A-Z"
        
        if not re.search(r'[a-z]', password):
            return False, "Пароль должен содержать хотя бы одну строчную букву a-z"
        
        if not re.search(r'[0-9]', password):
            return False, "Пароль должен содержать хотя бы одну цифру 0-9"
        
        if not re.search(r'[$@!%*?&]', password):
            return False, "Пароль должен содержать хотя бы один специальный символ $@!%*?&"
        
        return True, ""
    
    def login(self):
        username = self.login_input.text().strip()
        password = self.password_input.text()
        
        # проверяем на пустые поля в форме
        if not username or not password:
            self.login_error_label.setText("Все поля должны быть заполнены")
            return
        
        try:
            conn = sqlite3.connect('dbs/users.sql')
            cursor = conn.cursor()
            
            # проверяем юзера в дб
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            # пользователя нет в дб
            if not result:
                self.login_error_label.setText("Пользователь не найден")
                conn.close()
                return
            
            if result[0] != password:
                self.login_error_label.setText("Неверный пароль")
                conn.close()
                return
            
            self.login_button.setText("С возвращением")
            self.login_button.setEnabled(False)
            self.login_error_label.setText("")
            
            conn.close()
            
            # таймер для прелоадера
            QTimer.singleShot(1500, self.on_success_callback)
            
        except sqlite3.Error as e:
            self.login_error_label.setText(f"ошибка дб: {str(e)}")
    
    def register(self):
        username = self.reg_login_input.text().strip()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_input.text()
        
        """проверки пароля"""
        if not username or not password or not confirm_password:
            self.register_error_label.setText("Все поля должны быть заполнены")
            return
        
        if password != confirm_password:
            self.register_error_label.setText("Пароли не совпадают")
            return
        
        is_valid, error_message = self.validate_password(password)
        if not is_valid:
            self.register_error_label.setText(error_message)
            return
        
        # попытка регстрации
        try:
            conn = sqlite3.connect('dbs/users.sql')
            cursor = conn.cursor()
            
            # проверяем пользователя в дб
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                self.register_error_label.setText("Пользователь с таким логином уже существует")
                conn.close()
                return
            
            # добавляем пользователя после рег
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            
            conn.close()
            
            self.register_button.setText("Вы успешно зарегистрировались")
            self.register_button.setEnabled(False)
            self.register_error_label.setText("")
            
            # таймер для прелоадера
            QTimer.singleShot(1500, self.on_success_callback)
            
        except sqlite3.Error as e:
            self.register_error_label.setText(f"ошибка дб: {str(e)}")
