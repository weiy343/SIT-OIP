#include <Servo.h>
#include <SharpIR.h>
#include "DHT.h"

// Servo
Servo servo;
#define servoPin 49

int angle = 90;   // initial angle  for servo (beteen 1 and 179)
int angleStep = 10;
const int minAngle = 0;
const int maxAngle = 90;

// DHT Sensor
#define DHTPIN 53
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// IR Sensor
#define IRPin A15
#define model 1080

int distance_cm;

SharpIR mySensor = SharpIR(IRPin, model);

// Simulated Components
int LED1 = 4;       //Green Pump
int LED2 = 5;       //Orange Washing
int LED3 = 6;       //Red Fan
int LED4 = 7;      //Red Heating
int LED5 = 8;      //Yellow LED Strip

void setup() {
  // Servo setup
  servo.attach(servoPin);
  servo.write(angle);
  
  // IR setup
  pinMode(IRPin, INPUT);
  
  // DHT setup
  dht.begin();

  // Simulated componets setup
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0)
  {
    char command = Serial.read();
    int timer = Serial.parseInt();
    timer = timer * 1000;

    // Pump & Wash
    if (command == '0'){
      int isOpen = IRSensor();
      if (isOpen){
        Serial.println(isOpen);
        return;
      }
      waterPump(timer); // returns complete
      washing(timer); // returns complete
      drain(timer); // returns complete
    }

    // Sterilize
    else if (command == '1'){
      waterPump(timer); // Returns complete
      heatedFan(timer); // returns complete
      drain(timer); // returns complete
    }

    // Dry
    else if (command == '2'){
      servo.write(90); // ensure open
      heatedFan(timer); // returns complete
    }
    
    // LED check
    else if (command == '3'){
      LEDStrip(timer);
    }
  }
}

void DHTSensor()
{
  delay(1000);
  
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t))
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F(" Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(F(" Humidity: "));
  Serial.print(h);
  Serial.print(F("% "));
  Serial.print(F(" Heat index: "));
  Serial.print(hic);
  Serial.println(F("C "));
}

int IRSensor()
{
  distance_cm = mySensor.distance();
  
  // Closed
  if (distance_cm <= 8)
  {
    return 0;
  }

  // Opened
  else
  {
    return 1;
  }
}

void waterPump(int timer)
{
  servo.write(90); // ensure close
  digitalWrite(LED1, HIGH);
  delay(timer);
  digitalWrite(LED1, LOW);
  Serial.println("Done.");
}

void washing(int timer)
{
  digitalWrite(LED2, HIGH);
  delay(timer);
  digitalWrite(LED2, LOW);
  Serial.println("Done.");
}

void drain(int timer)
{
  servo.write(0);
  delay(timer);
  servo.write(90);
  Serial.println("Done.");
}

void heatedFan(int timer){
  fans();
  heating(); // Returns temp
  delay(timer);
  fanOff();
  heatingOff();
  Serial.println("Done.");
}

void fans()
{
  digitalWrite(LED3, HIGH);
}

void heating()
{
  // Read temperature as Celsius (the default)
  float t = dht.readHumidity();

  // Check if any reads failed and exit early (to try again).
  if (isnan(t))
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  while(t < 70){
    Serial.println(t);
    digitalWrite(LED4, HIGH);
    delay(500);
    digitalWrite(LED4, LOW);
    t = dht.readHumidity();
  }
  Serial.println(t);
  digitalWrite(LED4, HIGH);
}

void LEDStrip(int timer)
{
  digitalWrite(LED5, HIGH);
  delay(timer);
  digitalWrite(LED5, LOW);
}

void fanOff()
{
  digitalWrite(LED3, LOW);
}

void heatingOff()
{
  digitalWrite(LED4, LOW);
}
