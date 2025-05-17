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

        # Informações do dispositivo
        self.device_label = QLabel("🔌 Verificando dispositivo...")
        self.device_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        main_layout.addWidget(self.device_label, alignment=Qt.AlignCenter)

        # Grade geral com cartões e tela
        grid = QGridLayout()
        grid.setSpacing(20)

        # Cartões
        self.cards = {}
        sections = ["CPU", "RAM", "Armazenamento", "Bateria"]
        positions = [(0, 0), (0, 2), (1, 0), (1, 2)]
        for title, pos in zip(sections, positions):
            card = self.create_card(title)
            grid.addWidget(card, *pos)
            self.cards[title] = card.findChild(QLabel, "value")

        # === Tela central do celular ===
        screen_container = QVBoxLayout()

        self.screen_label = QLabel()
        self.screen_label.setFixedSize(200, 400)
        self.screen_label.setStyleSheet("""
            border-radius: 12px;
            background-color: #000;
            padding: 2px;
        """)
        screen_container.addWidget(self.screen_label, alignment=Qt.AlignCenter)

        # Informativo
        screen_info = QLabel("🕒 A imagem é atualizada automaticamente a cada 30 segundos.")
        screen_info.setStyleSheet("color: #B0B0B0; font-size: 12px;")
        screen_container.addWidget(screen_info, alignment=Qt.AlignCenter)

        grid.addLayout(screen_container, 0, 1, 2, 1, alignment=Qt.AlignCenter)

        main_layout.addLayout(grid)

        # Botão de captura manual
        btn_layout = QHBoxLayout()
        self.capture_btn = QPushButton("📸 Capturar Agora")
        self.capture_btn.setFixedWidth(180)
        self.capture_btn.clicked.connect(self.update_screen)
        btn_layout.addWidget(self.capture_btn, alignment=Qt.AlignCenter)
        main_layout.addLayout(btn_layout)

        # Timer de dados
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(4000)

        # Timer da tela
        self.screen_timer = QTimer()
        self.screen_timer.timeout.connect(self.update_screen)
        self.screen_timer.start(30000)

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
            self.device_label.setText("🚫 Nenhum dispositivo conectado")
            for lbl in self.cards.values():
                lbl.setText("Desconectado")
            self.screen_label.clear()
            return

        info = DeviceModel.get_device_info()
        self.device_label.setText(f"📱 {info['model']} | Android {info['android']} | Codinome: {info['device']}")
        self.cards["CPU"].setText(DeviceModel.get_cpu_human())
        self.cards["RAM"].setText(DeviceModel.get_ram_human())
        self.cards["Armazenamento"].setText(DeviceModel.get_storage_human())
        self.cards["Bateria"].setText(DeviceModel.get_battery_human())

    def update_screen(self):
        path = DeviceModel.capture_screen()
        if path:
            pixmap = QPixmap(path).scaled(
                self.screen_label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            self.screen_label.setPixmap(pixmap)
