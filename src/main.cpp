#include <Arduino.h>
#include <LiquidCrystal_I2C.h> // Library for LCD
#include <SPI.h>
#include <MFRC522.h>
#include <WIFI.h>
#include "env.h"

#define SS_PIN  5  // ESP32 pin GPIO5 
#define RST_PIN 27 // ESP32 pin GPIO27 


// either create an env file with these in 
// or uncomment and use it 
// const char* ssid = "your_ssid";
// const char* password = "your_password";

const uint port = 2332;
const char* ip = "10.0.0.43";

char buffer[66] = {};  

WiFiClient localClient;
MFRC522 rfid(SS_PIN, RST_PIN);
LiquidCrystal_I2C lcd(0x27, 20, 4); // I2C address 0x27, 20 column and 4 rows

typedef struct Part_s {
  char name[14];
  char spec[20];
  char footprint[16];
  char part_number[16];
}Part_t;

void print_part(Part_t * part){
  lcd.clear();
  lcd.setCursor(0, 0);
  Serial.printf("part: %.14s\n", part->name);
  lcd.printf("part: %.14s", part->name);
  lcd.setCursor(0, 1);
  Serial.printf("%.20s\n", part->spec);
  lcd.printf("%.20s", part->spec);
  lcd.setCursor(0, 2);
  Serial.printf("FP: %.16s\n", part->footprint);
  lcd.printf("FP: %.16s", part->footprint);
  lcd.setCursor(0, 3);
  Serial.printf("PN: %.16s\n", part->part_number);
  lcd.printf("PN: %.16s", part->part_number);
}

void setup() {
  Serial.begin(9600);
	Wire.begin(); // join I2C bus as the master
  SPI.begin(); // init SPI bus
  rfid.PCD_Init(); // init MFRC522
  Serial.println("started");
  lcd.init(); //initialize the lcd
  lcd.clear();
  lcd.backlight(); //open the backlight 
  lcd.setCursor(0, 0);
  // print_part();

  lcd.print("Connect Wlan");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    lcd.setCursor(0, 1);
    delay(500);
    lcd.print(".");
  }
  lcd.setCursor(0, 1);
  lcd.print(WiFi.localIP());
}

void loop() {
  if (rfid.PICC_IsNewCardPresent()) { // new tag is available
    if (rfid.PICC_ReadCardSerial()) { // NUID has been readed
      MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
      // print NUID in Serial Monitor in the hex format
      String UID;
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("UID:");
      for (int i = 0; i < rfid.uid.size; i++) {
        lcd.print(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
        lcd.print(rfid.uid.uidByte[i], HEX);
      }
      rfid.PICC_HaltA(); // halt PICC
      rfid.PCD_StopCrypto1(); // stop encryption on PCD
      if (localClient.connect(ip, port)) {                 // Establish a connection
        if (localClient.connected()) {
            localClient.write(rfid.uid.uidByte, rfid.uid.size);
            delay(400);
            Serial.printf("waiting have : %d bytes", localClient.available());
            while (localClient.available() != sizeof(buffer)){
              Serial.printf("waiting have : %d bytes", localClient.available());
              delay(100);
            }
            
            Part_t p;
            for (int i = 0; i < sizeof(buffer); i++){
              buffer[i] = localClient.read();
            }
            // Serial.printf("%s", buffer);
            memcpy(&p, buffer, 66);
            print_part(&p);
        }
      } else {
        lcd.setCursor(0, 1);
        lcd.print("no connection");
      }
      delay(200);
    }
  }
}

