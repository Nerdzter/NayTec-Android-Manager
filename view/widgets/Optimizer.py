from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QSlider
)
from PyQt5.QtCore import Qt
import subprocess


class Optimizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Optimizer")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("🧼 Otimização do Sistema")
        title.setStyleSheet("font-size: 24px; font-weight: 600;")
        layout.addWidget(title)

        # Limpar Cache
        self.btn_cache = self.create_button("🧹 Limpar Cache", "#00BFFF")
        self.btn_cache.clicked.connect(self.clean_cache)
        layout.addWidget(self.btn_cache)

        # Fechar Apps
        self.btn_close_apps = self.create_button("🛑 Fechar Apps em Segundo Plano", "#00FF7F")
        self.btn_close_apps.clicked.connect(self.close_background_apps)
        layout.addWidget(self.btn_close_apps)

        # Limitar Processos
        label_slider = QLabel("🔧 Limitar Processos em Segundo Plano")
        label_slider.setStyleSheet("font-size: 16px; font-weight: 500;")
        layout.addWidget(label_slider)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(4)
        self.slider.setValue(2)
        self.slider.setStyleSheet("color: #8A2BE2;")
        layout.addWidget(self.slider)

        self.btn_set_process_limit = self.create_button("Aplicar Limite de Processos", "#8A2BE2")
        self.btn_set_process_limit.clicked.connect(self.limit_background_processes)
        layout.addWidget(self.btn_set_process_limit)

        # Análise de segurança
        self.btn_security = self.create_button("🛡️ Analisar Segurança", "#FF4500")
        self.btn_security.clicked.connect(self.analyze_security)
        layout.addWidget(self.btn_security)

        # Reiniciar Dispositivo
        self.btn_reboot = self.create_button("🔄 Reiniciar Dispositivo", "#FF6347")
        self.btn_reboot.clicked.connect(self.reboot_device)
        layout.addWidget(self.btn_reboot)

        # Mensagem de status
        self.status = QLabel("")
        self.status.setStyleSheet("font-size: 14px; color: #B0B0B0;")
        layout.addWidget(self.status)

    def create_button(self, text, color):
        btn = QPushButton(text)
        btn.setFixedSize(260, 50)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #121212;
                border: none;
                font-size: 15px;
                font-weight: bold;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                opacity: 0.85;
            }}
        """)
        return btn

    def run_adb(self, cmd):
        try:
            output = subprocess.check_output(["adb", "shell"] + cmd.split(), encoding='utf-8')
            return output.strip()
        except Exception as e:
            return f"Erro: {e}"

    def clean_cache(self):
        self.status.setText("🧹 Limpando cache...")
        result = self.run_adb("pm trim-caches 9999999999")
        self.status.setText("✅ Cache limpo com sucesso!" if "Erro" not in result else result)

    def close_background_apps(self):
        self.status.setText("🛑 Fechando aplicativos em segundo plano...")
        result = self.run_adb("am kill-all")
        self.status.setText("✅ Aplicativos fechados." if "Erro" not in result else result)

    def limit_background_processes(self):
        limit = str(self.slider.value())
        self.status.setText(f"🔧 Limitando processos para {limit}...")
        result = self.run_adb(f"settings put global max_background_processes {limit}")
        self.status.setText("✅ Limite aplicado com sucesso." if "Erro" not in result else result)

    def analyze_security(self):
        self.status.setText("🛡️ Analisando aplicativos desativados...")
        result = self.run_adb("pm list packages -d")
        if result:
            QMessageBox.information(self, "Apps Desativados", result)
        else:
            QMessageBox.information(self, "Seguro", "Nenhum app desativado detectado.")
        self.status.setText("✅ Análise concluída.")

    def reboot_device(self):
        reply = QMessageBox.question(
            self,
            "Confirmar Reinício",
            "Tem certeza que deseja reiniciar o dispositivo?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.status.setText("🔄 Reiniciando...")
            self.run_adb("reboot")
