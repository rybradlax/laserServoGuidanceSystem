//Written By Nikodem Bartnik - nikodembartnik.pl
#include <Wire.h>
#include <Servo.h>
#include <Adafruit_NeoPixel.h>

Servo myservo;

int theta = 90;
/*int pin = 6;
int pixels = 24;
Adafruit_NeoPixel ring = Adafruit_NeoPixel(pixels, pin, NEO_GRB + NEO_KHZ800);
uint32_t green = ring.Color(0, 255, 0);
short const MED_BRIGHTNESS = 100;
short brightness = MED_BRIGHTNESS;*/

void setup() {
Serial.begin(115200);
Serial.setTimeout(0.2);
pinMode(9,OUTPUT);
myservo.attach(9);
myservo.write(90);
/*for(int x=0; x<pixels; x++) {
    ring.setPixelColor(x, green);
  }
  ring.show();
  ring.setBrightness(brightness);
*/



}

void loop() {

  while(true){
      String f;
  String b = "";
  int x;
    /*for (int pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(100);                       // waits 15ms for the servo to reach the position
  }*/
    if(Serial.available()){
      while(Serial.available()>0){
        f=Serial.readString();
        //Serial.println(f);
        //temp1 = f;
        }
        if(f.equals("m")){
          Serial.print(f);
          theta = theta + 10;
          if(theta>180 || theta<0){
            theta=90;
            }
          myservo.write(theta);
          } else if (f.equals("n")){
            theta = theta + 5;
          if(theta>180 || theta<0){
            theta=90;
            }
          myservo.write(theta);
            }else if (f=="b"){
            theta = theta + 3;
          if(theta>180 || theta<0){
            theta=90;
            }
          myservo.write(theta);
            } else if (f=="v"){
            theta = theta + 1;
          if(theta>180 || theta<0){
            theta=90;
            }
          myservo.write(theta);
            } else if (f.equals("c")){
            theta = theta - 10;
          if(theta>180 || theta<0){
            theta=90;
            }
          myservo.write(theta);
            } else if (f=="x"){
            theta = theta - 5;
          if(theta>180 || theta<0){
            theta=90;
            }
          myservo.write(theta);
            } else if (f=="z"){
            theta = theta - 3;
          if(theta>180 || theta<0){
            theta=90;
            }
          myservo.write(theta);
            } else if (f="l"){
            theta = theta - 1;
          if(theta>180 || theta<0){
            theta=90;
            }
          myservo.write(theta);
            }
        //Serial.println(x);
        myservo.write(theta);
        //Serial.println(b);
      //temp = f;
     // f=Serial.read()-'0';
    //  Serial.println(f);
    //  Serial.println(f);
      //f = temp + f;     
    }
    
   // if(temp!=0){
     // myservo.write(temp);
      //}
   
 /* myservo.write(0);
  delay(200);
  myservo.write(30);
  delay(200);
  myservo.write(60);
  delay(200);
  myservo.write(90);
  delay(200);
  myservo.write(120);
  delay(200);
  myservo.write(150);
  delay(200);
  myservo.write(180);
  delay(200);  
  */
  }
  /*    if(f != 0){
        temp = f;
        f=Serial.parseInt();
        myservo.write(f);
        f = temp + f;
        } else {
        f=Serial.parseInt();
        if(f!=0){
        myservo.write(f);
        }
         }
      
      delay(1000);*/
  }
