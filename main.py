import serial
import dearpygui.dearpygui as dpg
import time
import json
from threading import Timer

# Configurazione della porta seriale
PORTA_SERIALE = "COM6"  # Cambia con la tua porta seriale
BAUD_RATE = 9600

try:
    ser = serial.Serial(PORTA_SERIALE, BAUD_RATE, timeout=1)
    time.sleep(2)  # Attendi inizializzazione di Arduino
except serial.SerialException as e:
    print(f"Errore nell'apertura della porta seriale: {e}")
    ser = None

# Variabili per temperatura, umidità e soglie
temperatura = 0.0
umidita = 0.0
soglia_superiore = 25.0
soglia_inferiore = 20.0
stato_led = "Spenti"
storico_dati = []

# File per lo storico
data_file = "storico_temperatura.json"

# Funzione per leggere dati dalla porta seriale
def leggi_seriale():
    global temperatura, umidita, stato_led
    if ser and ser.in_waiting > 0:
        try:
            dati = ser.readline().decode('utf-8', errors='ignore').strip()
            valori = dati.split(",")
            if len(valori) == 3:
                temperatura = float(valori[0])
                umidita = float(valori[1])
                stato_led = valori[2]
        except ValueError:
            print("Errore nella conversione dei dati seriali")
        except Exception as e:
            print(f"Errore nella lettura seriale: {e}")

# Funzione per inviare le soglie ad Arduino
def invia_soglie():
    if ser:
        comando = f"{soglia_superiore},{soglia_inferiore}\n"
        ser.write(comando.encode())

# Funzione per aggiornare lo stato dei LED
def aggiorna_led():
    global stato_led
    if temperatura > soglia_superiore:
        stato_led = "LED Rosso"
    elif temperatura < soglia_inferiore:
        stato_led = "Tutti LED Spenti"
    else:
        stato_led = "LED Verde"

# Funzione per salvare lo storico dei dati
def salva_dati():
    global storico_dati
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    dati = {"timestamp": timestamp, "temperatura": temperatura, "umidita": umidita}
    storico_dati.append(dati)
    with open(data_file, "w") as file:
        json.dump(storico_dati, file, indent=4)

# Funzione per campionare dati ogni 10 secondi
def campionamento_dati():
    salva_dati()
    Timer(10, campionamento_dati).start()

# Funzione per aggiornare la soglia superiore
def aggiorna_soglia_superiore(sender, app_data):
    global soglia_superiore
    soglia_superiore = app_data
    invia_soglie()

# Funzione per aggiornare la soglia inferiore
def aggiorna_soglia_inferiore(sender, app_data):
    global soglia_inferiore
    soglia_inferiore = app_data
    invia_soglie()

# Funzione per gestire la GUI con i grafici
def applicazione_gui():
    dpg.create_context()
    dpg.create_viewport(title='Monitor Temperatura e Umidità', width=700, height=500)

    with dpg.window(label="Monitor", width=700, height=500):
        dpg.add_text("Temperatura:")
        temp_id = dpg.add_text(default_value=f"{temperatura} °C")
        dpg.add_text("Umidità:")
        umid_id = dpg.add_text(default_value=f"{umidita} %")

        dpg.add_slider_float(label="Soglia Superiore", min_value=15, max_value=30,
                             default_value=soglia_superiore, callback=aggiorna_soglia_superiore)
        dpg.add_slider_float(label="Soglia Inferiore", min_value=10, max_value=25,
                             default_value=soglia_inferiore, callback=aggiorna_soglia_inferiore)

        dpg.add_text("Stato LED:")
        led_id = dpg.add_text(default_value=stato_led)

        # Creazione grafici per temperatura e umidità
        with dpg.plot(label="Andamento Temperatura e Umidità", height=300, width=600):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Tempo")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Valori")

            temp_plot = dpg.add_line_series([], [], label="Temperatura", parent=y_axis)
            umid_plot = dpg.add_line_series([], [], label="Umidità", parent=y_axis)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Loop principale GUI
    tempo = []
    temp_valori = []
    umid_valori = []
    contatore = 0

    while dpg.is_dearpygui_running():
        leggi_seriale()
        aggiorna_led()

        dpg.set_value(temp_id, f"{temperatura} °C")
        dpg.set_value(umid_id, f"{umidita} %")
        dpg.set_value(led_id, stato_led)

        # Aggiornamento grafico
        tempo.append(contatore)
        temp_valori.append(temperatura)
        umid_valori.append(umidita)
        contatore += 1

        dpg.set_value(temp_plot, [tempo, temp_valori])
        dpg.set_value(umid_plot, [tempo, umid_valori])

        dpg.render_dearpygui_frame()

    dpg.destroy_context()
    if ser:
        ser.close()

# Avvio del programma
if __name__ == "__main__":
    campionamento_dati()
    applicazione_gui()