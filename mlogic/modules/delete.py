import sqlite3
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

class DeleteDialog(QDialog):
    def __init__(self, row, parent, delete_all=False, row_id=None):
        super().__init__(parent)
        self.row = row
        self.row_id = row_id
        self.delete_all = delete_all
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

        title = QLabel("Вы уверены, что хотите удалить запись?" if not self.delete_all else "Удалить все записи?")
        title.setStyleSheet("color: #EEF0ED; font-size: 16px;")
        
        buttons_layout = QHBoxLayout()
        yes_btn = QPushButton("Да")
        yes_btn.setStyleSheet(self.parent().button_style)
        yes_btn.clicked.connect(self.delete)
        
        no_btn = QPushButton("Нет")
        no_btn.setStyleSheet(self.parent().button_style)
        no_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(yes_btn)
        buttons_layout.addWidget(no_btn)
        
        content_layout.addWidget(title)
        content_layout.addLayout(buttons_layout)
        
        widget.setLayout(content_layout)
        layout.addWidget(widget)
        self.setLayout(layout)

    def delete(self):
        conn = sqlite3.connect('dbs/dlspls.sql')
        cursor = conn.cursor()
        
        if self.delete_all:
            cursor.execute("DELETE FROM dlspls")
        else:
            cursor.execute("DELETE FROM dlspls WHERE id = ?",
                        (self.row_id,))
        
        conn.commit()
        conn.close()
        self.accept()