#include <SoftwareSerial.h>

SoftwareSerial NodeMcu_SoftSerial(D1, D2); //RX, TX 11, 10

//declare global variable
char c;
String dataIn;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);

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
      // Reset the variable
      c=0;
      dataIn="";
    }
}
