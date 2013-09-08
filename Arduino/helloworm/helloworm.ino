#include <SHT1x.h>
#include <SPI.h>         
#include <WiFi.h>
#include <HttpClient.h>
#include <Xively.h>

#define dataPin 5  // orange/blue
#define clockPin 6 // yellow/yellow
#define MQ4pin 4
#define MQ8pin 5
SHT1x sht1x(dataPin, clockPin);
int led = 9;  // status led pin

int status = WL_IDLE_STATUS;
int attempts = 0;
char ssid[] = "SSID HERE";  //  your network SSID (name)
char pass[] = "PASS HERE";       // your network password

// Your Xively key to let you upload data
char xivelyKey[] = "XIVELY KEY HERE";
// Define the strings for our datastream IDs
char tempID[] = "temperature";
char humID[] = "humidity";
char gas4ID[] = "gasMQ4";
char gas8ID[] = "gasMQ8";
XivelyDatastream datastreams[] = {
  XivelyDatastream(tempID, strlen(tempID), DATASTREAM_FLOAT),
  XivelyDatastream(humID, strlen(humID), DATASTREAM_FLOAT),
  XivelyDatastream(gas4ID, strlen(gas4ID), DATASTREAM_FLOAT),
  XivelyDatastream(gas8ID, strlen(gas8ID), DATASTREAM_FLOAT),
};
// Finally, wrap the datastreams into a feed
XivelyFeed feed(XIVELY-FEED-HERE, datastreams, 4);

WiFiClient client;
XivelyClient xivelyclient(client);

/**************************
*  SETUP
***************************/

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up");
  pinMode(led, OUTPUT);

  // attempt to connect to Wifi network:
  while(!Serial) ;
  while ( status != WL_CONNECTED) { 
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:    
    status = WiFi.begin(ssid, pass);
    if (status == WL_CONNECT_FAILED) {
      Serial.println("connection failed, retrying in 10 seconds");
    }
    attempts++;
    if (attempts>5) {
      Serial.println("max 5 attempts. Maybe already connected?");
      break;
    }
      // wait 10 seconds for connection:
    delay(10000);
  }
  Serial.println("Connected to wifi");
  Serial.flush();
  
}


/**************************
*  LOOP
***************************/

void loop(){

  // read temp and humidity
  float tempF = sht1x.readTemperatureF();
  float humidity = sht1x.readHumidity();

  Serial.print(tempF);
  Serial.print(",");
  Serial.print(humidity);
  
  // read gas sensors
  int valMQ4, valMQ8;
  valMQ4 = analogRead(MQ4pin);
  valMQ8 = analogRead(MQ8pin);
  Serial.print(',');
  Serial.print(valMQ4);//Print the value to serial port
  Serial.print(',');
  Serial.println(valMQ8);
  
  // send data to Xively
  datastreams[0].setFloat(tempF);
  datastreams[1].setFloat(humidity);
  datastreams[2].setFloat(valMQ4);
  datastreams[3].setFloat(valMQ8);

  Serial.println("Uploading data to Xively");
  int ret = xivelyclient.put(feed, xivelyKey);
  Serial.print("xivelyclient.put returned ");
  Serial.println(ret);
  
  // blink the LED so we know it's alive
  digitalWrite(led, LOW); 
  delay(120000);  // one datapoint every 2 minutes
  digitalWrite(led, HIGH);  
  
  Serial.flush();
}

