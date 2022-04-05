#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

const char* ssid = "Anonymous";
const char* password = "winston2728";

SoftwareSerial NodeMcu_SoftSerial(D1, D2); //RX, TX 11, 10

//declare global variable
char c;
String dataIn;
String mobile, pin;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);

  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
 
    delay(1000);
    Serial.print("Connecting..");
 
  }

  //Open serial communication (arduino-NodeMcu)
  NodeMcu_SoftSerial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

    while(NodeMcu_SoftSerial.available()>0)
    {
      c = NodeMcu_SoftSerial.read();
      if(c=='\n'){break;}
      else{dataIn+=c;}

    }

    if(c=='\n')
    {
      //Show data in to Serial Monitor
      Serial.println(dataIn);
      NodeMcu_SoftSerial.print("Received from arduino \n");
      NodeMcu_SoftSerial.print(dataIn.substring(0,12));
      NodeMcu_SoftSerial.print(dataIn.substring(13,18));
      mobile = dataIn.substring(0,12);
      pin = dataIn.substring(13,18);
      NodeMcu_SoftSerial.print("http://rvm123.pythonanywhere.com/api/accounts/"+mobile+"-"+pin);

      WiFiClient client;
      if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
      Serial.println("WiFi Connected");
      HTTPClient http;  //Declare an object of class HTTPClient
   
      http.begin(client, "http://rvm123.pythonanywhere.com/api/accounts/"+mobile+"-"+pin);  //Specify request destination
      int httpCode = http.GET();                                  //Send the request
   
      if (httpCode > 0) { //Check the returning code
   
        String payload = http.getString();   //Get the request response payload
        Serial.println(payload); 
        NodeMcu_SoftSerial.print(payload +" \n");//Print the response payload
   
      }
   
      http.end();   //Close connection
   
    }
      
      // Reset the variable
      c=0;
      dataIn="";
    }
}