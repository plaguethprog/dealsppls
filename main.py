import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont

os.makedirs('dbs', exist_ok=True)
os.makedirs('flogic', exist_ok=True)
os.makedirs('mlogic', exist_ok=True)
os.makedirs('mlogic/modules', exist_ok=True)

from flogic.auth import AuthWindow
from flogic.preloader import Preloader
from mlogic.dealsppls import MainWindow

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        self.setup_fonts()
        
        self.init_databases()
        
        self.auth_window = AuthWindow(self.start_preloader)
        self.auth_window.show()
        
        sys.exit(self.app.exec_())
    
    def setup_fonts(self):
        """шрифты, если есть в фонтсах мой то его если нет то системный"""
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont(":/fonts/Roboto-Regular.ttf")
        if font_id != -1:
            font_family = font_db.applicationFontFamilies(font_id)[0]
            default_font = QFont(font_family, 10)
            self.app.setFont(default_font)
        else:
            default_font = QFont("Arial", 10)
            self.app.setFont(default_font)
    
    def init_databases(self):
        conn_users = sqlite3.connect('dbs/users.sql')
        cursor_users = conn_users.cursor()
        
        cursor_users.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        
        conn_users.commit()
        conn_users.close()
        
        if os.path.exists('dbs/dlspls.sql'):
            conn_dlspls = sqlite3.connect('dbs/dlspls.sql')
            cursor_dlspls = conn_dlspls.cursor()

            cursor_dlspls.execute('''
            CREATE TABLE IF NOT EXISTS dlspls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fio TEXT NOT NULL,
                deal TEXT NOT NULL,
                datetime TEXT NOT NULL
            )
            ''')
            
            conn_dlspls.commit()
            conn_dlspls.close()
    
    def start_preloader(self):
        self.auth_window.hide()
        self.preloader = Preloader(self.start_main_window)
        self.preloader.show()
    
    def start_main_window(self):
        self.preloader.hide()
        self.main_window = MainWindow()
        self.main_window.show()

if __name__ == "__main__":
    app = App()
