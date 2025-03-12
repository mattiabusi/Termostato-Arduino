# Termostato Arduino

Un **termostato basato su Arduino** che utilizza un **sensore di temperatura e umidità DHT11** per monitorare l'ambiente e attivare LED di segnalazione in base alla temperatura rilevata.

##  Funzionalità
- Misura **temperatura e umidità** con il sensore **DHT11**.
- Accende un **LED rosso** se la temperatura è **superiore a 30°C**.
- Accende un **LED verde** se la temperatura è **inferiore a 20°C**.
- Invio dei dati alla porta seriale per monitoraggio in tempo reale.
- 
##  Componenti Hardware
- **Arduino Uno**
- **Sensore DHT11** (Temperatura e Umidità)
- **LED Verde** (collegato al pin 4)
- **LED Rosso** (collegato al pin 3)
- **Resistenze da 220Ω** (per i LED)

##  Requisiti Software
- **Arduino IDE**
- Libreria **DHT** per il sensore  
  
##  Schema di Collegamento
- **DHT11**  
  - VCC → **5V**  
  - GND → **GND**  
  - Data → **Pin 2**  
- **LED Verde** → **Pin 4**  
- **LED Rosso** → **Pin 3**
  




