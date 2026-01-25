import sys
import os
import multiprocessing
import yt_dlp
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# --- WORKER THREAD (Para não travar a tela) ---
class DownloadThread(QThread):
    finished = pyqtSignal(str)  # Sinal de sucesso (envia o caminho do arquivo)
    error = pyqtSignal(str)     # Sinal de erro (envia a mensagem de erro)

    def __init__(self, url, quality):
        super().__init__()
        self.url = url
        self.quality = quality

    def run(self):
        # Define o caminho direto para a pasta Música
        music_folder = os.path.join(os.path.expanduser('~'), 'Music')
        
        # Configuração do yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(music_folder, '%(title)s.%(ext)s'), # Salva direto no destino com o nome do vídeo
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': self.quality,
            }],
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                # Pega o título limpo para mostrar na mensagem final
                filename = ydl.prepare_filename(info)
                final_filename = os.path.splitext(filename)[0] + ".mp3"
                
            self.finished.emit(final_filename)
        except Exception as e:
            self.error.emit(str(e))

# --- JANELA PRINCIPAL ---
class AudioTrimApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Download de Música (YouTube)')
        self.setGeometry(100, 100, 450, 220)

        # Estilo visual (Opcional: Deixa um pouco mais moderno)
        self.setStyleSheet("""
            QWidget { font-size: 14px; }
            QPushButton { padding: 8px; font-weight: bold; }
            QLineEdit { padding: 5px; }
        """)

        self.urlLabel = QLabel("Insira a URL do vídeo:")
        self.urlLineEdit = QLineEdit()
        self.urlLineEdit.setPlaceholderText("Cole o link aqui...")
        
        self.qualityLabel = QLabel("Qualidade (kbps):")
        self.qualityComboBox = QComboBox()
        self.qualityComboBox.addItems(["192", "320", "128"]) # 192 é o padrão ideal
        
        self.urlbutton = QPushButton('Baixar e Converter')
        self.urlbutton.clicked.connect(self.startDownload)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.urlLabel)
        layout.addWidget(self.urlLineEdit)
        layout.addSpacing(10)
        layout.addWidget(self.qualityLabel)
        layout.addWidget(self.qualityComboBox)
        layout.addSpacing(20)
        layout.addWidget(self.urlbutton)
        self.setLayout(layout)

    def startDownload(self):
        youtube_url = self.urlLineEdit.text()
        quality = self.qualityComboBox.currentText()

        if not youtube_url:
            QMessageBox.warning(self, "Atenção", "O campo de URL está vazio.")
            return

        # Desabilita o botão para evitar cliques duplos
        self.urlbutton.setEnabled(False)
        self.urlbutton.setText("Baixando... Aguarde.")

        # Inicia a Thread de Download
        self.thread = DownloadThread(youtube_url, quality)
        self.thread.finished.connect(self.onDownloadFinished)
        self.thread.error.connect(self.onDownloadError)
        self.thread.start()

    def onDownloadFinished(self, filepath):
        self.urlbutton.setEnabled(True)
        self.urlbutton.setText("Baixar e Converter")
        self.urlLineEdit.clear()
        QMessageBox.information(self, 'Sucesso', f'Música salva em:\n{filepath}')

    def onDownloadError(self, error_msg):
        self.urlbutton.setEnabled(True)
        self.urlbutton.setText("Baixar e Converter")
        QMessageBox.critical(self, 'Erro', f'Falha no download:\n{error_msg}')

def main():
    app = QApplication(sys.argv)
    trimApp = AudioTrimApp()
    trimApp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # Essa linha avisa o Windows: "Se eu for um processo filho, não rode a main() de novo!"
    multiprocessing.freeze_support()
    main()