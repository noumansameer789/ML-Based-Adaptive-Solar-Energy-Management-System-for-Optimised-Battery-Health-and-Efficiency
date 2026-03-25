#include <OneWire.h>
#include <DallasTemperature.h> // 18b20 temp sensor
#include <LiquidCrystal_I2C.h> // LCD display
#include "ThingSpeak.h" // server
#include <WiFi.h>
#define DS18B20_PIN 2

// Voltage ADCs
#define CELL1_PIN 34
#define CELL2_PIN 39
#define CELL3_PIN 36

#define SECRET_SSID "Redmi Note 11"
#define SECRET_PASS "12347890"

WiFiClient client;

unsigned long myChannelNumber =  2976035;
const char * myWriteAPIKey = "Z5P3KWD7QB8FRKIY";

// Timing
unsigned long lastSensorRead = 0;
unsigned long cycleTime = 10000; // 10 seconds
unsigned long lastCycleMillis = 0;

// ACS712
#define CHARGE_CURRENT_PIN 32
#define LOAD_CURRENT_PIN 35

// Relay Control
#define RELAY_CHARGE 18
#define RELAY_LOAD   19

int check_pi1 = 4;
int check_pi2 = 16;

// Constants for ACS712
const float ACS_OFFSET = 1.65; // Adjust as per your system supply
const float ACS_SENSITIVITY = 0.185; // For ACS712-5A version

// LCD
LiquidCrystal_I2C lcd(0x27, 16, 2); // Adjust address if needed
OneWire oneWire(DS18B20_PIN);
DallasTemperature sensors(&oneWire);

// === Utility Functions ===
float readVoltage(int pin, float R1, float R2) {
  int adc = analogRead(pin);
  float v = (adc / 4095.0) * 3.3;
  return v * ((R1 + R2) / R2); // Voltage divider
}

float readAverageCurrent(int pin, int samples = 50) {
  float sum = 0;
  for (int i = 0; i < samples; i++) {
    float voltage = analogRead(pin) / 4095.0 * 3.3;
    sum += (voltage - ACS_OFFSET) / ACS_SENSITIVITY;
    delay(2); // small delay between samples
  }
  return sum / samples;
}

float estimateSoC(float voltage) {
  // For 3S battery: 9.6V (0%) to 12.6V (100%)
  float soc = (voltage - 9.6) / (12.6 - 9.6) * 100.0;
  return constrain(soc, 0.0, 100.0);
}

float estimateHealth(float fullVoltage) {
  // Health estimate: how close full charge is to ideal 12.6V
  float health = (fullVoltage / 12.6) * 100.0;
  return constrain(health, 0.0, 100.0);
}

void setup() {
  Serial.begin(115200);
  lcd.init(); lcd.backlight();
  lcd.setCursor(0,0); lcd.print("SMART BMS");
  sensors.begin();

  WiFi.mode(WIFI_STA);
  ThingSpeak.begin(client);

  WiFi.begin(SECRET_SSID, SECRET_PASS);
  Serial.print("Connecting to Wi-Fi");
  delay(1000);
  
  while (WiFi.status() != WL_CONNECTED) {
    lcd.print(".");
    Serial.print(".");
    delay(300);
  }
  
  Serial.println();
  Serial.print("Connected with IP: ");
  lcd.clear();
  lcd.setCursor(0, 1);
  lcd.print("System Online");
  
  pinMode(RELAY_CHARGE, OUTPUT);
  pinMode(RELAY_LOAD, OUTPUT);
  digitalWrite(RELAY_CHARGE, LOW);
  digitalWrite(RELAY_LOAD, LOW);

  pinMode(check_pi1,INPUT);
  pinMode(check_pi2,INPUT);

  delay(2000); lcd.clear();
}

void loop() {
  // === Read Temperature ===
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);

  // === Read Voltages ===
  float cell1 = readVoltage(CELL1_PIN, 2200, 1900);
  float cell2 = readVoltage(CELL2_PIN, 8800, 3375);
  float cell3 = readVoltage(CELL3_PIN, 8800, 2000);  // total voltage

  float totalVolt = cell3;
  float soc = estimateSoC(totalVolt);
  float health = estimateHealth(totalVolt); // Simplified health logic

  // === Read Currents (Averaged) ===
  float chargeCurrent = readAverageCurrent(CHARGE_CURRENT_PIN);
  chargeCurrent = chargeCurrent+0.2;
  float loadCurrent = readAverageCurrent(LOAD_CURRENT_PIN);
  loadCurrent = loadCurrent-0;
  
  // === Serial Monitor ===
  Serial.print("C1:"); Serial.print(cell1, 2);
  Serial.print(" C2:"); Serial.print(cell2, 2);
  Serial.print(" C3:"); Serial.print(cell3, 2);
  Serial.print(" | Temp: "); Serial.print(tempC, 1);
  Serial.print("C | I+:"); Serial.print(chargeCurrent, 2);
  Serial.print(" I-:"); Serial.println(loadCurrent, 2);

  
  // === Safety Checks ===
  bool safeVoltage = (cell1 < 4.2 && cell2 < 4.2 && cell3 < 4.2) && 
                     (cell1 > 3.0 && cell2 > 3.0 && cell3 > 3.0);
  bool safeTemp = (tempC < 50.0);
  bool safeCharge = (abs(chargeCurrent) < 4.5);
  bool safeLoad = (abs(loadCurrent) < 6.0);
  
  bool pi_status = digitalRead(check_pi1);
  
  // === Relay Logic ===
//  digitalWrite(RELAY_CHARGE, safeVoltage && safeTemp && safeCharge ? HIGH : LOW);
  digitalWrite(RELAY_LOAD, safeVoltage && safeTemp ? HIGH : LOW);
  lcd.setCursor(14,0);lcd.print(digitalRead(check_pi1));lcd.print(digitalRead(check_pi2));
  
  if(digitalRead(check_pi1) == 1 && digitalRead(check_pi2)==1)
  {
    Serial.println("in11");
    if(soc<20)
    {
      Serial.println("soc<20");
      digitalWrite(RELAY_CHARGE,LOW);
    }
    else
    {
      Serial.println("soc>20");
      digitalWrite(RELAY_CHARGE,HIGH);
    }
  }

  else if(digitalRead(check_pi1) == 1 && digitalRead(check_pi2)==0)
  {
    if(soc<40)
    {
      digitalWrite(RELAY_CHARGE,LOW);
    }
    else
    {
      digitalWrite(RELAY_CHARGE,HIGH);
    }
  }
  
    else if(digitalRead(check_pi1) == 0 && digitalRead(check_pi2)==1)
  {
    if(soc<60)
    {
      digitalWrite(RELAY_CHARGE,LOW);
    }
    else
    {
      digitalWrite(RELAY_CHARGE,HIGH);
    }
  }

    else if(digitalRead(check_pi1) == 0 && digitalRead(check_pi2)==0)
  {
    if(soc<80)
    {
      digitalWrite(RELAY_CHARGE,LOW);
    }
    else
    {
      digitalWrite(RELAY_CHARGE,HIGH);
    }
  }

//  else
//  {
//    digitalWrite(RELAY_CHARGE,LOW);
//  }
  // === LCD Display ===
  lcd.setCursor(0, 0);
  lcd.print("SoC:"); lcd.print(soc, 0); lcd.print("% ");
  lcd.print(" T:"); lcd.print(tempC, 0); 

  lcd.setCursor(0, 1);
  lcd.print("H:"); lcd.print(health, 0); lcd.print("% ");
  lcd.print("  V:"); lcd.print(totalVolt, 1); lcd.print("I");
  delay(1500);lcd.clear();
  
  lcd.setCursor(0, 0);
  lcd.print("Charge I:"); lcd.print(abs(chargeCurrent), 1);   lcd.print(" Amps");

  lcd.setCursor(0, 1);
  lcd.print("load I:"); lcd.print(loadCurrent, 1);   lcd.print(" Amps");

   // --- Update ThingSpeak ---
    ThingSpeak.setField(1, totalVolt);
    ThingSpeak.setField(2, abs(chargeCurrent));
    ThingSpeak.setField(3, health);
    ThingSpeak.setField(4, soc);
    ThingSpeak.setField(5, tempC);

    int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
    if (x == 200) {
      Serial.println("Channel update successful.");
    } else {
      Serial.println("Problem updating channel. HTTP error code " + String(x));
    }
    
  delay(1000);lcd.clear();
}
