#include <SHT1x.h>
#include <SPI.h>         
#include <WiFi.h>
#include <HttpClient.h>
#include <Xively.h>
#include <dht.h>

#define dataPin 5  // orange/blue
#define clockPin 6 // yellow/yellow
#define dht22_pin 3 
#define MQ7pin 1
#define MQ8pin 5
SHT1x sht1x(dataPin, clockPin);
int led = 9;  // status led pin
dht DHT;
int status = WL_IDLE_STATUS;
int attempts = 0;
char ssid[] = "SSID HERE";  //  your network SSID (name)
char pass[] = "PASS HERE";       // your network password

// Your Xively key to let you upload data
char xivelyKey[] = "XIVELY KEY HERE";
// Define the strings for our datastream IDs
char tempID[] = "temperature";
char humID[] = "humidity";
char tempDHTID[] = "tempDHT22";
char humDHTID[] = "humDHT22";
char gas7ID[] = "gasMQ7";
char gas8ID[] = "gasMQ8";
XivelyDatastream datastreams[] = {
  XivelyDatastream(tempID, strlen(tempID), DATASTREAM_FLOAT),
  XivelyDatastream(humID, strlen(humID), DATASTREAM_FLOAT),
  XivelyDatastream(tempDHTID, strlen(tempDHTID), DATASTREAM_FLOAT),
  XivelyDatastream(humDHTID, strlen(humDHTID), DATASTREAM_FLOAT),
  XivelyDatastream(gas7ID, strlen(gas7ID), DATASTREAM_FLOAT),
  XivelyDatastream(gas8ID, strlen(gas8ID), DATASTREAM_FLOAT),
};
// Finally, wrap the datastreams into a feed
XivelyFeed feed(XIVELY-FEED-HERE, datastreams, 6);

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
  Serial.print("\t");
  Serial.print(humidity);
  delay(1000);
  
  float tIn, hIn;
  // read temp and humidity from DHT22
  int chk = DHT.read22(dht22_pin);
  if (chk==DHTLIB_OK) {
    tIn = DHT.temperature * 9/5 +32;
    hIn = DHT.humidity;     
  }
  else{
    tIn = -1;
    hIn = -1;
  }
  Serial.print("\t"+String(tIn)+"\t"+String(hIn));
  delay(1000);
  
  // read gas sensors
  int valMQ7, valMQ8;
  valMQ7 = analogRead(MQ7pin);
  Serial.print('\t');
  Serial.print(valMQ7);
  delay(1000);
  valMQ8 = analogRead(MQ8pin);
  Serial.print('\t');
  Serial.println(valMQ8);
  
  // send data to Xively
  datastreams[0].setFloat(tempF);
  datastreams[1].setFloat(humidity);
  datastreams[2].setFloat(tIn);
  datastreams[3].setFloat(hIn);
  datastreams[4].setFloat(valMQ7);
  datastreams[5].setFloat(valMQ8);

  Serial.println("Uploading data to Xively");
  int ret = xivelyclient.put(feed, xivelyKey);
  Serial.print("xivelyclient.put returned ");
  Serial.println(ret);
  
  // blink the LED so we know it's alive
  digitalWrite(led, LOW); 
  delay(60000);  // one datapoint every 1 minute
  //delay(5000);
  digitalWrite(led, HIGH);  
  
  Serial.flush();
}

