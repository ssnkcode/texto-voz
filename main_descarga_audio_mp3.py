from kokoro import KPipeline
import pyaudio
import numpy as np
import soundfile as sf


# Lista de voces disponibles
voces_disponibles = ['em_santa', 'em_alex', 'ef_dora']

# Mostrar opciones de voces al usuario
print("Voces disponibles:")
for i, voz in enumerate(voces_disponibles, 1):
    print(f"{i}. {voz}")

# Pedir al usuario que seleccione una voz
while True:
    try:
        seleccion = int(input("Selecciona el número de la voz que quieres usar (1-3): "))
        if 1 <= seleccion <= 3:
            voz_seleccionada = voces_disponibles[seleccion - 1]
            break
        else:
            print("Por favor, selecciona un número entre 1 y 3")
    except ValueError:
        print("Por favor, ingresa un número válido")

print(f"Voz seleccionada: {voz_seleccionada}")

# Inicializar el pipeline
pipeline = KPipeline(lang_code='e')

# Configurar PyAudio para reproducción en tiempo real
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=24000,
                output=True)

audio_counter = 1  # Contador para nombres de archivo únicos

while True:
    text = input("Introduce el texto a reproducir (o 'salir' para terminar): ")
    if text.lower() == 'salir':
        break
    
    # Lista para almacenar segmentos del audio actual
    current_audio_segments = []
    
    # Generar y reproducir audio en tiempo real con la voz seleccionada
    generator = pipeline(text, voice=voz_seleccionada)
    
    for i, (gs, ps, audio) in enumerate(generator):
        print(f"Reproduciendo segment {i}: {gs}")
        
        # Convertir tensor de PyTorch a array de NumPy y luego a float32
        audio_numpy = audio.cpu().numpy()
        audio_float32 = audio_numpy.astype(np.float32)
        stream.write(audio_float32.tobytes())
        
        # Guardar segmento del audio actual
        current_audio_segments.append(audio_float32)
    
    # Preguntar si quiere guardar este audio específico
    save_choice = input("¿Quieres guardar este audio en MP3? (s/n): ")
    if save_choice.lower() == 's':
        if current_audio_segments:
            # Combinar todos los segmentos del audio actual
            full_audio = np.concatenate(current_audio_segments)
            
            # Preguntar por el nombre del archivo con valor por defecto
            nombre_default = f"audio_generado_{audio_counter}.mp3"
            nombre_archivo = input(f"Nombre del archivo (Enter para '{nombre_default}'): ").strip()
            
            # Usar nombre por defecto si el usuario presiona Enter
            if not nombre_archivo:
                nombre_archivo = nombre_default
            else:
                # Asegurar que tenga extensión .mp3
                if not nombre_archivo.lower().endswith('.mp3'):
                    nombre_archivo += '.mp3'
            
            # Guardar como archivo MP3
            sf.write(nombre_archivo, full_audio, 24000, format='MP3')
            print(f"Audio guardado como: {nombre_archivo}")
            audio_counter += 1
        else:
            print("No hay audio para guardar")

# Cerrar el stream de audio
stream.stop_stream()
stream.close()
p.terminate()

print("Reproducción completada!")