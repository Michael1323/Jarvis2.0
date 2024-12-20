import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyaudio

# Configuración del reconocimiento de voz
r = sr.Recognizer()

# Configuración voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)  # Voz en español

# Nombre asistente
nombre_asistente = "yarvis"

# Almacenamos nuestro nombre
archivo_nombre = "nombre_usuario.txt"

def obtener_nombre_usuario():
    try:
        with open(archivo_nombre, 'r') as file:
            nombre = file.read()
            if nombre:
                return nombre
    except FileNotFoundError:
        pass
    return None

def establecer_nombre_usuario():
    hablar("Hola, soy yarvis. ¿Cuál es tu nombre?")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)

            nombre = r.recognize_google(audio, language='es')

            with open(archivo_nombre, 'w') as file:
                file.write(nombre)
                return nombre.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"Error al establecer nombre: {e}")
            return ""


def obtener_hora_actual():
    hora = datetime.datetime.now()
    hora = hora.strftime('%H:%M:%S')
    return hora

def obtener_saludo():
    hora = datetime.datetime.now()
    hora = hora.hour

    if 5 <= hora < 12:
        return "Buenos Días"
    elif 12 <= hora < 18:
        return "Buenas Tardes"
    else:
        return "Buenas Noches"

def escuchar_comando():
    try:
        mic = sr.Microphone()  # Crear explícitamente el objeto Micrófono
        with mic as source:  # Usamos el micrófono con el contexto "with"
            print("Escuchando comando...")
            r.adjust_for_ambient_noise(source, duration=1)  # Ajusta el ruido de fondo
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            comando = r.recognize_google(audio, language='es')
            print(f"Comando recibido: {comando}")
            return comando.lower()
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"Error al escuchar comando: {e}")
        return ""

def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

# Obtener el nombre del usuario, si existe
nombre_usuario = obtener_nombre_usuario()

if nombre_usuario:
    saludo = obtener_saludo()
    hora_actual = obtener_hora_actual()
    hablar(f"{saludo}, {nombre_usuario.capitalize()} | Son las {hora_actual}. ¿En qué puedo ayudarte?")
else:
    nombre_usuario = establecer_nombre_usuario()
    hablar(f"Mucho gusto, {nombre_usuario.capitalize()}")

# Bucle principal
while True:
    comando = escuchar_comando()  # Ahora esta función está definida

    if nombre_asistente.lower() in comando:
        hablar("¿En qué puedo ayudarte?")
    elif 'dormir' in comando:
        hablar("Durmiendo...")
        break  # Sale del bucle
    elif 'reproduce' in comando:
        busqueda = comando.replace('reproduce', '')
        hablar("Reproduciendo en YouTube " + busqueda)
        pywhatkit.playonyt(busqueda)
        hablar(f"¿En qué más puedo ayudarte?, {nombre_usuario.capitalize()}?")
    elif 'hora' in comando:
        hora_actual = obtener_hora_actual()
        hablar(f"La hora actual es {hora_actual}")
    else:
        hablar("No entendí tu petición. ¿Puedes repetir?")

# Aquí no es necesario el "else" después del bucle while
print("Yarvis está durmiendo...")
