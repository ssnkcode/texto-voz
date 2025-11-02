# 🗂️ Organizador de Archivos + 🎤 Conversor de Texto a Voz

Este proyecto:
- **Conversor de Texto a Voz**: Convierte texto a voz en tiempo real usando Kokoro TTS

## 📋 Requisitos Previos

- **Python 3.11** (Requerido)
- Git (opcional, para clonar el repositorio)

## 🛠️ Configuración del Entorno

### 1. Crear y activar entorno virtual
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

### 2. Instalar dependencias
```bash
# Instalar dependencias básicas
pip install torch torchaudio torchvision
pip install kokoro-tts
pip install soundfile
pip install numpy

# Instalar PyAudio - ELIGE UNA OPCIÓN:

# Opción 1: Método directo
pip install pyaudio

# Si la opción 1 falla, usa la Opción 2:
pip install pipwin
pipwin install pyaudio