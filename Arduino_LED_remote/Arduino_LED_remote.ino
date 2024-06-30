#include <IRremote.h>

#define PIN_SEND 3

IRsend irsend;
String data;

void setup() {
  // put your setup code here, to run once:
  //pinMode(13, OUTPUT);
  Serial.begin(9600); // Initialize serial interface
  //digitalWrite(LED_BUILTIN, HIGH);
  pinMode(3, OUTPUT);
  IrSender.begin(PIN_SEND); // Initializes IR sender
  Serial.println("Ready to transmit IR signal");
}

void loop() {
  //Serial.println("Running");
  while(Serial.available())
  {
    data = Serial.readString();
    data.trim();
  }
  //Serial.println(data);
  if(data == "Red")
  {
    IrSender.sendNEC(0x0, 0x15, 1);
    Serial.println("Red");
  }
  else if(data == "Green")
  {
    IrSender.sendNEC(0x0, 0x16, 1);
    Serial.println("Green");
  }
  else if(data == "White")
  {
    IrSender.sendNEC(0x0, 0x14, 1);
    Serial.println("White");
  }
  else if(data == "DarkBlue")
  {
    IrSender.sendNEC(0x0, 0x17, 1);
    Serial.println("Dark Blue");
  }
  else if(data == "Yellow")
  {
    IrSender.sendNEC(0x0, 0x10, 1);
    Serial.println("Yellow");
  }
  else if(data == "Orange")
  {
    IrSender.sendNEC(0x0, 0x11, 1);
    Serial.println("Orange");
  }
  else if(data == "Purple")
  {
    IrSender.sendNEC(0x0, 0x12, 1);
    Serial.println("Purple");
  }
  else if(data == "LightBlue")
  {
    IrSender.sendNEC(0x0, 0x13, 1);
    Serial.println("Light Blue");
  }
  else if(data == "Mode")
  {
    IrSender.sendNEC(0x0, 0x4D, 1);
    Serial.println("Mode");
  }
  else if(data == "Sound2")
  {
    IrSender.sendNEC(0x0, 0x9, 1);
    Serial.println("Sound2");
  }
  else if(data == "Sound3")
  {
    IrSender.sendNEC(0x0, 0xA, 1);
    Serial.println("Sound3");
  }

  data = "A";
}