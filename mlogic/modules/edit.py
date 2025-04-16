import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt

class EditDialog(QDialog):
    def __init__(self, row, row_id, parent):
        super().__init__(parent)
        self.row = row
        self.row_id = row_id  
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

        title = QLabel("Редактировать запись")
        title.setStyleSheet("color: #EEF0ED; font-size: 18px; font-weight: bold;")
        
        # Получаем текущие данные для редактирования
        conn = sqlite3.connect('dbs/dlspls.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT id, fio, deal FROM dlspls WHERE id = ?", 
                      (self.parent().table.item(self.row, 0).text(),))
        current_data = cursor.fetchone()
        conn.close()

        self.fio_input = QLineEdit(current_data[1] if current_data else "")
        self.fio_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #4D4B4B; color: #FFFFFF;")
        
        self.deal_input = QLineEdit(current_data[2] if current_data else "")
        self.deal_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #4D4B4B; color: #FFFFFF;")
        
        save_btn = QPushButton("Сохранить")
        save_btn.setStyleSheet(self.parent().button_style)
        save_btn.clicked.connect(self.save_changes)
        
        content_layout.addWidget(title)
        content_layout.addWidget(self.fio_input)
        content_layout.addWidget(self.deal_input)
        content_layout.addWidget(save_btn)
        
        widget.setLayout(content_layout)
        layout.addWidget(widget)
        self.setLayout(layout)

    def save_changes(self):
        fio = self.fio_input.text().strip()
        deal = self.deal_input.text().strip()
        
        if not fio or not deal:
            return
            
        conn = sqlite3.connect('dbs/dlspls.sql')
        cursor = conn.cursor()
        cursor.execute("UPDATE dlspls SET fio = ?, deal = ?, datetime = ? WHERE id = ?",
                    (fio, deal, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.row_id))
        conn.commit()
        conn.close()
        
        self.accept()