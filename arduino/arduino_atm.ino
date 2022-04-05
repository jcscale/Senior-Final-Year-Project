#include <SoftwareSerial.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;

char keys [ROWS] [COLS] = {
  {'1', '2', '3', '+'},
  {'4', '5', '6', '-'},
  {'7', '8', '9', '*'},
  {'C', '0', '=', '/'}
};
byte rowPins[ROWS] = {2, 3, 4, 5};
byte colPins[COLS] = {6, 7, 8, 9};

Keypad myKeypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

boolean presentValue = false;
boolean next = false;
boolean final = false;
String num1, num2;
int answer = 0;
char op;

SoftwareSerial Arduino_SoftSerial(10, 11); //RX, TX

//Declare Global Variable
char c;
String dataIn;


String mobile, pin;



void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);

  //Open serial communication (arduino-NodeMcu)
  Arduino_SoftSerial.begin(9600);

  lcd.begin();
  lcd.backlight();
  lcd.print("Reverse Vending");
  lcd.setCursor(0,1);
  lcd.print("Machine");
  delay(2000);
  lcd.clear();

//  lcd.setCursor(0,0);
//  lcd.print("Mobile Number:");
//  lcd.setCursor(0,1);
//  lcd.print("63");
//  lcd.clear();
    //lcd.setCursor(0,0);
    lcd.print("Mobile Number");
    lcd.setCursor(0,1);
    lcd.print("+63");
  }

  void loop() {
  
  char key = myKeypad.getKey();

  if (key != NO_KEY && (key == '1' || key == '2' || key == '3' || key == '4' || key == '5' || key == '6' || key == '7' || key == '8' || key == '9' || key == '0'))
  {
    if (presentValue != true)
    {
      num1 = num1 + key;
      //int numLength = num1.length();
      lcd.setCursor(3,1); 
      lcd.print(num1);
      Serial.println(num1);
    }
    else
    {
      num2 = num2 + key;
      //int numLength = num2.length();
      //int numLength1 = num1.length();
//      lcd.setCursor(1 + numLength1, 0);
      lcd.setCursor(0,1);
      lcd.print(num2);
      Serial.println(num2);
      final = true;
    }
  }

  else if (presentValue == false && key != NO_KEY && (key == '/' || key == '*' || key == '-' || key == '+'))
  {
    if (presentValue == false)
    {
      lcd.clear();
      lcd.print("Pin Number");
//      int numLength = num1.length();
      presentValue = true;
      op = key;
//      lcd.setCursor(0 + numLength, 0);
      lcd.setCursor(0,1);
      lcd.print(op);
    }
  }

  else if (final == true && key != NO_KEY && key == '=') {
  
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("63"+num1);
  Serial.println("63"+num1);
  lcd.setCursor(0,1);
  lcd.print(num2);
  Serial.println(num2);
  Arduino_SoftSerial.print("63"+num1+"-"+num2+"\n"); // \n - end data character
  
  delay(500);

  while(Arduino_SoftSerial.available()>0)
    {
      c = Arduino_SoftSerial.read();
      if(c == '\n'){break;}
      else{dataIn+=c;}
    }

    if(c=='\n')
    {
      //Show incoming data to serial monitor
      Serial.println(dataIn);

      //reset the variable
      c = 0;
      dataIn="";
    }
    
  }
  else if (key != NO_KEY && key == 'C') {
    lcd.clear();
    presentValue = false;
    final = false;
    num1 = "";
    num2 = "";
    answer = 0;
    op = ' ';
  }
}
  
  

//void loop() {
//  // put your main code here, to run repeatedly:
//
//    Arduino_SoftSerial.print("hello \n"); // \n - end data character
//    delay(500);
//
//    while(Arduino_SoftSerial.available()>0)
//    {
//      c = Arduino_SoftSerial.read();
//      if(c == '\n'){break;}
//      else{dataIn+=c;}
//    }
//
//    if(c=='\n')
//    {
//      //Show incoming data to serial monitor
//      Serial.println(dataIn);
//
//      //reset the variable
//      c = 0;
//      dataIn="";
//    }
//}
