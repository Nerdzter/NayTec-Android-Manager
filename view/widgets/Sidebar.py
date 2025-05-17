from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt

class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(80)
        self.setObjectName("Sidebar")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 20, 0, 0)
        self.layout.setSpacing(15)

        self.buttons = []
        self.active_index = 0

        self.sections = [
            ("📊", "Dashboard"),
            ("🧹", "Otimização"),
            ("🛡️", "Antivírus"),
            ("📈", "Desempenho"),
            ("⚙️", "Configurações")
        ]

        for index, (icon, name) in enumerate(self.sections):
            btn = QPushButton(icon)
            btn.setToolTip(name)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.setObjectName("SidebarButton")
            btn.clicked.connect(lambda checked, i=index: self.change_page(i))
            self.layout.addWidget(btn)
            self.buttons.append(btn)

        self.buttons[0].setChecked(True)

    def change_page(self, index):
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)
        self.active_index = index
        self.page_changed.emit(index)
