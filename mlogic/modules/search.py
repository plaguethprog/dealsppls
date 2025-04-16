import sqlite3
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QDateEdit, QTableWidgetItem
from PyQt5.QtCore import Qt, QDate

class SearchDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.parent_window = parent
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

        title = QLabel("Поиск")
        title.setStyleSheet("color: #EEF0ED; font-size: 18px; font-weight: bold;")
        
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Поиск по ключевому слову")
        self.keyword_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #4D4B4B; color: #FFFFFF;")
        
        self.fio_input = QLineEdit()
        self.fio_input.setPlaceholderText("Поиск по ФИО")
        self.fio_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #4D4B4B; color: #FFFFFF;")
        
        date_label = QLabel("Поиск по дате:")
        date_label.setStyleSheet("color: #EEF0ED;")
        
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumDate(QDate(1999, 1, 1))
        self.date_input.setMaximumDate(QDate(2025, 4, 20))
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #4D4B4B; color: #FFFFFF;")
        
        search_btn = QPushButton("Поиск")
        search_btn.setStyleSheet(self.parent_window.button_style)
        search_btn.clicked.connect(self.search)
        
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet(self.parent_window.button_style)
        close_btn.clicked.connect(self.close)
        
        content_layout.addWidget(title)
        content_layout.addWidget(self.keyword_input)
        content_layout.addWidget(self.fio_input)
        content_layout.addWidget(date_label)
        content_layout.addWidget(self.date_input)
        content_layout.addWidget(search_btn)
        content_layout.addWidget(close_btn)
        
        widget.setLayout(content_layout)
        layout.addWidget(widget)
        self.setLayout(layout)

    def search(self):
        keyword = self.keyword_input.text().strip()
        fio = self.fio_input.text().strip()
        date = self.date_input.date().toString("yyyy-MM-dd")
        
        conn = sqlite3.connect('dbs/dlspls.sql')
        cursor = conn.cursor()
        
        # Базовый запрос
        query = "SELECT id, fio, deal, datetime FROM dlspls WHERE 1=1"
        params = []
        
        # Добавляем условия поиска
        if keyword:
            query += " AND (fio LIKE ? OR deal LIKE ?)"
            params.extend(['%' + keyword + '%', '%' + keyword + '%'])
        
        if fio:
            query += " AND fio LIKE ?"
            params.append('%' + fio + '%')
        
        if date:
            query += " AND datetime LIKE ?"
            params.append('%' + date + '%')
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Очищаем таблицу и заполняем результатами поиска
        parent_table = self.parent_window.table
        parent_table.setRowCount(len(rows))
        
        # Обновляем ID для каждой строки
        self.parent_window.row_ids = {}
        
        for row_idx, row_data in enumerate(rows):
            self.parent_window.row_ids[row_idx] = row_data[0]  # Сохраняем ID
            for col_idx, data in enumerate(row_data[1:]):  # Skip ID
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                parent_table.setItem(row_idx, col_idx, item)
        
        parent_table.resizeColumnsToContents()
        conn.close()
        self.close()
