#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int sensor1 = 2; // IR sensor 1
const int sensor2 = 3; // IR sensor 2

int count = 0;
int sensor1State = 0;
int sensor2State = 0;
unsigned long lastTriggerTime = 0;

// LCD setup
LiquidCrystal_I2C lcd(0x27, 16, 2); // Change address if needed

void setup() {
  Serial.begin(9600);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("People Counter");
  lcd.setCursor(0, 1);
  lcd.print("Count: 0");
}

void loop() {
  sensor1State = digitalRead(sensor1);
  sensor2State = digitalRead(sensor2);

  // Entry detection: Sensor1 -> Sensor2
  if (sensor1State == LOW) {
    delay(80); // Reduced debounce delay
    if (digitalRead(sensor2) == LOW) {
      count++;
      Serial.print("Entry Detected | Count: ");
      Serial.println(count);
      updateLCD("Entry Detected", count);
      waitUntilClear();
    }
  }

  // Exit detection: Sensor2 -> Sensor1
  if (sensor2State == LOW) {
    delay(80); // Reduced debounce delay
    if (digitalRead(sensor1) == LOW) {
      count--;
      Serial.print("Exit Detected | Count: ");
      Serial.println(count);
      updateLCD("Exit Detected", count);
      waitUntilClear();
    }
  }
}

void waitUntilClear() {
  while (digitalRead(sensor1) == LOW || digitalRead(sensor2) == LOW) {
    delay(20);
  }
}

void updateLCD(const char* message, int currentCount) {
  lcd.setCursor(0, 0);
  lcd.print("                "); // Clear line 1 manually
  lcd.setCursor(0, 0);
  lcd.print(message);

  lcd.setCursor(0, 1);
  lcd.print("Count: ");
  lcd.print("     "); // Clear old number
  lcd.setCursor(7, 1);
  lcd.print(currentCount);
}
