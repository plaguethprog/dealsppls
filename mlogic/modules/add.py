import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt

class AddDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #3D3B3B;
                border-radius: 8px;
                border: 1px solid #4D4B4B;
            }
        """)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Добавить нового сотрудника")
        title.setStyleSheet("color: #EEF0ED; font-size: 18px; font-weight: bold;")
        
        self.fio_input = QLineEdit()
        self.fio_input.setPlaceholderText("ФИО")
        self.fio_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #4D4B4B; color: #FFFFFF;")
        
        self.deal_input = QLineEdit()
        self.deal_input.setPlaceholderText("Научные труды сотрудника")
        self.deal_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #4D4B4B; color: #FFFFFF;")
        
        add_btn = QPushButton("Добавить")
        add_btn.setStyleSheet(self.parent().button_style)
        add_btn.clicked.connect(self.add_record)
        
        content_layout.addWidget(title)
        content_layout.addWidget(self.fio_input)
        content_layout.addWidget(self.deal_input)
        content_layout.addWidget(add_btn)
        
        widget.setLayout(content_layout)
        layout.addWidget(widget)
        self.setLayout(layout)

    def add_record(self):
        fio = self.fio_input.text().strip()
        deal = self.deal_input.text().strip()
        
        if not fio or not deal:
            return
            
        conn = sqlite3.connect('dbs/dlspls.sql')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dlspls (fio, deal, datetime) VALUES (?, ?, ?)",
                      (fio, deal, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        
        self.accept()