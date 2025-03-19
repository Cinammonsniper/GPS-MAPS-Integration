#include <SoftwareSerial.h>

SoftwareSerial gps(4, 3);
String nmeaSentence;


String latitude, longitude, altitude, fixstatus, precision, geoidseperation;

void parsedata(String nmea)
{
  String current_char, field;
  String fields[15];
  int i, field_count = 0;
  i+=1;
  while (current_char != "*")
  {
    current_char = nmea.substring(i, i-1);;
    if (current_char == ",")
    {
      fields[field_count] = field;
      field = "";
      field_count += 1;
    }else
    {
      field += current_char;
    }
    i+=1;
  }
  Serial.println();
  if (field_count > 10) {
        latitude = fields[2] + " " + fields[3];  
        longitude = fields[4] + " " + fields[5];
        fixstatus = fields[6];     
        precision = fields[8];
        altitude = fields[9];
        geoidseperation = fields[11];
    }
  
}


void setup(){
  Serial.begin(9600);
  gps.begin(9600);
}


void loop() {
    while (gps.available()) {
        char c = gps.read();
//        Serial.println(c);
        
        if (c == '\n') {  
            
            if (nmeaSentence.startsWith("$GPGGA")) 
            {
                parsedata(nmeaSentence);
                Serial.print("Latitude: "); Serial.println(latitude);
                Serial.print("Longitude: "); Serial.println(longitude);
                Serial.print("Fix Status: "); Serial.println(fixstatus);
                Serial.print("Altitude: "); Serial.println(altitude);
                Serial.print("Precision: "); Serial.println(precision);
                Serial.print("Geoid Seperation: "); Serial.println(geoidseperation);
                Serial.print("Actual Height: "); Serial.println(altitude.toInt() - geoidseperation.toInt());
                Serial.print("#");

            }
            nmeaSentence = "";
        } else {
            nmeaSentence += c;
        }
    }
}
