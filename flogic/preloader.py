import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtGui import QColor, QPalette, QLinearGradient, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty

# стили таскбара
class CustomProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.setTextVisible(False)
        self.setFixedHeight(20)
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 10px;
                background-color: #3D3B3B;
            }
            
            QProgressBar::chunk {
                border-radius: 10px;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #525350, stop:0.5 #EBF209, stop:1 #7EF209);
            }
        """)

class Preloader(QWidget):
    def __init__(self, on_complete_callback):
        super().__init__()
        
        self.on_complete_callback = on_complete_callback
        
        self.setWindowTitle("Научные труды сотрудников - Загрузка")
        self.setMinimumSize(500, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.setup_styles()
        
        self.init_ui()
        
        self.start_loading()
    
    def setup_styles(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2D2B2B"))
        palette.setColor(QPalette.WindowText, QColor("#EEF0ED"))
        self.setPalette(palette)
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        self.title_label = QLabel("Загрузка данных...")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #EEF0ED; font-size: 24px; font-weight: bold;")
        
        self.message_label = QLabel("Пожалуйста, подождите...")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: #BBBBBB; font-size: 14px;")
        
        self.progress_bar = CustomProgressBar()
        
        layout.addStretch(2)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.progress_bar)
        layout.addStretch(2)
        
        self.setLayout(layout)
    
    def start_loading(self):
        """анимации)))))))"""
        self.animation = QPropertyAnimation(self, b"progress_value")
        self.animation.setDuration(15000)  # 15 секунд
        self.animation.setStartValue(0)
        self.animation.setEndValue(100)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self.animation.finished.connect(self.on_loading_complete)
    
        self.animation.start()
        
        # разные сообщения для таскбара
        self.loading_messages = [
            "Загрузка данных...",
            "Подготовка базы данных...",
            "Инициализация компонентов...",
            "Настройка интерфейса...",
            "Почти готово..."
        ]
        
        # таймеры для смены сообщений
        self.message_timer = QTimer(self)
        self.message_timer.timeout.connect(self.update_message)
        self.message_timer.start(3000)  # каждые 3 секунды 
        
        self.current_message_index = 0
    
    def update_message(self):
        if self.current_message_index < len(self.loading_messages):
            self.message_label.setText(self.loading_messages[self.current_message_index])
            self.current_message_index += 1
    
    def on_loading_complete(self):
        self.message_timer.stop()
        
        self.title_label.setText("Загрузка завершена")
        self.message_label.setText("Запуск приложения...")
        
        QTimer.singleShot(1000, self.on_complete_callback)
    
    def _get_progress_value(self):
        return self.progress_bar.value()
    
    def _set_progress_value(self, value):
        self.progress_bar.setValue(value)
    
    progress_value = pyqtProperty(int, _get_progress_value, _set_progress_value)
