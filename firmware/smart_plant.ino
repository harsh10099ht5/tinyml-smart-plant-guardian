#include <DHT.h>

// --------------------------------------------------
// Pin Configuration
// --------------------------------------------------

#define SOIL_MOISTURE_PIN 34
#define DHT_PIN 4
#define DHT_TYPE DHT11

#define LED_PIN 2
#define BUZZER_PIN 5

// --------------------------------------------------
// Sensor Object
// --------------------------------------------------

DHT dht(DHT_PIN, DHT_TYPE);

// --------------------------------------------------
// Soil Moisture Calibration
// --------------------------------------------------

// In values ko apne sensor ke according calibrate karna hoga.
const int SOIL_DRY_VALUE = 4095;
const int SOIL_WET_VALUE = 1500;

// Approximate time since last watering.
// Later, this value can be received from a button,
// RTC module, or mobile application.
float hoursSinceWatering = 2.0;


// --------------------------------------------------
// Setup
// --------------------------------------------------

void setup() {
  Serial.begin(115200);

  pinMode(SOIL_MOISTURE_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  dht.begin();

  delay(2000);

  Serial.println("Smart Plant Guardian Started");
  Serial.println(
    "soil_moisture,temperature,humidity,hours_since_watering"
  );
}


// --------------------------------------------------
// Read Soil Moisture Percentage
// --------------------------------------------------

int readSoilMoisture() {
  int rawValue = analogRead(SOIL_MOISTURE_PIN);

  int moisturePercentage = map(
    rawValue,
    SOIL_DRY_VALUE,
    SOIL_WET_VALUE,
    0,
    100
  );

  moisturePercentage = constrain(
    moisturePercentage,
    0,
    100
  );

  return moisturePercentage;
}


// --------------------------------------------------
// Alert Function
// --------------------------------------------------

void triggerAlert() {
  digitalWrite(LED_PIN, HIGH);
  digitalWrite(BUZZER_PIN, HIGH);

  delay(200);

  digitalWrite(BUZZER_PIN, LOW);
}


// --------------------------------------------------
// Main Loop
// --------------------------------------------------

void loop() {
  int soilMoisture = readSoilMoisture();

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Check whether DHT11 returned valid readings
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("DHT11 reading failed.");
    delay(2000);
    return;
  }

  // ------------------------------------------------
  // Basic plant condition rules
  // ------------------------------------------------

  bool needsWater = soilMoisture < 30;
  bool excessWaterRisk = soilMoisture > 85;
  bool highTemperature = temperature > 35;

  if (needsWater || highTemperature) {
    triggerAlert();
  } else {
    digitalWrite(LED_PIN, LOW);
    digitalWrite(BUZZER_PIN, LOW);
  }

  // ------------------------------------------------
  // CSV data output for Python script
  // ------------------------------------------------

  Serial.print(soilMoisture);
  Serial.print(",");

  Serial.print(temperature, 1);
  Serial.print(",");

  Serial.print(humidity, 1);
  Serial.print(",");

  Serial.println(hoursSinceWatering, 1);

  delay(5000);
}