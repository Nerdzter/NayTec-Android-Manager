from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider,
    QMessageBox, QScrollArea, QFrame, QCheckBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
import subprocess
import re

class Optimizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Optimizer")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove barra de título
        self.setStyleSheet("background-color: #121212;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # === LEFT PANEL (oculto parcial com menor largura) ===
        left_wrapper = QFrame()
        left_wrapper.setFixedWidth(240)
        left_wrapper.setStyleSheet("background-color: #1C1C1E;")
        left_panel = QVBoxLayout(left_wrapper)
        left_panel.setContentsMargins(20, 20, 20, 20)
        left_panel.setSpacing(15)

        # Limpeza
        left_panel.addWidget(self.section_label("Limpeza"))
        self.btn_cache = self.create_button("Limpar Cache", self.clean_cache)
        self.btn_close_apps = self.create_button("Fechar Apps em Segundo Plano", self.close_background_apps)
        left_panel.addWidget(self.wrap_shadow(self.btn_cache))
        left_panel.addWidget(self.wrap_shadow(self.btn_close_apps))

        # Gerenciamento
        left_panel.addWidget(self.section_label("Gerenciamento"))
        slider_layout = QVBoxLayout()
        self.slider_label = QLabel("Processos: 2")
        self.slider_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        slider_layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(4)
        self.slider.setValue(2)
        self.slider.valueChanged.connect(self.update_slider_label)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                height: 10px;
                background: #333;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #00BFFF, stop:1 #0050A0);
                border: 1px solid #00BFFF;
                width: 14px;
                height: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        slider_layout.addWidget(self.slider)
        left_panel.addLayout(slider_layout)

        self.btn_set_process_limit = self.create_button("Aplicar Limite de Processos", self.limit_background_processes)
        left_panel.addWidget(self.wrap_shadow(self.btn_set_process_limit))

        # Segurança
        left_panel.addWidget(self.section_label("Segurança"))
        self.btn_security = self.create_button("Analisar Segurança", self.analyze_security)
        self.btn_reboot = self.create_button("Reiniciar Dispositivo", self.reboot_device)
        left_panel.addWidget(self.wrap_shadow(self.btn_security))
        left_panel.addWidget(self.wrap_shadow(self.btn_reboot))

        left_panel.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(left_wrapper)

        # === RIGHT PANEL ===
        right_panel = QVBoxLayout()
        right_panel.setContentsMargins(40, 20, 40, 20)
        right_panel.setSpacing(15)

        app_title = QLabel("Aplicativos Instalados")
        app_title.setStyleSheet("font-size: 18px; font-weight: 500; color: white;")
        right_panel.addWidget(app_title)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #1C1C1E; border: none;")
        self.apps_container = QWidget()
        self.apps_layout = QVBoxLayout(self.apps_container)
        self.apps_layout.setSpacing(10)
        self.scroll.setWidget(self.apps_container)
        right_panel.addWidget(self.scroll, 1)

        uninstall_all_btn = QPushButton("Desinstalar Selecionados")
        uninstall_all_btn.setStyleSheet("background-color: #444; color: white; border-radius: 10px; padding: 10px; font-weight: bold;")
        uninstall_all_btn.clicked.connect(self.uninstall_selected_apps)
        right_panel.addWidget(self.wrap_shadow(uninstall_all_btn))

        self.status = QLabel("")
        self.status.setStyleSheet("font-size: 13px; color: #B0B0B0; margin-top: 10px;")
        right_panel.addWidget(self.status)

        layout.addLayout(right_panel, 2)

        self.apps_checkboxes = []
        self.load_apps()

    def section_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 16px; font-weight: 500; color: #B0B0B0; margin-top: 10px;")
        return lbl

    def update_slider_label(self):
        self.slider_label.setText(f"Processos: {self.slider.value()}")

    def create_button(self, text, action):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2A2A2E;
                color: white;
                border: 1px solid #3A3A3C;
                padding: 10px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3A3A3C;
            }
        """)
        btn.clicked.connect(action)
        return btn

    def wrap_shadow(self, widget):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        frame.setStyleSheet("background-color: transparent; border: none;")
        return frame

    def run_adb(self, cmd):
        try:
            output = subprocess.check_output(["adb", "shell"] + cmd.split(), encoding="utf-8")
            return output.strip()
        except Exception as e:
            return f"Erro: {e}"

    def clean_cache(self):
        self.status.setText("Limpando cache...")
        result = self.run_adb("pm trim-caches 9999999999")
        self.status.setText("Cache limpo!" if "Erro" not in result else result)

    def close_background_apps(self):
        self.status.setText("Fechando apps...")
        result = self.run_adb("am kill-all")
        self.status.setText("Apps fechados." if "Erro" not in result else result)

    def limit_background_processes(self):
        val = self.slider.value()
        result = self.run_adb(f"settings put global max_background_processes {val}")
        self.status.setText("Limite aplicado." if "Erro" not in result else result)

    def analyze_security(self):
        self.status.setText("Analisando apps...")
        result = self.run_adb("pm list packages -d")
        if result:
            QMessageBox.information(self, "Apps Desativados", result)
        else:
            QMessageBox.information(self, "Seguro", "Nenhum app desativado.")
        self.status.setText("Análise concluída.")

    def reboot_device(self):
        reply = QMessageBox.question(self, "Confirmar", "Reiniciar dispositivo?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.status.setText("Reiniciando...")
            self.run_adb("reboot")

    def load_apps(self):
        self.status.setText("Carregando apps...")
        try:
            packages_output = subprocess.check_output([
                "adb", "shell", "pm", "list", "packages", "-3"
            ], encoding="utf-8")
            packages = [line.replace("package:", "").strip() for line in packages_output.splitlines()]
            self.apps_checkboxes.clear()

            for pkg in packages:
                try:
                    label_output = subprocess.check_output([
                        "adb", "shell", "dumpsys", "package", pkg
                    ], encoding="utf-8")
                    match = re.search(r"application-label:'([^']+)'", label_output)
                    label = match.group(1) if match else pkg
                except:
                    label = pkg

                cb = QCheckBox(label)
                cb.setObjectName(pkg)
                cb.setStyleSheet("color: white; font-size: 14px; background-color: #2A2A2E; border-radius: 10px; padding: 8px;")
                self.apps_checkboxes.append(cb)
                self.apps_layout.addWidget(cb)

            self.status.setText(f"{len(packages)} apps carregados.")

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
            self.status.setText(f"{len(selected)} apps removidos.")
