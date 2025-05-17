from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QGridLayout
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from model.device_model import DeviceModel


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Dashboard")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Dispositivo
        self.device_label = QLabel("🔌 Verificando dispositivo...")
        self.device_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        main_layout.addWidget(self.device_label, alignment=Qt.AlignCenter)

        # GRID layout para organizar tudo ao redor da tela central
        grid = QGridLayout()
        grid.setSpacing(20)

        # Cartões de status
        self.cards = {}
        sections = ["CPU", "RAM", "Armazenamento", "Bateria"]

        positions = [(0, 0), (0, 2), (1, 0), (1, 2)]
        for title, pos in zip(sections, positions):
            card = self.create_card(title)
            grid.addWidget(card, *pos)
            self.cards[title] = card.findChild(QLabel, "value")

        # Miniatura central da tela do celular
        self.screen_label = QLabel()
        self.screen_label.setFixedSize(200, 400)
        self.screen_label.setStyleSheet("border: 3px solid #8A2BE2; border-radius: 12px;")
        grid.addWidget(self.screen_label, 0, 1, 2, 1, alignment=Qt.AlignCenter)

        main_layout.addLayout(grid)

        # Botão de captura
        self.capture_btn = QPushButton("📸 Capturar Tela")
        self.capture_btn.setFixedWidth(180)
        self.capture_btn.clicked.connect(self.update_screen)
        main_layout.addWidget(self.capture_btn, alignment=Qt.AlignCenter)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(4000)

        self.update_data()

    def create_card(self, title):
        box = QGroupBox()
        box.setStyleSheet("""
            QGroupBox {
                background-color: #1E1E1E;
                border: none;
                border-bottom: 3px solid #00BFFF;
                border-radius: 10px;
            }
        """)
        box.setFixedSize(220, 120)
        vbox = QVBoxLayout(box)
        vbox.setContentsMargins(12, 8, 12, 8)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        vbox.addWidget(title_label)

        value_label = QLabel("...")
        value_label.setObjectName("value")
        value_label.setStyleSheet("font-size: 13px; color: #B0B0B0;")
        value_label.setWordWrap(True)
        vbox.addWidget(value_label)

        return box

    def update_data(self):
        if not DeviceModel.is_connected():
            self.device_label.setText("🚫 Nenhum dispositivo encontrado via ADB")
            for lbl in self.cards.values():
                lbl.setText("Desconectado")
            self.screen_label.clear()
            return

        # Dispositivo
        info = DeviceModel.get_device_info()
        self.device_label.setText(f"📱 {info['model']} | Android {info['android']} | Codinome: {info['device']}")

        # Cartões com dados interpretáveis
        self.cards["CPU"].setText(DeviceModel.get_cpu_human())
        self.cards["RAM"].setText(DeviceModel.get_ram_human())
        self.cards["Armazenamento"].setText(DeviceModel.get_storage_human())
        self.cards["Bateria"].setText(DeviceModel.get_battery_human())

        self.update_screen()

    def update_screen(self):
        path = DeviceModel.capture_screen()
        if path:
            pixmap = QPixmap(path).scaled(
                self.screen_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.screen_label.setPixmap(pixmap)
