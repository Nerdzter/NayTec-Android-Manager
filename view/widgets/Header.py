from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class Header(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Header")
        self.setFixedHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)

        # Título
        self.title_label = QLabel("Dashboard")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: 500;")
        layout.addWidget(self.title_label)

        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Botões de controle da janela
        self.minimize_btn = QPushButton("-")
        self.maximize_btn = QPushButton("⬜")
        self.close_btn = QPushButton("×")

        for btn in [self.minimize_btn, self.maximize_btn, self.close_btn]:
            btn.setObjectName("HeaderButton")
            btn.setFixedSize(30, 30)
            layout.addWidget(btn)

        # Conectar botões à janela principal
        self.minimize_btn.clicked.connect(self.parent().showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_max_restore)
        self.close_btn.clicked.connect(self.parent().close)

    def toggle_max_restore(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()
