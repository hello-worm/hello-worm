//#include <Time.h>
#include <SD.h>
#include <SHT1x.h>
#include <SPI.h>         
#include <WiFi.h>
//#include <WiFiUdp.h>
#include <HttpClient.h>
#include <Xively.h>

#define dataPin 5
#define clockPin 6
#define MQ4pin 4
#define MQ8pin 5
SHT1x sht1x(dataPin, clockPin);
int led = 9;  // status led pin
File myFile;  // data file on the SD card

//String timestamp;  // timestamp for each data line
//#define TZ_ADJUST -7

int status = WL_IDLE_STATUS;
int attempts = 0;
char ssid[] = "fp143133c";  //  your network SSID (name)
char pass[] = "lowellhouse";       // your network password

/*
unsigned int localPort = 2390;      // local port to listen for UDP packets
IPAddress timeServer(69, 25, 96, 13); // time.nist.gov NTP server
const int NTP_PACKET_SIZE = 48; // NTP time stamp is in the first 48 bytes of the message
byte packetBuffer[ NTP_PACKET_SIZE]; //buffer to hold incoming and outgoing packets 
WiFiUDP Udp;
*/

// Your Xively key to let you upload data
char xivelyKey[] = "h4Etm594B8XO72JWQPIYmy60HjqRo6sekTwlI409o9sDDROf";
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
XivelyFeed feed(1317080174, datastreams, 2);

WiFiClient client;
XivelyClient xivelyclient(client);

/**************************
*  SETUP
***************************/

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up");
  pinMode(led, OUTPUT);
  SD.begin();

  // attempt to connect to Wifi network:
  while(!Serial) ;
  byte mac[6];
  WiFi.macAddress(mac);
  Serial.print("first hex digit of mac address: ");
  Serial.println(mac[5],HEX);
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
      break;
    }
      // wait 10 seconds for connection:
    delay(10000);
  }
  Serial.println("Connected to wifi");
  Serial.flush();
/*
  Serial.println("\nStarting connection to server...");
  Udp.begin(localPort);
  
  sendNTPpacket(timeServer); // send an NTP packet to a time server
    // wait to see if a reply is available
  delay(1000);  
  if ( Udp.parsePacket() ) { 
    Serial.println("packet received"); 
    // We've received a packet, read the data from it
    Udp.read(packetBuffer,NTP_PACKET_SIZE);  // read the packet into the buffer
    unsigned long highWord = word(packetBuffer[40], packetBuffer[41]);
    unsigned long lowWord = word(packetBuffer[42], packetBuffer[43]);  
    // combine the four bytes (two words) into a long integer
    // this is NTP time (seconds since Jan 1 1900):
    unsigned long secsSince1900 = highWord << 16 | lowWord;    

    // now convert NTP time into everyday time:
    Serial.print("Unix time = ");
    // Unix time starts on Jan 1 1970. In seconds, that's 2208988800:
    const unsigned long seventyYears = 2208988800UL;     
    // subtract seventy years:
    unsigned long epoch = secsSince1900 - seventyYears;  
    // print Unix time:
    Serial.println(epoch);         

    setTime(epoch+60*60*TZ_ADJUST);    
    Serial.print("Time set. Arduino Time: ");
    Serial.println(now());
  }
  */
  
}


/**************************
*  LOOP
***************************/

void loop(){
  // prep SD card file
  myFile = SD.open("test6.txt", FILE_WRITE);
  if (!myFile) {
    // if the file didn't open, print an error:
    Serial.println("error opening text file");
    SD.begin();
  }
  /*
  // get timestamp
  timestamp = String(now());
  if (myFile)
    myFile.print(timestamp+",");
  Serial.print(timestamp+",");
  //} 
  */
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
  delay(5000);  
  digitalWrite(led, HIGH);  
  
  Serial.flush();
}


/******************************
*  helpers
******************************/
/*
// send an NTP request to the time server at the given address 
unsigned long sendNTPpacket(IPAddress& address)
{
  //Serial.println("1");
  // set all bytes in the buffer to 0
  memset(packetBuffer, 0, NTP_PACKET_SIZE); 
  // Initialize values needed to form NTP request
  // (see URL above for details on the packets)
  //Serial.println("2");
  packetBuffer[0] = 0b11100011;   // LI, Version, Mode
  packetBuffer[1] = 0;     // Stratum, or type of clock
  packetBuffer[2] = 6;     // Polling Interval
  packetBuffer[3] = 0xEC;  // Peer Clock Precision
  // 8 bytes of zero for Root Delay & Root Dispersion
  packetBuffer[12]  = 49; 
  packetBuffer[13]  = 0x4E;
  packetBuffer[14]  = 49;
  packetBuffer[15]  = 52;
  
  //Serial.println("3");

  // all NTP fields have been given values, now
  // you can send a packet requesting a timestamp:         
  Udp.beginPacket(address, 123); //NTP requests are to port 123
  //Serial.println("4");
  Udp.write(packetBuffer,NTP_PACKET_SIZE);
  //Serial.println("5");
  Udp.endPacket(); 
  //Serial.println("6");
}
*/
