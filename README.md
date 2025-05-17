# NayTec Android Manager

🚀 Aplicativo Desktop moderno para gerenciamento avançado de dispositivos Android via ADB.

> Desenvolvido com PyQt5 e inspirado no visual refinado do macOS, com foco em performance, segurança e experiência premium.

---

## 🎨 Interface

- Estilo macOS com tema escuro (Dark Mode)
- Destaques neon: azul, verde e roxo
- Fonte: SF Pro
- Animações suaves e responsivas

---

## 🧩 Funcionalidades

### 📊 Dashboard
- Status de conexão via ADB
- Informações do dispositivo (nome, modelo, Android)
- Uso em tempo real de CPU, RAM, Armazenamento e Bateria

### 🧹 Otimização
- Limpeza de RAM com um clique
- Lista de apps com botão "Forçar Parada" e "Desinstalar"

### 🛡️ Antivírus
- Análise rápida
- Resultados com quarentena e exclusão de ameaças

### 📈 Desempenho
- Gráficos interativos (linha, área, pizza)
- Histórico de uso da CPU, RAM, armazenamento e bateria

---

## 🧪 Tecnologias

- Python 3.x
- PyQt5
- psutil
- pyqtgraph
- ADB (Android Debug Bridge)

---

## 📁 Estrutura

NayTec-Android-Manager/
├── controller/
├── model/
├── view/
├── resources/
│ ├── fonts/
│ ├── icons/
│ └── styles/
├── main.py


---

## ⚙️ Como executar

```bash
pip install -r requirements.txt
python main.py


Certifique-se de que o ADB está instalado e configurado no seu PATH.

