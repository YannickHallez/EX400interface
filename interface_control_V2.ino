
#define SensorFlow A0     // Pin where the flow sensor is connected
#define SensorPressure A1  // Pin where the pressure sensor is connected

int flowReading;      // débit
int pressureReading;   // pression

void setup() {
  Serial.begin(9600);  // Démarrer la communication série
}

void loop() {
  // Remplir les tableaux pendant 4 secondes
    flowReading = analogRead(SensorFlow);
    pressureReading = analogRead(SensorPressure);

  // Envoyer les valeurs accumulées sur le port série
    Serial.print("Flow ");
    Serial.println(flowReading);

    Serial.print("Pressure ");
    Serial.println(pressureReading);

  // Attendre 0.100 secondes avant de recommencer le cycle
    delay(100);  
}
