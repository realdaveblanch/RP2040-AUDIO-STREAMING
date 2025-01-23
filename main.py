import network
import time
import ustruct
import math
import random
import usocket

# Datos de la red Wi-Fi
ssid = "xxxxx"
password = "xxxxxx"

# Configurar la conexión Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Esperar a que se conecte
while not wlan.isconnected():
    time.sleep(1)

# Imprimir la dirección IP obtenida
print("Conectado a Wi-Fi")
print("Dirección IP:", wlan.ifconfig()[0])
# Configurar el pin del LED como salida
led = machine.Pin("LED", machine.Pin.OUT)

# Generar un tono de audio aleatorio en formato WAV
def generate_random_tone():
    sample_rate = 8000  # Frecuencia de muestreo (8 kHz)
    duration = 0.05  # Duración en segundos por cada tono (ajustable)
    frequency = 440 + random.randint(0, 10000)  # Frecuencia aleatoria entre 440 y 940 Hz

    # Número de muestras por duración del tono
    num_samples = int(sample_rate * duration)
    
    # Cabecera WAV (simplificada para un canal mono y 2 bits)
    header = bytearray(44)
    ustruct.pack_into('<4s', header, 0, b'RIFF')
    ustruct.pack_into('<I', header, 4, 36 + num_samples * 1)  # 1 byte por muestra
    ustruct.pack_into('<4s', header, 8, b'WAVE')
    ustruct.pack_into('<4s', header, 12, b'fmt ')
    ustruct.pack_into('<I', header, 16, 16)
    ustruct.pack_into('<H', header, 20, 1)
    ustruct.pack_into('<H', header, 22, 1)
    ustruct.pack_into('<I', header, 24, sample_rate)
    ustruct.pack_into('<I', header, 28, sample_rate * 1)  # 1 byte por muestra
    ustruct.pack_into('<H', header, 32, 1)
    ustruct.pack_into('<H', header, 34, 2)  # 2 bits por muestra
    ustruct.pack_into('<4s', header, 36, b'data')
    ustruct.pack_into('<I', header, 40, num_samples * 1)  # 1 byte por muestra

    # Elección aleatoria de tipo de onda
    wave_type = random.choice(['sine', 'square', 'triangle', 'fm'])

    data = bytearray()

    for i in range(num_samples):
        if wave_type == 'sine':
            # Onda Senoidal
            
            sample_value = int(128 + 127 * math.sin(2 * math.pi * frequency * (i / sample_rate)))
        
        elif wave_type == 'square':
            # Onda Cuadrada
      
            sample_value = 128 if (i // (sample_rate / frequency)) % 2 == 0 else 0
  
        elif wave_type == 'triangle':
            # Onda Triangular
     
            sample_value = int(128 + 127 * (2 * (i / (sample_rate / frequency)) - 1) % 2 - 1)
         
        elif wave_type == 'noise':
            # Ruido blanco
    
            sample_value = random.randint(0, 255)
         
        elif wave_type == 'fm':
            # Onda con Modulación de Frecuencia (FM)
          
            modulated_frequency = frequency + 50 * math.sin(2 * math.pi * 2 * (i / sample_rate))  # FM simple
            sample_value = int(128 + 127 * math.sin(2 * math.pi * modulated_frequency * (i / sample_rate)))
          
        
        # Mapeo de 8 bits a 2 bits (niveles 0, 85, 170, 255)
        if sample_value < 64:
            sample_value = 0
        elif sample_value < 128:
            sample_value = 85
        elif sample_value < 192:
            sample_value = 170
        else:
            sample_value = 255
    
        # Añadir la muestra al buffer de datos
        data.append(sample_value)
        
    return header + data

# Servidor HTTP para transmitir el audio
def simple_server():
    addr = usocket.getaddrinfo('0.0.0.0', 8081)[0][-1]  # Cambié el puerto a 8081
    s = usocket.socket()
    s.bind(addr)
    s.listen(1)
    print('Esperando conexión en', addr)

    while True:
        cl, addr = s.accept()
        print('Cliente conectado desde', addr) 
        request = cl.recv(1024)  # Leer la solicitud del cliente
        print("Request:", request)
        led.on()

        # Enviar cabecera HTTP
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: audio/wav\r\n"
        response += "Connection: keep-alive\r\n"
        response += "\r\n"

        # Enviar la cabecera inicial
        cl.send(response)
        
        try:
            
            while True:
                # Enviar continuamente los tonos como stream
                cl.send(generate_random_tone())  # Enviar tono aleatorio en vivo
                #time.sleep(0.1)  # Ajusta el intervalo entre tonos (en segundos)
        except OSError:
            # Si el cliente cierra la conexión, se maneja el error
            print("Conexión cerrada por el cliente.")
            led.off()
            cl.close()

# Ejecutar el servidor
simple_server()

