from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider,
    QMessageBox, QScrollArea, QFrame, QCheckBox
)
from PyQt5.QtCore import Qt
import subprocess
import re


class Optimizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Optimizer")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Lado esquerdo - botões de otimização
        left_panel = QVBoxLayout()
        left_panel.setSpacing(15)

        title = QLabel("\ud83e\ude9c Otimização do Sistema")
        title.setStyleSheet("font-size: 24px; font-weight: 600; color: #FFFFFF;")
        left_panel.addWidget(title)

        self.btn_cache = self.create_button("\ud83e\ude9c Limpar Cache", "#00BFFF", self.clean_cache)
        self.btn_close_apps = self.create_button("\u274c Fechar Apps em Segundo Plano", "#00FF7F", self.close_background_apps)
        self.btn_set_process_limit = self.create_button("Aplicar Limite de Processos", "#8A2BE2", self.limit_background_processes)
        self.btn_security = self.create_button("\ud83d\udee1\ufe0f Analisar Segurança", "#FF4500", self.analyze_security)
        self.btn_reboot = self.create_button("\ud83d\udd04 Reiniciar Dispositivo", "#FF6347", self.reboot_device)

        # Slider de limite de processos
        left_panel.addWidget(QLabel("\u2692\ufe0f Limitar Processos em Segundo Plano", self, styleSheet="font-size: 16px; color: #FFFFFF;"))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(4)
        self.slider.setValue(2)
        self.slider.setStyleSheet("color: #8A2BE2;")
        left_panel.addWidget(self.slider)

        # Adiciona os botões
        for btn in [self.btn_cache, self.btn_close_apps, self.btn_set_process_limit, self.btn_security, self.btn_reboot]:
            left_panel.addWidget(btn)

        layout.addLayout(left_panel, 1)

        # Lado direito - lista de apps
        right_panel = QVBoxLayout()

        app_title = QLabel("\ud83d\udcf1 Aplicativos Instalados")
        app_title.setStyleSheet("font-size: 18px; font-weight: 500; color: #FFFFFF;")
        right_panel.addWidget(app_title)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #1E1E1E; border: none;")
        self.apps_container = QWidget()
        self.apps_layout = QVBoxLayout(self.apps_container)
        self.scroll.setWidget(self.apps_container)
        right_panel.addWidget(self.scroll, 1)

        uninstall_all_btn = QPushButton("\ud83d\uddd1\ufe0f Desinstalar Selecionados")
        uninstall_all_btn.setStyleSheet("background-color: #DC143C; color: white; font-weight: bold; border-radius: 8px; padding: 8px;")
        uninstall_all_btn.clicked.connect(self.uninstall_selected_apps)
        right_panel.addWidget(uninstall_all_btn)

        layout.addLayout(right_panel, 2)

        self.status = QLabel("")
        self.status.setStyleSheet("font-size: 14px; color: #B0B0B0;")
        layout.addWidget(self.status)

        self.apps_checkboxes = []
        self.load_apps()

    def create_button(self, text, color, action):
        btn = QPushButton(text)
        btn.setFixedSize(260, 50)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #121212;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                opacity: 0.85;
            }}
        """)
        btn.clicked.connect(action)
        return btn

    def run_adb(self, cmd):
        try:
            output = subprocess.check_output(["adb", "shell"] + cmd.split(), encoding="utf-8")
            return output.strip()
        except Exception as e:
            return f"Erro: {e}"

    def clean_cache(self):
        self.status.setText("\ud83e\ude9c Limpando cache...")
        result = self.run_adb("pm trim-caches 9999999999")
        self.status.setText("\u2705 Cache limpo!" if "Erro" not in result else result)

    def close_background_apps(self):
        self.status.setText("\u274c Fechando apps...")
        result = self.run_adb("am kill-all")
        self.status.setText("\u2705 Apps fechados." if "Erro" not in result else result)

    def limit_background_processes(self):
        val = self.slider.value()
        result = self.run_adb(f"settings put global max_background_processes {val}")
        self.status.setText("\u2705 Limite aplicado." if "Erro" not in result else result)

    def analyze_security(self):
        self.status.setText("\ud83d\udee1\ufe0f Analisando apps...")
        result = self.run_adb("pm list packages -d")
        if result:
            QMessageBox.information(self, "Apps Desativados", result)
        else:
            QMessageBox.information(self, "Seguro", "Nenhum app desativado.")
        self.status.setText("\u2705 Análise concluída.")

    def reboot_device(self):
        reply = QMessageBox.question(self, "Confirmar", "Reiniciar dispositivo?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.status.setText("\ud83d\udd04 Reiniciando...")
            self.run_adb("reboot")

    def load_apps(self):
        self.status.setText("\ud83d\udce6 Carregando apps...")
        try:
            packages_output = subprocess.check_output(
                ["adb", "shell", "pm", "list", "packages", "-3"], encoding="utf-8"
            )
            packages = [line.replace("package:", "").strip() for line in packages_output.splitlines()]
            self.apps_checkboxes.clear()

            for pkg in packages:
                try:
                    label_output = subprocess.check_output(
                        ["adb", "shell", "dumpsys", "package", pkg], encoding="utf-8"
                    )
                    match = re.search(r"application-label:'([^']+)'", label_output)
                    label = match.group(1) if match else pkg
                except:
                    label = pkg

                cb = QCheckBox(label)
                cb.setObjectName(pkg)
                cb.setStyleSheet("color: #FFFFFF; font-size: 14px;")
                self.apps_checkboxes.append(cb)
                self.apps_layout.addWidget(cb)

            self.status.setText(f"\ud83d\udcc4 {len(packages)} apps carregados.")

        except Exception as e:
            self.status.setText(f"Erro: {e}")

    def uninstall_selected_apps(self):
        selected = [cb for cb in self.apps_checkboxes if cb.isChecked()]
        if not selected:
            QMessageBox.information(self, "Nada selecionado", "Selecione ao menos um app para desinstalar.")
            return

        confirm = QMessageBox.question(
            self, "Confirmar", f"Deseja remover {len(selected)} apps?", QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            for cb in selected:
                pkg = cb.objectName()
                self.run_adb(f"pm uninstall {pkg}")
                cb.setDisabled(True)
                cb.setChecked(False)
            self.status.setText(f"\ud83d\udcc9 {len(selected)} apps removidos.")