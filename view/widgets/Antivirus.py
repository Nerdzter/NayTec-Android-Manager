from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar,
    QMessageBox, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QEasingCurve, QPropertyAnimation
from controller import security_controller
import subprocess

class Antivirus(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Antivirus")
        self.setStyleSheet("background-color: #1C1C1E; color: white;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Análise de Ameaças")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: white;")
        layout.addWidget(title)

        desc = QLabel("Identificamos comportamentos suspeitos, permissões críticas e apps maliciosos.")
        desc.setStyleSheet("font-size: 14px; color: #B0B0B0;")
        layout.addWidget(desc)

        scan_frame = QFrame()
        scan_frame.setStyleSheet("""
            QFrame {
                background-color: #2A2A2E;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        scan_layout = QVBoxLayout(scan_frame)
        scan_layout.setSpacing(15)

        self.scan_button = QPushButton("Iniciar Análise")
        self.scan_button.setStyleSheet("""
            QPushButton {
                background-color: #007aff;
                color: white;
                padding: 10px 24px;
                border: none;
                border-radius: 12px;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #339CFF;
            }
        """)
        self.scan_button.clicked.connect(self.start_scan)
        scan_layout.addWidget(self.scan_button)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #2A2A2E;
                border-radius: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #007aff;
                border-radius: 8px;
            }
        """)
        scan_layout.addWidget(self.progress)

        self.results_label = QLabel("")
        self.results_label.setStyleSheet("font-size: 14px; color: #B0B0B0;")
        scan_layout.addWidget(self.results_label)

        layout.addWidget(scan_frame)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: transparent; border: none;")
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setSpacing(12)
        self.scroll.setWidget(self.results_container)
        layout.addWidget(self.scroll)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def start_scan(self):
        self.results_label.setText("Verificando... Por favor, aguarde.")
        self.progress.setVisible(True)
        self.scan_button.setEnabled(False)
        QTimer.singleShot(1500, self.run_analysis)

    def run_analysis(self):
        try:
            print("[DEBUG] Iniciando análise...")
            threats = security_controller.summarize_threats()
            print(f"[DEBUG] {len(threats)} ameaças detectadas")
        except Exception as e:
            print(f"[ERRO] {e}")
            self.results_label.setText(f"Erro: {e}")
            self.progress.setVisible(False)
            self.scan_button.setEnabled(True)
            return

        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if not threats:
            self.results_label.setText("Nenhuma ameaça foi detectada.")
        else:
            self.results_label.setText(f"{len(threats)} ameaça(s) detectada(s):")
            for pkg, label in threats:
                card = self.create_threat_card(pkg, label)
                self.results_layout.addWidget(card)
                self.animate_card(card)

        self.progress.setVisible(False)
        self.scan_button.setEnabled(True)

    def create_threat_card(self, pkg, name):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #29292D;
                border-radius: 12px;
                padding: 14px;
            }
        """)
        layout = QHBoxLayout(card)
        layout.setSpacing(15)

        label = QLabel(f"{name}\n<small style='color:#888'>{pkg}</small>")
        label.setStyleSheet("font-size: 14px;")
        layout.addWidget(label, 1)

        remove_btn = QPushButton("Desinstalar")
        remove_btn.setStyleSheet("background-color: #FF3B30; color: white; padding: 6px 14px; border-radius: 10px;")
        remove_btn.clicked.connect(lambda: self.uninstall_app(pkg, name))
        layout.addWidget(remove_btn)

        disable_btn = QPushButton("Quarentena")
        disable_btn.setStyleSheet("background-color: #FFA500; color: white; padding: 6px 14px; border-radius: 10px;")
        disable_btn.clicked.connect(lambda: self.quarantine_app(pkg, name))
        layout.addWidget(disable_btn)

        # Sombras
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 5)
        shadow.setColor(Qt.black)
        card.setGraphicsEffect(shadow)

        return card

    def animate_card(self, widget):
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(400)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        widget.anim = anim  # Prevent garbage collection

    def uninstall_app(self, pkg, name):
        confirm = QMessageBox.question(self, "Confirmar", f"Deseja remover o app '{name}'?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            subprocess.call(["adb", "shell", "pm", "uninstall", pkg])
            self.start_scan()

    def quarantine_app(self, pkg, name):
        confirm = QMessageBox.question(self, "Confirmar", f"Deseja desativar o app '{name}'?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            subprocess.call(["adb", "shell", "pm", "disable-user", pkg])
            self.start_scan()
