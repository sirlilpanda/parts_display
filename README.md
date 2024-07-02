# part finder

this is a project that allow through a use of an NFC tag on each of your parts to retrieve basic data from it

## what you will need

- esp32
- [4x20 LCD display](https://www.amazon.com/dp/B0BXKKBZND?&linkCode=sl1&tag=zlufy-20&linkId=2e7e605d71d53c0fe820cbd5463520f6&language=en_US&ref_=as_li_ss_tl)
    - LCD -> ESP32
    - GND -> GND
    - VCC -> VIN
    - SDA -> D21
    - SCL -> D22
- [RC522 RFID card reader](https://www.amazon.com/dp/B0B33Y87ZG?th=1&linkCode=sl1&tag=zlufy-20&linkId=c02e1985458df4bf21bf005217883069&language=en_US&ref_=as_li_ss_tl)  
    - READER -> ESP32
    - 3.3v -> 3.3v
    - RST -> D26
    - GND -> GND
    - SDA -> D5
    - SCK -> D18
    - MISO -> D19
    - MOSI -> D23
- and your computer

## usage

- first you will want to run `main.py` with in the server dir
- next you will want to complie and upload `main.cpp` to an esp32 with LCD and rfid tag reader
    - you will needed to add you ssid and password to main.cpp, either in `/include/env.h` or uncomment lines 17 and 18, adding you ssid and password in there
    - you will also need to make sure the `ip` on line 18 is set to the local ip of your computer
- you will first see on the LCD text saying `Connect Wlan` and a few seconds later the local ip of the esp32 should appear if not
  - check you entered in you ssid and password correctly
- after you have connected you can start scaning your parts
  - when you scan the LCD will show the UID of the NFC tag, and then a few seconds later will either
    - load the part in this will display
      - the name of the part like `resistor`, `capacitor`, etc..
      - the specs of the part such as the ohms or crystal freq
      - the footprint of the part
      - the part number for either digikey or what ever parts supplier you use
    - or it will show no connection, this could be caused by 2 things either
      - you have not started main.py
      - or your computers ip within the code is not correct
- on the GUI side when a part is scaned 2 things can happen either:
  - the part auto fills in the input field with its specs
    - if you want to change these values then you can just change them and click update_part this will update the entry within the database
  - the title changes to part not in database and the UID of the tag appears in the UID field
    - if this occurs the part scan is as it says not in the database then input the approprate infomation into the input boxes and click update_part, this will add the part in to the data and if you rescan it the new data should appear on the LCD

# future improvements
- adding auto datasheet diplay
    - when you scan a known part it will make a request and pull the datasheet down from the datasheet link and display it along side the part adder
- adding more documention
  - ive try to make the code modular so if you dont want to use the wifi server you could write your own server, all you have is an in and out queue as can be seen in `main.py` just send the UID through the `out_queue` and the `in_queue` will receive the current part as laid out in `part.py`
  