#include <Time.h>
#include <SD.h>
#include <SHT1x.h>
#define dataPin 4
#define clockPin 3
#define MQ4pin 0
#define MQ8pin 1
SHT1x sht1x(dataPin, clockPin);
int led = 5;  // status led pin
File myFile;  // data file on the SD card
String timestamp;  // timestamp for each data line

#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by Unix time_t as ten ASCII digits
#define TIME_HEADER  'T'   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message 

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up");
  pinMode(led, OUTPUT);
  pinMode(10, OUTPUT);
  SD.begin();
}

void loop(){
  // prep SD card file
  myFile = SD.open("test2.txt", FILE_WRITE);
  if (!myFile) {
    // if the file didn't open, print an error:
    Serial.println("error opening test.txt");
    SD.begin();
  }
  
  // get timestamp
  if(Serial.available() ) 
  {
    processSyncMessage();
  }
  //if(timeStatus() == timeNotSet){
    //if (myFile)
    //  myFile.print("00000000000000");
    //Serial.print("00000000000000");
    //Serial.print("\n");
  //}
  //else{  
  // if not sync'd, it will just start at 1970   
  timestamp = digitalClockDisplay();  
  if (myFile)
    myFile.print(timestamp+",");
  Serial.print(timestamp+",");
  //} 
  
  // read temp and humidity
  float tempF = sht1x.readTemperatureF();
  float humidity = sht1x.readHumidity();
  if (myFile){
    //myFile.print(tempF)+","+String(humidity)+",");
    myFile.print(tempF);
    myFile.print(",");
    myFile.print(humidity);
  }
  Serial.print(tempF);
  Serial.print(",");
  Serial.print(humidity);
  
  // read gas sensors
  int valMQ4, valMQ8;
  valMQ4 = analogRead(MQ4pin);
  valMQ8 = analogRead(MQ8pin);
  if (myFile){
    myFile.print(",");
    myFile.print(valMQ4);
    myFile.print(",");
    myFile.print(valMQ8);
    myFile.print("\n");
  }
  Serial.print(',');
  Serial.print(valMQ4);//Print the value to serial port
  Serial.print(',');
  Serial.println(valMQ8);
  
  myFile.close();
  
  // blink the LED again
  // blink the LED so we know it's alive
  analogWrite(led, 0); 
  delay(1000);  
  analogWrite(led, 5);  
}


String digitalClockDisplay(){
  // digital clock display of the time
  String timestamp="";
  timestamp += year();
  timestamp += printDigits(month());
  timestamp += printDigits(day());
  timestamp += printDigits(hour());
  timestamp += printDigits(minute());
  timestamp += printDigits(second());
  
  return timestamp;
}

String printDigits(int digits){
  // utility function for digital clock display: print leading 0
  String digitstr = "";
  if(digits < 10)
    digitstr = '0'+String(digits);
  else
    digitstr = String(digits);
  //Serial.print(digits);
  return digitstr;
}

void processSyncMessage() {
  // if time sync available from serial port, update time and return true
  while(Serial.available() >=  TIME_MSG_LEN ){  // time message consists of header & 10 ASCII digits
    char c = Serial.read() ; 
    Serial.print(c);  
    if( c == TIME_HEADER ) {       
      time_t pctime = 0;
      for(int i=0; i < TIME_MSG_LEN -1; i++){   
        c = Serial.read();          
        if( c >= '0' && c <= '9'){   
          pctime = (10 * pctime) + (c - '0') ; // convert digits to a number    
        }
      }   
      setTime(pctime);   // Sync Arduino clock to the time received on the serial port
    }  
  }
}
