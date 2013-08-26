/*  
##Testing Environment for Xively Arduino Tutorial##  
This program is designed to test the sensing circuit created  
in the Xively Wi-Fi tutorial. It tests the photocell as well as the  
LED output. This sketch can be adapted to take sensor readings from any analog sensor.  
Derived from basicSensorTestEnv by Calum Barnes and AnalogInput by Tom Igoe  
  
By Calum Barnes 3-4-2013  
MIT License - [http://opensource.org/licenses/MIT]  
Copyright (c) 2013 Calum Barnes  
*/
  
/////////////////////////////////  
/////////////SETUP///////////////  
/////////////////////////////////  
const int analogInPin = A2;  // Analog input pin that sensors is attached to (DEFAULT=A2)  
int readingDelay = 10;  // Delay between each reading (DEFAULT=10)  
int readingsPerSample = 10;  // Number of reaings per sample / loop (DEFAULT=10)  
boolean singleRead = false;  // Series of readings (False) or single reading (TRUE) (DEFAULT=FALSE)  
boolean enableLED = true;  // LED  
const int ledPin = 9;  // Pin that Anode of LED is attached to (DEFAULT=13)  
/////////////////////////////////  
  
//vars  
int sensorValue = 0; // value read from the pot  
int outputValue = 0;  
int ledValue = 0;  
int sval;  
int sensorAvg;  
int tenTot;   
  
void setup() {  
 // initialize serial communications at 19200 bps:  
 Serial.begin(9600);   
  
 pinMode(analogInPin, INPUT);  //configure pin as input  
 pinMode(ledPin, OUTPUT);
}  
  
  
void loop() {  
 if(!singleRead){  
   //SAMPLE OF 10 READINGS   
   for (int i=0; i<readingsPerSample; i++){  //repeat number of times defined in setup  
     sval = analogRead(analogInPin);  //take single reading  
     tenTot = tenTot + sval;  //add up readings  
     delay(readingDelay);  //delay between readings as defined in setup. should be non 0  
   }  
   sensorAvg = (tenTot / 10);  //divide the total  
   tenTot = 0; //reset total variable  
   outputValue = sensorAvg;  //define smoothed, averaged reading  
 }else{   
   //STRAIGHT READINGS //only do this if singleRead=true   
   sensorValue = analogRead(analogInPin);  
   outputValue = sensorValue;  
 }  
  
  
 //print the data   
 Serial.print("Photocell= ");  
 Serial.println(outputValue);  //print the final value to serial mon  
  
 //turn on LED to level of the light  
 ledValue = map(outputValue, 0, 1023, 0, 255);  //changing output to single byte for pin  
 analogWrite(ledPin, ledValue);  //turn on led to specified level  
  
}  
