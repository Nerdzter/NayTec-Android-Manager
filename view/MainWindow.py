from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from view.widgets.Sidebar import Sidebar
from view.widgets.Header import Header
from view.widgets.Dashboard import Dashboard
from view.widgets.Optimizer import Optimizer
from view.widgets.Antivirus import Antivirus


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NayTec Android Manager")
        self.setMinimumSize(1200, 720)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal horizontal: Sidebar + Conteúdo
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar (esquerda)
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        # Layout vertical para Header + Conteúdo central
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addLayout(content_layout)

        # Header
        self.header = Header(self)
        content_layout.addWidget(self.header)

        # Stack de páginas centrais
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        self.stack.addWidget(Dashboard()) 
        self.stack.addWidget(Optimizer())  
        self.stack.addWidget(Antivirus())

        # Conectar navegação
        self.sidebar.page_changed.connect(self.change_page)

    def change_page(self, index):
        self.stack.setCurrentIndex(index)
