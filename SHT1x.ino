#include <SHT1x.h>
#define dataPin 10
#define clockPin 11
SHT1x sht1x(dataPin, clockPin);

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up");
}

void loop(){
  float tempF = sht1x.readTemperatureF();
  float humidity = sht1x.readHumidity();
  //float tempF = sht1x.readHumidity();
  Serial.print(tempF);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print("\n");
  delay(500);
}
