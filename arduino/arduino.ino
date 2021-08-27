#include <Servo.h>
#include <SharpIR.h>
#include "DHT.h"

// Servo
Servo servo;
#define servoPin 49

int angle =0;    // initial angle  for servo (beteen 1 and 179)
int angleStep =10;
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
  
  // IR setup
  pinMode(IRPin, INPUT);
  
  // DHT setup
  dht.begin();

  // Simulated componets setup
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0)
  {
    char data = Serial.read();

    // Open Drainage Port
    if (data == '0'){
      servo.write(0);
    }

    // Close Drainage Port
    else if (data == '1'){
      servo.write(90);
    }

    // Checking Cover Status
    else if (data == '2'){
      IRSensor();
    }

    // Water Pump Status
    else if (data == '3'){
      WaterPump();
    }

    // Ultrasonic cleaner
    else if (data == '4'){
      Washing();
    }

    // Fan Control On
    else if (data == '5'){
      fans();
    }

    // Fan Control Off
    else if (data == '6'){
      fanOff();
    }

    // Heating Element On
    else if (data == '7'){
      heating();
    }

    // Heating Element Off
    else if (data == '8'){
      heatingOff();
    }

    // LED Strip
    else if (data == '9'){
      LEDStrip();
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

void IRSensor()
{
  distance_cm = mySensor.distance();
  
  // Closed
  if (distance_cm <= 8)
  {
    Serial.println(1);
  }

  // Opened
  else
  {
    Serial.println(0);
  }
}

void WaterPump()
{
  digitalWrite(LED1, HIGH);
  delay(10000);
  digitalWrite(LED1, LOW);
  Serial.println("Done.");
}

void Washing()
{
  digitalWrite(LED2, HIGH);
  delay(10000);
  digitalWrite(LED2, LOW);
  Serial.println("Done.");
}

void fans()
{
  digitalWrite(LED3, HIGH);
}

void heating()
{
  delay(500);

  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(t))
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  Serial.println(t);
  
  if (t < 40){
    digitalWrite(LED4, HIGH);
    delay(1000);
    digitalWrite(LED4, LOW);
  }
  else {
    digitalWrite(LED4, HIGH);
  }
}

void LEDStrip()
{
  digitalWrite(LED5, HIGH);
  delay(10000);
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
