import sqlite3
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                           QTableWidgetItem, QPushButton, QDialog, QGraphicsOpacityEffect,
                           QMenu, QAction, QSizePolicy, QScrollArea, QHeaderView)
from PyQt5.QtGui import QColor, QPalette, QFont, QCursor
from PyQt5.QtCore import Qt

from mlogic.modules.add import AddDialog
from mlogic.modules.edit import EditDialog
from mlogic.modules.delete import DeleteDialog
from mlogic.modules.search import SearchDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Научные труды сотрудников")
        self.setMinimumSize(800, 600)
        self.setup_styles()
        self.init_ui()
        self.setup_database()
        self.load_data()

    def setup_styles(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2D2B2B"))
        palette.setColor(QPalette.WindowText, QColor("#EEF0ED"))
        palette.setColor(QPalette.Base, QColor("#3D3B3B"))
        palette.setColor(QPalette.Text, QColor("#FFFFFF"))
        self.setPalette(palette)

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

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Таблица: Научные труды сотрудников")
        title.setStyleSheet("color: #EEF0ED; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ФИО", "Научные труды", "Дата и время"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #3D3B3B;
                color: #FFFFFF;
                border: 1px solid #4D4B4B;
                gridline-color: #4D4B4B;
            }
            QHeaderView::section {
                background-color: #3D3B3B;
                color: #EEF0ED;
                padding: 5px;
                border: 1px solid #4D4B4B;
            }
        """)
        # style dlya table
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setMinimumSectionSize(100)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.table.cellClicked.connect(self.show_details)
        layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.add_btn.setStyleSheet(self.button_style)
        self.add_btn.clicked.connect(self.open_add_dialog)
        
        self.search_btn = QPushButton("Поиск")
        self.search_btn.setStyleSheet(self.button_style)
        self.search_btn.clicked.connect(self.open_search_dialog)
        
        self.delete_all_btn = QPushButton("Удалить все")
        self.delete_all_btn.setStyleSheet(self.button_style)
        self.delete_all_btn.clicked.connect(self.delete_all)

        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.search_btn)
        buttons_layout.addWidget(self.delete_all_btn)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        refresh_action = QAction("Обновить", self)
        refresh_action.triggered.connect(self.refresh_data)
        context_menu.addAction(refresh_action)
        context_menu.exec_(QCursor.pos())

    def refresh_data(self):
        self.load_data()

    def setup_database(self):
        if not os.path.exists('dbs'):
            os.makedirs('dbs')
        
        # проверка дб на существование (чтобы не было ошибки)
        db_path = 'dbs/dlspls.sql'
        if not os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dlspls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fio TEXT NOT NULL,
                    deal TEXT NOT NULL,
                    datetime TEXT NOT NULL
                )
            ''')
            conn.commit()
            conn.close()

    def load_data(self):
        conn = sqlite3.connect('dbs/dlspls.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT id, fio, deal, datetime FROM dlspls")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        
        # массив для сохранения айди для каждой строки
        self.row_ids = {}
        
        for row_idx, row_data in enumerate(rows):
            self.row_ids[row_idx] = row_data[0]
            for col_idx, data in enumerate(row_data[1:]):  
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.table.setItem(row_idx, col_idx, item)
        
        self.table.setWordWrap(True)
        
        self.table.resizeRowsToContents()
        
        self.table.setColumnWidth(1, 300)  
        self.table.setColumnWidth(0, 150) 
        self.table.setColumnWidth(2, 150) 
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed) 
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) 
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed) 
        
        conn.close()

    def show_details(self, row, column):
        if row < 0 or row >= len(self.row_ids):
            return
            
        fio = self.table.item(row, 0).text()
        deal = self.table.item(row, 1).text()
        datetime = self.table.item(row, 2).text()
        row_id = self.row_ids[row]  # получение айди для строки
        
        self.detail_dialog = DetailDialog(fio, deal, datetime, row, row_id, self)
        self.detail_dialog.show()
        
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.3)
        self.setGraphicsEffect(self.opacity_effect)

    def open_add_dialog(self):
        dialog = AddDialog(self)
        dialog.exec_()
        self.load_data()

    def open_search_dialog(self):
        dialog = SearchDialog(self)
        dialog.exec_()

    def delete_all(self):
        dialog = DeleteDialog(None, self, delete_all=True)
        dialog.exec_()
        self.load_data()

    def clear_opacity(self):
        self.setGraphicsEffect(None)
        
    def resizeEvent(self, event):
        # изменение окна изменение размера колонки
        super().resizeEvent(event)
        self.load_data() 

class DetailDialog(QDialog):
    def __init__(self, fio, deal, datetime, row, row_id, parent):
        super().__init__(parent)
        self.row = row
        self.row_id = row_id
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui(fio, deal, datetime)

    def init_ui(self, fio, deal, datetime):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #3D3B3B;
                border-radius: 8px;
                border: 1px solid #4D4B4B;
            }
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)

        fio_label = QLabel(f"ФИО: {fio}")
        fio_label.setStyleSheet("color: #EEF0ED; font-size: 14px;")
        fio_label.setWordWrap(True)

        deal_label = QLabel(f"Научные труды: {deal}")
        deal_label.setStyleSheet("color: #EEF0ED; font-size: 14px;")
        deal_label.setWordWrap(True)

        time_label = QLabel(f"Время добавления: {datetime}")
        time_label.setStyleSheet("color: #EEF0ED; font-size: 14px;")
        time_label.setWordWrap(True)

        content_layout.addWidget(fio_label)
        content_layout.addWidget(deal_label)
        content_layout.addWidget(time_label)

        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)

        buttons_layout = QHBoxLayout()
        edit_btn = QPushButton("Изменить")
        edit_btn.setStyleSheet(self.parent().button_style)
        edit_btn.clicked.connect(self.edit)

        delete_btn = QPushButton("Удалить")
        delete_btn.setStyleSheet(self.parent().button_style)
        delete_btn.clicked.connect(self.delete)

        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)

        content_layout_outer = QVBoxLayout()
        content_layout_outer.addWidget(scroll)
        content_layout_outer.addLayout(buttons_layout)

        widget.setLayout(content_layout_outer)
        layout.addWidget(widget)
        self.setLayout(layout)

        self.setMaximumHeight(400)

    def edit(self):
        dialog = EditDialog(self.row, self.row_id, self.parent())
        dialog.exec_()
        self.parent().load_data()
        self.parent().clear_opacity()
        self.close()

    def delete(self):
        dialog = DeleteDialog(self.row, self.parent(), row_id=self.row_id)
        dialog.exec_()
        self.parent().load_data()
        self.parent().clear_opacity()
        self.close()

    def mousePressEvent(self, event):
        if not self.childAt(event.pos()):
            self.parent().clear_opacity()
            self.close()
