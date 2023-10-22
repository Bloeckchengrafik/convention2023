#include <Arduino.h>
#include <Wire.h>
#include <VL53L0X.h>
#include "I2CScanner.h"
#include "TCA9548A.h"
#include "BluetoothSerial.h"

VL53L0X sensor;

bool measuring;
bool wasMeasuring;
I2CScanner scanner;

TCA9548A mux1(0x70);
TCA9548A mux2(0x70);

int measurement[10000];
int measurementCount = 0;

BluetoothSerial SerialBT;

void setup()
{
  Serial.begin(115200);
  SerialBT.begin("Scanner");
  
  Wire.begin(8, 9);
  mux1.begin(Wire);
  mux2.begin(Wire);

  mux1.closeAll();
  mux2.closeAll();

  // init 6 sensors at mux1 and 4 sensors at mux2
  for (int i = 0; i < 6; i++)
  {
    mux1.openChannel(i);
    if (sensor.init()) {
      Serial.print("Sensor initialized for mux1 channel ");
      Serial.println(i);
    } else {
      Serial.print("Failed to initialize sensor for mux1 channel ");
      Serial.println(i);
    }
    mux1.closeAll();
  }

  for (int i = 0; i < 4; i++)
  {
    mux2.openChannel(i);
    if (sensor.init()) {
      Serial.print("Sensor initialized for mux2 channel ");
      Serial.println(i);
    } else {
      Serial.print("Failed to initialize sensor for mux2 channel ");
      Serial.println(i);
    }
    mux2.closeAll();
  }
}

void createMeasurement(int* target, int id)
{
  int measurement[10];

  for (int i = 0; i < 6; i++)
  {
    mux1.openChannel(i);
    measurement[i] = sensor.readRangeSingleMillimeters();
    mux1.closeAll();
  }

  for (int i = 0; i < 4; i++)
  {
    mux2.openChannel(i);
    measurement[i + 6] = sensor.readRangeSingleMillimeters();
    mux2.closeAll();
  }

  SerialBT.print("M ");
  SerialBT.print(millis());
  SerialBT.print(" ");
  for (int i = 0; i < 10; i++)
  {
    SerialBT.print(measurement[i]);
    SerialBT.print(" ");
    target[i + (id * 10)] = measurement[i];
  }
  SerialBT.println();
}

#pragma region Stuff for demo only

/// @brief Process events from serial (not needed for swarm implementation)
void processEvents()
{
  // If we got a char on serial, process it
  if (Serial.available() || SerialBT.available())
  {
    char c = ' ';
    if (Serial.available())
    {
      c = Serial.read();
    }
    else if (SerialBT.available())
    {
      c = SerialBT.read();
    }

    switch (c)
    {
    case 'm':
      measuring = true;
      break;
    case 's':
      measuring = false;
      break;
    default:
      Serial.print("Unknown command: ");
      Serial.println(c);
      Serial.println("Available commands: m (measure), s (stop)");
      break;
    }
  }
}

#pragma endregion

/// @brief Get stuff done fast
void loop()
{
  processEvents(); // @todo: Remove this line for swarm implementation

  if (measuring)
  {
    if (!wasMeasuring)
    {
      SerialBT.print("INIT ");
      SerialBT.println(millis());
      measurementCount = 0;
    }
  }
  else
  {
    if (wasMeasuring)
    {
      SerialBT.println("END");
      // Send data
    }
  }

  wasMeasuring = measuring;

  if (measuring)
  {
    // Do measuring
    createMeasurement(measurement, measurementCount);
    measurementCount++;
    if (measurementCount >= 900)
    {
      measuring = false;
    }
  }
}
