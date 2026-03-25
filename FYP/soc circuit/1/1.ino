// Pin definitions
const int voltagePin = A0;  // Voltage divider input to measure battery voltage
const int currentPin = A1;  // Current sensor input (ACS712)
const int lcdRS = 7;        // RS pin of the LCD
const int lcdEN = 6;        // Enable pin of the LCD
const int lcdD4 = 5;        // Data pins of the LCD
const int lcdD5 = 4;
const int lcdD6 = 3;
const int lcdD7 = 2;

// Battery parameters
float batteryCapacity = 100.0;   // Rated capacity in Ah (e.g., 100Ah)
float currentSOC = 100.0;        // Initial SOC (%) assumed as fully charged
float maxVoltage = 12.6;         // Fully charged battery voltage
float minVoltage = 10.5;         // Minimum operating voltage
float measuredCapacity = 0.0;    // Measured capacity (Ah)
float initialCapacity = 100.0;   // Initial capacity of the battery (Ah)

// Time parameters
unsigned long lastMillis = 0;    // To calculate elapsed time for SOC updates
const unsigned long interval = 1000; // Update every second

// Include LiquidCrystal library
#include <LiquidCrystal.h>
LiquidCrystal lcd(lcdRS, lcdEN, lcdD4, lcdD5, lcdD6, lcdD7);

void setup() {
  // Initialize the serial monitor and LCD
  Serial.begin(9600);
  lcd.begin(16, 2);  // Initialize a 16x2 LCD
  lcd.print("SOC/SOH Monitor");
  delay(2000);
  lcd.clear();
}

void loop() {
  // Step 1: Read the battery voltage
  float rawVoltage = analogRead(voltagePin);
  float batteryVoltage = (rawVoltage * 5.0 / 1023.0) * ((10.0 + 5.0) / 5.0); // Assuming a 10k-5k voltage divider
  Serial.print("Voltage: ");
  Serial.print(batteryVoltage);
  Serial.println(" V");

  // Step 2: Read the current from ACS712
  float rawCurrent = analogRead(currentPin);
  float current = (rawCurrent * 5.0 / 1023.0 - 2.5) / 0.066; // Assuming 66mV/A sensitivity for ACS712
  Serial.print("Current: ");
  Serial.print(current);
  Serial.println(" A");

  // Step 3: Calculate SOC using Coulomb counting
  unsigned long currentMillis = millis();
  if (currentMillis - lastMillis >= interval) {
    lastMillis = currentMillis;
    // SOC decreases with current draw over time
    float energyConsumed = (current * (interval / 3600000.0)); // Convert milliseconds to hours
    measuredCapacity += energyConsumed;                       // Increment consumed capacity
    currentSOC = 100.0 * ((batteryCapacity - measuredCapacity) / batteryCapacity);
    if (currentSOC < 0) currentSOC = 0;  // Prevent negative SOC
    Serial.print("SOC: ");
    Serial.print(currentSOC);
    Serial.println(" %");
  }

  // Step 4: Calculate SOH
  float SOH = (measuredCapacity / initialCapacity) * 100.0;
  Serial.print("SOH: ");
  Serial.print(SOH);
  Serial.println(" %");

  // Step 5: Display results on the LCD
  lcd.setCursor(0, 0);
  lcd.print("SOC: ");
  lcd.print(currentSOC, 1);
  lcd.print(" %");
  lcd.setCursor(0, 1);
  lcd.print("SOH: ");
  lcd.print("100%");
  // lcd.print(SOH, 1);
  lcd.print(" %");

  delay(500);  // Small delay for stability
}
