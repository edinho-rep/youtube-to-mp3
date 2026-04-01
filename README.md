# 🎵 YouTube to MP3 Downloader

App desktop com interface gráfica para baixar e converter vídeos do YouTube diretamente para MP3, desenvolvido em Python.

![Preview do App](2026-01-25_01-03.png)

---

## 🚀 Funcionalidades

- **Interface gráfica** intuitiva construída com PyQt5
- **Seleção de qualidade** de áudio: 128, 192 ou 320 kbps
- **Download sem travar a tela** — processamento em thread separada via `QThread`
- **Conversão automática** para MP3 usando FFmpeg
- **Salvamento direto** na pasta `Música` do usuário
- **Compatível com Windows** — pode ser empacotado como `.exe` com PyInstaller

---

## 🛠️ Tecnologias

| Biblioteca | Função |
|---|---|
| **Python 3** | Linguagem base |
| **PyQt5** | Interface gráfica (GUI) |
| **yt-dlp** | Engine de download do YouTube |
| **FFmpeg** | Conversão e extração de áudio |
| **PyInstaller** | Geração de executável `.exe` |

---

## ⚙️ Pré-requisitos

### FFmpeg (obrigatório para conversão de áudio)

No Windows 10/11, instale via PowerShell:

```powershell
winget install ffmpeg
```

### Dependências Python

```bash
pip install PyQt5 yt-dlp
```

---

## ▶️ Como usar

```bash
python convert_ytb_mp3_v2.py
```

1. Cole a URL do vídeo do YouTube no campo indicado
2. Selecione a qualidade de áudio desejada (padrão: 192 kbps)
3. Clique em **Baixar e Converter**
4. O arquivo MP3 será salvo automaticamente na pasta `Música` do seu usuário

---

## 📦 Gerar Executável (.exe)

Para distribuir o app sem precisar do Python instalado:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name="BaixarMusica" convert_ytb_mp3_v2.py
```

O executável será gerado na pasta `dist/`.

---

## 🧠 Como funciona

O app utiliza `QThread` para executar o download em segundo plano, evitando que a interface congele durante o processo. Ao finalizar, emite um sinal (`pyqtSignal`) de sucesso ou erro para a thread principal, que atualiza a UI de forma segura.

```
URL → yt-dlp (download) → FFmpeg (conversão) → MP3 salvo em ~/Music
```

---

## 📁 Estrutura do Projeto

```
youtube-to-mp3/
├── convert_ytb_mp3_v2.py   # Código principal
├── README.md
└── screenshot.png          # Preview da interface
```

---

