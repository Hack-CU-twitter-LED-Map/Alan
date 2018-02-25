//LED Matrix Driver for Arduino 

#define A A0
#define B A1
#define C A2
#define D A3
#define R1 2
#define R2 3
#define B1 4
#define B2 5
#define G1 6
#define G2 7
#define LAT 8
#define OE 9
#define CLK 10

//PORTC macros
#define ADR PORTC
#define Ashift 0
#define Bshift 1
#define Cshift 2
#define Dshift 3

//PORTD macros
#define RGB PORTD
#define R1shift 2
#define R2shift 3
#define B1shift 4
#define B2shift 5
#define G1shift 6
#define G2shift 7

//PORTB macros
#define CTL PORTB
#define LATshift 0
#define OEshift 1
#define CLKshift 2

//clear, set, and toggle pins
#define CLR(x,y) (x&=(~(1<<y)))
#define SET(x,y) (x|=(1<<y))
#define TOGGLE(x,y) (x=(x^(1<<y)))

//global variables
volatile int count = 0;
volatile int address = 0;
volatile String colordata;
volatile int inputcolor;

//determine color of top half of LED matrix
void colorcasetophalf(int citycolor){
  switch(citycolor){
    case 48: 
      SET(RGB,R1shift);
      break;
    case 49:
      SET(RGB,R1shift);
      SET(RGB,B1shift);
      break;
    case 50:
      SET(RGB,R1shift);
      SET(RGB,B1shift);
      SET(RGB,G1shift);
      break;
    case 51:
      SET(RGB,R1shift);
      SET(RGB,G1shift);
      break;
    case 52:
      SET(RGB,G1shift);
      break;
  }
}

//determine color of bottom half of LED matrix
void colorcasebothalf(int citycolor){
  switch(citycolor){
    case 48: 
      SET(RGB,R2shift);
      break;
    case 49:
      SET(RGB,R2shift);
      SET(RGB,B2shift);
      break;
    case 50:
      SET(RGB,R2shift);
      SET(RGB,B2shift);
      SET(RGB,G2shift);
      break;
    case 51:
      SET(RGB,R2shift);
      SET(RGB,G2shift);
      break;
    case 52:
      SET(RGB,G2shift);
      break;
  }
}

//function to set the value of a pin
void setAddress(int adrs,int shift, int power){
  if((adrs & power)== 0){
    CLR(ADR,shift);
  }
  else{
    SET(ADR,shift);
  }
}


void setup() {
  // put your setup code here, to run once:
  //configure serial terminal
  Serial.begin(9600);

  //configure pins as output
  pinMode(A,OUTPUT);
  pinMode(B,OUTPUT);
  pinMode(C,OUTPUT);
  pinMode(D,OUTPUT);
  pinMode(R1,OUTPUT);
  pinMode(R2,OUTPUT);
  pinMode(B1,OUTPUT);
  pinMode(B2,OUTPUT);
  pinMode(G1,OUTPUT);
  pinMode(G2,OUTPUT);
  pinMode(LAT,OUTPUT);
  pinMode(OE,OUTPUT);
  pinMode(CLK,OUTPUT);

  //configure pin outputs
  CLR(ADR,Ashift);
  CLR(ADR,Bshift);
  CLR(ADR,Cshift);
  CLR(ADR,Dshift);
  CLR(RGB,R1shift);
  CLR(RGB,R2shift);
  CLR(RGB,B1shift);
  CLR(RGB,B2shift);
  CLR(RGB,G1shift);
  CLR(RGB,G2shift);
  CLR(CTL,LATshift);
  SET(CTL,OEshift);
  CLR(CTL,CLKshift);

  //configure timer
  noInterrupts();
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;

  OCR1A = 1;
  TCCR1B |= (1 << CS10);
  TCCR1B |= (1 << WGM12);
  interrupts();
}

//timer ISR
ISR(TIMER1_COMPA_vect){
  if(count == 0){
    CLR(CTL,LATshift);
    CLR(CTL,OEshift);
  }

  //Denver
  if(address == 14 && count == 34){
    colorcasetophalf(colordata[0]);
  }
  //Colorado Springs
  else if(address == 3 && count == 34){
    colorcasebothalf(colordata[1]);
   }
   //Arvada
  else if(address == 13 && count == 32){
    colorcasetophalf(colordata[7]);
  }
  //Fort Collins
  else if(address == 2 && count == 32){
    colorcasetophalf(colordata[3]);

  }
  //Lakewood
  else if(address == 14 && count == 32){
    colorcasetophalf(colordata[4]);
  }
  //Thornton
  else if(address == 11 && count == 34){
    colorcasetophalf(colordata[5]);
  }
  //Centennial
  else if(address == 15 && count == 36){
    colorcasebothalf(colordata[9]);
  }
  //Pueblo
  else if(address == 9 && count == 38){
    colorcasebothalf(colordata[6]);
  }
  //Westminster
  else if(address == 11 && count == 32){
    colorcasetophalf(colordata[8]);
  }
  //Boulder
  else if(address == 10 && count == 30){
    colorcasetophalf(colordata[10]);
  }
  //Aurora
  else if(address == 14 && count == 36){
    colorcasetophalf(colordata[2]);
  } 
  
  else{
    CLR(RGB,R1shift);
    CLR(RGB,R2shift);
    CLR(RGB,B1shift);
    CLR(RGB,B2shift);
    CLR(RGB,G1shift);
    CLR(RGB,G2shift);
  }
  TOGGLE(CTL,CLKshift);
  count++;
  if(count == 63){
    count = 0;
    SET(CTL,LATshift);
    SET(CTL,OEshift);
    TOGGLE(CTL,CLKshift);
    if(address == 15){
      address = 0;
    }
    else{
      address = address +1;
    }
    setAddress(address,Ashift,1);
    setAddress(address,Bshift,2);
    setAddress(address,Cshift,4);
    setAddress(address,Dshift,8);
    pwmcount = pwmcount +1;
  }
}

//receives data serially
void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() >0 ){
    colordata = Serial.readString();
    TIMSK1 |= (1 << OCIE1A);
  }

}
