#include <DHT.h>

#define DHTPIN 2   
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const int LED_VERDE = 4;
const int LED_ROSSO = 3;
float soglia_superiore = 30.0; 
float soglia_inferiore = 20.0; 

void setup() {
    Serial.begin(9600);
    dht.begin();
    pinMode(LED_VERDE, OUTPUT);
    pinMode(LED_ROSSO, OUTPUT);
}

void loop() {
    float umidita = dht.readHumidity();
    float temperatura = dht.readTemperature();

    if (isnan(umidita) || isnan(temperatura)) {
        Serial.println("Errore nella lettura del sensore!");
        return;
    }

    String stato_led = "Spenti";

    if (temperatura >= soglia_superiore) {
        digitalWrite(LED_ROSSO, HIGH);
        digitalWrite(LED_VERDE, LOW);
        stato_led = "Rosso acceso";
    } else if (temperatura <= soglia_inferiore) {
        digitalWrite(LED_ROSSO, LOW);
        digitalWrite(LED_VERDE, LOW);
        stato_led = "Spenti";
    } else {
        digitalWrite(LED_ROSSO, LOW);
        digitalWrite(LED_VERDE, HIGH);
        stato_led = "Verde acceso";
    }

    // Invia dati a Python (temperatura, umidità, stato LED)
    Serial.print(temperatura);
    Serial.print(",");
    Serial.print(umidita);
    Serial.print(",");
    Serial.println(stato_led);

    // Controlla se ci sono nuovi dati dalla porta seriale
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n'); // Legge la stringa fino a fine riga
        int commaIndex = input.indexOf(',');
        if (commaIndex != -1) {
            soglia_superiore = input.substring(0, commaIndex).toFloat();
            soglia_inferiore = input.substring(commaIndex + 1).toFloat();
        }
    }

    delay(2000); // Campionamento ogni 2 secondi
}