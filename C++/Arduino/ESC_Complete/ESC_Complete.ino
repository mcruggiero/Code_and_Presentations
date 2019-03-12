//Here is the code I worked out for a beautiful puzzle box based on the Arduino, a Tim1638, and
//DHT22 Humitity Sensor, photoresistor, and 

#include <DHT.h>

const uint8_t strobe = 8;
const uint8_t clock = 9;
const uint8_t data = 10;
const uint8_t buzzer = 11;
const uint8_t DHTPIN = 7;
const uint8_t LED0 = 6;
const uint8_t LED1 = 5;
const uint8_t LED2 = 4;
const uint8_t LED3 = 3;
const uint8_t PowerPhoto = 28;
const uint8_t analogPinPhoto= 0;
const uint8_t analogPinResis= 1;
const uint8_t ground= 22;
/*
 top
 vcc
 gnd
 stb 8
 clk 9 
 dio 10
 */



//Variables for Humidity and Temp
DHT dht(DHTPIN, DHT22);
long hum;
long temper;

//Variables for TM1638
const uint8_t brightness = 0x8f; //brightness levels 0x88-0x8f

long Timer = (long)45*60*100; //Start time
long counter;

uint8_t scrollTextBreak = 0;
uint8_t delaySpeed = 200;
long lastButtonTime = 0;
uint8_t currentBinaryValue = 0;

uint8_t buttonStates[8] = {0,0,0,0,0,0,0,0};
uint8_t puzzleStates[4] = {0,0,0,0};

uint8_t modeState;
uint8_t primesArePoisonState;
uint8_t modeCount;

/* Digits and LEDs
The bits are displayed by mapping bellow
 -- 0 --
|       |
5       1
 -- 6 --
4       2
|       |
 -- 3 --  .7
*/

//display values for the eight 7-digit displays
const uint8_t displays[] = {
  0xc0, //display #0
  0xc2, //display #1
  0xc4, //display #2
  0xc6, //display #3
  0xc8, //display #4
  0xca, //display #5
  0xcc, //display #6
  0xce}; //display #7

//Complete Set from 7 digit display
const uint8_t letters[] = {
  0b01110111, /*0 A */
  0b01111100, /*1 B */
  0b00111001, /*2 C */
  0b01011110, /*3 D */
  0b01111001, /*4 E */
  0b01110001, /*5 F */
  0b00111101, /*6 G */
  0b01110110, /*7 H */
  0b00110000, /*8 I */
  0b00011110, /*9 J */
  0b01110101, /*10 K */
  0b00111000, /*11 L */
  0b00010101, /*12 M */
  0b00110111, /*13 N */
  0b00111111, /*14 O */
  0b01110011, /*15 P */ 
  0b01101011, /*16 Q */
  0b00110011, /*17 R */
  0b01101101, /*18 S */
  0b01111000, /*19 T */
  0b00111110, /*20 U */
  0b00111110, /*21 V */
  0b00101010, /*22 W */
  0b01110110, /*23 X */
  0b01101110, /*24 Y */
  0b01011011, /*25 Z */
  0b01000000, /*26 - */
  0b00000000, /*27 space*/
  0b00111111, /*28 0*/
  0b00000110, /*29 1*/
  0b01011011, /*30 2*/
  0b01001111, /*31 3*/
  0b01100110, /*32 4*/
  0b01101101, /*33 5*/
  0b01111101, /*34 6*/
  0b00000111, /*35 7*/
  0b01111111, /*36 8*/
  0b01101111, /*37 9*/
  0b10000110,};/*38 1.*/

//A simple Digit set
const uint8_t digits[] = {
  0b00111111, // 0
  0b00000110, // 1
  0b01011011, // 2
  0b01001111, // 3
  0b01100110, // 4
  0b01101101, // 5
  0b01111101, // 6
  0b00000111, // 7
  0b01111111, // 8
  0b01101111}; // 9

//scrollText values
//scroll text values

const int binaryPrompt [] =    {27, 27, 27, 27, 27, 27, 27, 27,
                          0,   3,  3,  27, 32, 27, 1,  8,
                          13,  0,  17, 24, 27, 13, 20, 12,
                          1,   4,  17, 18, 27, 19, 14, 27,
                          2,   0,  11, 8,  1,  17, 0,  19,
                          4,
                          27,  27, 27, 27, 27, 27, 27, 27};
uint8_t length_of_binaryPrompt = sizeof(binaryPrompt)/sizeof(int);

const int primesArePoison[] =  {27, 27, 27, 27, 27, 27, 27, 27,
                          15, 17, 8,  12, 4,  18, 27, 0,
                          17, 4,  27, 15, 14, 8,  18, 14,
                          13, 27, 22, 7,  4,  13, 27, 19,
                          7,  4,  27, 2, 11,  14, 2,  10,
                          27, 17, 20, 13, 18,
                          27, 27, 27, 27, 27, 27, 27, 27};
uint8_t length_of_primesArePoison = sizeof(primesArePoison)/sizeof(int);

const int add[] =        {27, 27, 27, 27, 27, 27, 27, 27,
                          0,  3,  3,  27, 19, 7,  4,  27,         //add the
                          5,  14, 11, 11, 14, 22, 8,  13,         //followin
                          6,  27, 30, 27, 13, 20, 12, 1,  4,  17, //g 2 number
                          18, 27, 27, 27, 27, 27, 27, 27,         //s
                          27};
uint8_t length_of_add = sizeof(add)/sizeof(int);

const int pressOne[] =   {27, 27, 27, 27, 27, 27, 27, 27,
                          15, 17, 4,  18, 18, 27, 1,  20, //press bu
                          19, 19, 14, 13, 18, 27, 19, 14, //ttons to
                          27, 0,  2,  19, 8,  21, 0,  19, //activat
                          4,  27, 11, 8,  6,  7,  19, 18, //e
                          27, 29, 27, 19, 14, 27, 8,  13,
                          15, 20, 19, 27, 30, 27, 19, 14,
                          27, 16, 20, 8,  19,
                          27, 27, 27, 27,
                          27, 27, 27, 27};
uint8_t length_of_pressOne = sizeof(pressOne)/sizeof(int);

const int to[] =         {27, 27, 27, 27, 27, 27, 27, 27,
                          0,  3,  3,  27, 19, 14, 27, 27, 27, 27, 27, 27, // add to
                          27, 27, 27, 27, 27, 27, 27, 27};
uint8_t length_of_to = sizeof(to)/sizeof(int);

const int numbersAgain[] ={27, 27, 27, 27, 27, 27, 27, 27,
                          19, 7,  4,  27, 30, 27, 13, 20,
                          12, 1,  4,  17, 18, 27, 14, 13,
                          4,  27, 12, 14, 17, 4,  27, 19,
                          8,  12, 4,  27, 27, 27, 27, 27,
                          27, 27, 27};
uint8_t length_of_numbersAgain = sizeof(numbersAgain)/sizeof(int);

const int no[] =         {27, 27, 27, 27, 27, 27, 27, 27,
                          27, 27, 27, 27, 27, 27, 27, 27,
                          13, 14, 27, 27, 27, 27, 27, 27,
                          27, 27, 27, 27, 27, 27, 27, 27,
                          13, 14, 27, 27, 27, 27, 27, 27,
                          27, 27, 27, 27, 27, 27, 27, 27,
                          15, 14, 22, 4,  17, 27, 11, 14,
                          18, 18, 26, 0,  19, 19, 4,
                          12, 15, 19, 8,  13, 6,  27, 17,
                          4,  18, 19, 0,  17, 19,
                          26, 28, 26, 28, 26, 28, 26, 28,
                          26, 28, 26, 28, 26, 28, 26, 28};
uint8_t length_of_no = sizeof(no)/sizeof(int);

const int correct[] =    {27, 27, 27, 27, 27, 27, 27, 27,
                          2,  14, 17, 17, 4, 2, 19, 27,
                          27, 27, 27, 27, 27, 27, 27};
uint8_t length_of_correct = sizeof(correct)/sizeof(int);

const int await_entry[] = {27, 27, 27, 27, 27, 27, 27, 27,
                          0,  22, 0,  8,  19, 8,  13, 6, 
                          27, 27, 27, 27, 27, 27, 27, 27,
                          29, 27, 19, 14, 27, 4,  13,
                          19, 4,  17, 27, 30, 27, 19, 14,
                          27, 16, 20, 8,  19, 27, 14, 19,
                          7,  4,  17, 18, 27, 19, 14, 27,
                          18, 
                          4,  19,
                          27, 27, 27, 27, 27, 27, 27};                          
uint8_t length_of_await_entry = sizeof(await_entry)/sizeof(int);

const int quiz10[] =    {27, 27, 27, 27, 27, 27, 27, 27,
                          1,  8,  13, 0,  17, 24, 27, 18,
                          24, 18, 19, 4,  12, 18, 27, 5,
                          0,  8,  11, 20, 17, 4,  27, 15,
                          17, 4,  18, 18, 27, 29, 27, 19,
                          14, 27, 17, 4,  18, 4,  19, 27,
                          30, 27, 19, 14, 27, 16, 20, 8,
                          19,
                          27, 27, 27, 27, 27, 27, 27, 27};
const uint8_t length_of_quiz10 = sizeof(quiz10)/sizeof(int);

const int quiz40[] =      {27, 27, 27, 27, 27, 27, 27, 27,
                           7,  20, 12, 8,  3,  27, 18, 4,
                           13, 18, 14, 17, 27, 5,  0,  8,
                           11, 27, 17, 0, 8, 18, 4, 27, 19,
                           14, 27, 37, 28, 27, 15, 
                           17, 4,  18, 18, 27, 29, 27, 19,
                           14, 27, 17, 4,  18, 4,  19, 27,
                           30, 27, 19, 14, 27, 16, 20, 8,
                           19,
                           27, 27, 27, 27, 27, 27, 27, 27};
const uint8_t length_of_quiz40 = sizeof(quiz40)/sizeof(int);

const int quiz60[] =      {27, 27, 27, 27, 27, 27, 27, 27,
                           15, 7,  14, 19, 14, 17, 4, 18,
                           19, 14, 17, 27, 18, 4, 13, 18, 14, 17,
                           27, 5,  0,  8, 11,
                           27, 18, 4, 19, 27, 
                           1, 4, 19, 22, 4, 4, 13, 27,
                           30, 38, 29, 27, 0, 13, 3, 27,
                           32, 38, 29, 27, 15,
                           17, 4,  18, 18, 27,
                           29, 27, 19,
                           14, 27, 17, 4,  18, 4,  19, 27,
                           30, 27, 19, 14, 27, 16, 20, 8,
                           19, 27, 
                           27, 27, 27, 27, 27, 27, 27, 27};
const uint8_t length_of_quiz60 = sizeof(quiz60)/sizeof(int);

const int quiz80[] =      {27, 27, 27, 27, 27, 27, 27, 27,
                           17, 4, 18, 8, 18, 19, 14, 17, //resistor
                           27, 4, 11, 4, 12, 4, 13, 19, //element
                           27, 12, 8, 18, 18, 8, 13, 6, //missing
                           27, 18, 4, 19, //set
                           27, 1, 4, 19, 22, 4, 4, 13, 27,
                           27, 29, 28, 28, 28, 28, //10000 Hard Code This
                           27, 0, 13, 3,
                           27, 29, 28, 33, 28, 28,
                           27, 14, 7, 12, 18,
                           27, 29, 27, 19,
                           14, 27, 17, 4,  18, 4,  19, 27,
                           30, 27, 19, 14, 27, 16, 20, 8,
                           19, 27, 
                           27, 27, 27, 27, 27, 27, 27, 27};
const uint8_t length_of_quiz80 = sizeof(quiz80)/sizeof(int);

const int solution[] =     {27, 27, 27, 27, 27, 27, 27, 27,
                           11, 27, 8, 27, 21, 27, 4, 27, 
                           27, 27, 27, 27, 27, 27, 27, 27};
const uint8_t length_of_solution = sizeof(solution)/sizeof(int);



//TIM1638 LED Commands
void sendCommand(uint8_t value){
  digitalWrite(strobe, LOW);
  shiftOut(data, clock, LSBFIRST, value);
  digitalWrite(strobe, HIGH);}

void sendDigit(int displ, int dig){
  sendCommand(0x44);
  digitalWrite(strobe, LOW);
  shiftOut(data, clock, LSBFIRST, displays[displ]);
  shiftOut(data, clock, LSBFIRST, dig);
  digitalWrite(strobe, HIGH);}

void setLed(uint8_t value, uint8_t position){
  pinMode(data, OUTPUT);
  sendCommand(0x44);
  digitalWrite(strobe, LOW);
  shiftOut(data, clock, LSBFIRST, 0xC1 + (position << 1));
  shiftOut(data, clock, LSBFIRST, value);
  digitalWrite(strobe, HIGH);}

void reset(){
  sendCommand(0x40); // set auto increment mode
  digitalWrite(strobe, LOW);
  shiftOut(data, clock, LSBFIRST, 0xc0);   // set starting address to 0
  for(uint8_t i = 0; i < 16; i++){
    shiftOut(data, clock, LSBFIRST, 0x00);}
  digitalWrite(strobe, HIGH);}

//Button Commands
void debounce(){
  uint8_t temp;
  //button scan
  uint8_t buttons = 0;
  digitalWrite(strobe, LOW);
  shiftOut(data, clock, LSBFIRST, 0x42);
  pinMode(data, INPUT);
  for (uint8_t i = 0; i < 4; i++){ //scans all of the buttons
    uint8_t v = shiftIn(data, clock, LSBFIRST) << i;
    buttons |= v;}
  pinMode(data, OUTPUT);
  digitalWrite(strobe, HIGH);

  //debounce input
  if(buttons != 0 && lastButtonTime < millis()){
      
    lastButtonTime = millis() + 500;
    for(int i = 0; i < 8; i++){ //This collects the buttong 
      if(buttons == int(1<<i)){
        if(buttonStates[i] == 1){
          buttonStates[i] = 0;}
        else{buttonStates[i] = 1;}}}
        
    if(modeState > 9){
      if(buttonStates[1] == 1){
        modeState = 0;
        scrollTextBreak = 1;
        modeSetState();}
      if(buttonStates[0] == 1){
        scrollTextBreak = 1;
        modeSetState();}}
      
    currentBinaryValue = 0;
    for(int i = 2; i <8 ; i++){
      setLed(buttonStates[i],i);
      if(buttonStates[i] == 1){
        currentBinaryValue += 1<<(7-i);}}
    Serial.print(F("Button Debounce Value: "));
    Serial.println(buttons);
    Serial.print(F("Binary Value: "));
    Serial.println(currentBinaryValue);
    Serial.print(F("Mode State: "));
    Serial.println(modeState);
    Serial.print(F("ButtonStates: "));
    for(int i = 0; i < 8; i++){Serial.print(buttonStates[i]);}
      Serial.println();}}

void buttonStateReset(){
  for(int i = 0; i < 8; i++){buttonStates[i] = 0;}}

//scroll text and Blinker
void blinker(){
  for(int i = 0; i < 8; i++){
        setLed(millis()*millis()%8, i);}
       for(int i = 0; i < 8; i++){
        setLed(int(pow(millis(),.5))%8, i);}}

void scrollText(const int text[], uint8_t length_of_text,uint8_t blinkin){//This is a "main mode" Function
  for(int j = 0; j < length_of_text - 7; j++){
    if(scrollTextBreak > 0){
    scrollTextBreak -= 1;
    Serial.print("Scroll Text Break: ");
    Serial.println(scrollTextBreak);
    break;}
    delay(delaySpeed);
    for(int i = 0; i < 8; i++){
      sendDigit(i,letters[text[j+i]]);
      alwaysRun();
  if(blinkin == 1){
    blinker();}}}}
    
//Clock Face
void clockFace(){
  reset();
  if(primesArePoisonState == 0){
    scrollText(primesArePoison,length_of_primesArePoison,1);
    ++primesArePoisonState;}  

  modeState = 0;
  buttonStateReset();
  counter = Timer - millis()/10;
  long centi_seconds = millis()/10;
  long centi_seconds_left = counter;
  int seconds_left = centi_seconds_left/100;
  int minutes_left = seconds_left/60;
  int mili_hundredths = centi_seconds_left % 10;
  int mili_tenths = (centi_seconds_left/10) % 10;
  int seconds_ones = seconds_left % 10;
  int seconds_tens = (seconds_left/10) % 6;
  int minutes_ones = minutes_left % 10;
  int minutes_tens = (minutes_left/10) % 6;
  sendDigit(7, digits[mili_tenths]);
  sendDigit(6, digits[seconds_ones] + B10000000 * mili_tenths);
  sendDigit(5, digits[seconds_tens]);
  sendDigit(4, digits[minutes_ones] + B10000000 * seconds_left);
  sendDigit(3, digits[minutes_tens]);
  blinker();
  alwaysRun();
  if(buttonStates[1] == 1 || buttonStates[2] == 1 || 
    buttonStates[4] == 1 || buttonStates[6] == 1){
      primesArePoisonState = 0;
      fail();}}
      
 //Binary Flash      
void binaryFlash(String binary){
  for(int i = 0; i < 6; i++){ //binary flash 1
    setLed(int(binary[i])-48,i+2);}} // with int(binary[x] ASCII Character Decimal Value for 0 is 48, could also use atol()  


void fail(){
  reset();
  sendCommand(0x89);
  scrollTextBreak = 0;
  scrollText(no,length_of_no,0);
  sendCommand(brightness);
  reset();
  modeState = 0;
}

//Tests
uint8_t binaryLED(){
    reset();
    alwaysRun();
    buttonStateReset();
    
    String binary;
    String binary2;
    String binaryA;
    uint8_t randNumber = random(1,30);
    uint8_t randNumber2 = random(randNumber,63-randNumber);
    uint8_t binaryAnswer = randNumber + randNumber2;
    
    scrollText (add, length_of_add,0);

    for(int i = 0; i < 6; i++) {
      binary += String(bitRead(randNumber,5-i));
      binary2 += String(bitRead(randNumber2,5-i));
      binaryA += String(bitRead(binaryAnswer,5-i));}

    Serial.println(randNumber);
    Serial.println(binary);
    Serial.println(randNumber2);
    Serial.println(binary2);
    Serial.println(binaryAnswer);
    Serial.println(binaryA);

    for(int j = 0; j<2; j++){ //This allows the two loops to scroll twice
      binaryFlash(binary);
      delay(1500);
      scrollText (to, length_of_to,0);
      reset();
      delay(500);
      binaryFlash(binary2);
      delay(2000);
      if(j == 0){ //so the numbers agian prompt is only read once
        scrollText(numbersAgain, length_of_numbersAgain,0);}}

    delay(1500);
    reset();
    while(modeState == 11){
      alwaysRun();
      scrollText(await_entry, length_of_await_entry,0);
      if(buttonStates[0] == 1){
        if(currentBinaryValue  ==  binaryAnswer){
          scrollTextBreak = 0;
          scrollText(correct,length_of_correct,0);
          modeState = 0;
          puzzleStates[0] = 1;
          digitalWrite(LED0, HIGH);
          for(int i = 0; i < 4; i++){Serial.print(puzzleStates[i]);}
          Serial.println();}
        else{
          fail();}}}}

void humid(){
  buttonStateReset();
  while(modeState == 41){
      alwaysRun();
      reset();    
      hum = dht.readHumidity();
      temper = (dht.readTemperature() * 1.8 + 32);
      sendDigit(0, digits[hum/10]);
      sendDigit(1, digits[hum%10]+ B10000000);
      sendDigit(2, letters[7]);
      if(temper > 100){
        sendDigit(3, digits[temper/100]);}
      sendDigit(4, digits[temper/10]);
      sendDigit(5, digits[temper%10]+ B10000000);
      sendDigit(6, letters[5]);
      if(buttonStates[0] == 1){
        if(hum > 89){
          scrollTextBreak = 0;
          scrollText(correct,length_of_correct,0);
          modeState = 0;
          puzzleStates[1] = 1;
          digitalWrite(LED1, HIGH);
          for(int i = 0; i < 4; i++){Serial.print(puzzleStates[i]);}
          Serial.println();}
        else{
          fail();}}}}

void photo(){
  const int Vin = 5;    // Control Voltage
  digitalWrite(PowerPhoto, HIGH);
  const int control = 10000; // Control Resistor  
  float Vout;
  float buffer;
  reset();
  buttonStateReset();
  
  while(modeState == 61){
    alwaysRun();
    
    buffer = analogRead(analogPinPhoto) * Vin;
    Vout = (buffer)/1024.0;
    buffer = (Vin/Vout) -1;
    float photo = control * buffer / 1000;
    uint8_t photo_display_thou = uint8_t(photo / 10);
    uint8_t photo_display_hund = uint8_t(photo) % 10;
    uint8_t photo_display_ten = uint8_t(photo * 10) % 10;
    uint8_t photo_display_one = uint8_t(photo * 100) % 10;

    Serial.println(photo);
    
    sendDigit(0, digits[photo_display_thou]);
    sendDigit(1, digits[photo_display_hund] + B10000000);
    sendDigit(2, digits[photo_display_ten]);
    sendDigit(3, digits[photo_display_one]);

    sendDigit(5, letters[10]);
    sendDigit(6, letters[14]);
    sendDigit(7, letters[12]);
    
    delay(100);
        
   if(buttonStates[0] == 1){
          if(21.1 < photo &&  photo < 41.9){
            scrollTextBreak = 0;
            scrollText(correct,length_of_correct,0);
            modeState = 0;
            puzzleStates[2] = 1;
            digitalWrite(LED2,HIGH);
            for(int i = 0; i < 4; i++){Serial.print(puzzleStates[i]);}
            Serial.println();
            digitalWrite(PowerPhoto, LOW);}
          else{
            fail();
            digitalWrite(PowerPhoto, LOW);}}}}


void resistor(){ //Check back with
  Serial.println("hi");
  const int Vin = 5;    // Control Voltage
  const int control = 10000; // Control Resistor  
  float Vout;
  float buffer;
  reset();
  buttonStateReset();
  
  while(modeState == 81){
    alwaysRun();
    
    buffer = analogRead(analogPinResis) * Vin;
    Vout = (buffer)/1024.0;
    buffer = (Vin/Vout) -1;
    float photo = control * buffer / 1000;
    uint8_t photo_display_thou = uint8_t(photo / 10);
    uint8_t photo_display_hund = uint8_t(photo) % 10;
    uint8_t photo_display_ten = uint8_t(photo * 10) % 10;
    uint8_t photo_display_one = uint8_t(photo * 100) % 10;

    Serial.println(photo);
    
    sendDigit(0, digits[photo_display_thou]);
    sendDigit(1, digits[photo_display_hund]);
    sendDigit(2, digits[photo_display_ten]);
    sendDigit(3, digits[photo_display_one]);
    sendDigit(4, digits[0]);

    sendDigit(6, letters[14]);
    sendDigit(7, letters[12]);
    
    delay(100);
        
   if(buttonStates[0] == 1){
          if(9.9 < photo &&  photo < 10.5){
            scrollTextBreak = 0;
            scrollText(correct,length_of_correct,0);
            modeState = 0;
            puzzleStates[3] = 1;
            digitalWrite(LED3,HIGH);
            for(int i = 0; i < 4; i++){Serial.print(puzzleStates[i]);}
            Serial.println();}
          else{
            fail();}}}}

//alwaysRun
void alwaysRun(){
  debounce();}

void modeSetState(){
  reset();
  Serial.print(F("New Mode State: "));
  Serial.println(modeState);}
  
//Mode

void modes(){
  
  alwaysRun();
  scrollTextBreak = 0;
  if(modeState == 0){
    clockFace();
    if(buttonStates[0] == 1 && puzzleStates[0] == 0){
      buttonStateReset();
      modeState = 10;
      modeSetState();}
      
    else if(buttonStates[3] == 1 && puzzleStates[1] == 0){
      buttonStateReset(); 
      modeState = 40;
      modeSetState();}
      
    else if(buttonStates[5] == 1 && puzzleStates[2] == 0){
      buttonStateReset(); 
      modeState = 60;
      modeSetState();}
    
    else if(buttonStates[7] == 1 && puzzleStates[3] == 0){
      buttonStateReset(); 
      modeState = 80;
      modeSetState();;}}

  else if(modeState == 10){
    scrollText(quiz10, length_of_quiz10, 1);
    if(buttonStates[0] == 1){
      modeState = 11;
      modeSetState();
      binaryLED();}}
      
  else if(modeState == 40){
    scrollText(quiz40, length_of_quiz40, 1); 
    if(buttonStates[0] == 1){
      modeState = 41;
      modeSetState();}}

  else if(modeState == 41){
    humid();}

  else if(modeState == 60){
    scrollText(quiz60, length_of_quiz60, 1);
    if(buttonStates[0] == 1){
      modeState = 61;
      modeSetState();}}

  else if(modeState == 61){
  photo();}

  else if(modeState == 80){
    scrollText(quiz80, length_of_quiz80, 1);
    if(buttonStates[0] == 1){
      modeState = 81;
      modeSetState();}}

  else if(modeState == 81){
  resistor();}}

void setup(){
  Serial.begin(9600);
  pinMode(strobe, OUTPUT);
  pinMode(clock, OUTPUT);
  pinMode(data, OUTPUT);
  pinMode(buzzer, OUTPUT);
  digitalWrite(buzzer, LOW);
  digitalWrite(LED0, HIGH);
  digitalWrite(LED1, OUTPUT);
  digitalWrite(LED2, OUTPUT);
  digitalWrite(LED3, OUTPUT);
  digitalWrite(PowerPhoto, OUTPUT);
  digitalWrite(ground, OUTPUT);
  sendCommand(brightness);
  reset();
  dht.begin();
  hum = dht.readHumidity();
  randomSeed(analogRead(1));
  modeState = 0;
  primesArePoisonState = 0; //Set this value to 0 when ready
  digitalWrite(LED0, LOW);
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
  digitalWrite(PowerPhoto, LOW);
  digitalWrite(ground, LOW);
  }

void loop(){
  modeCount = 0;
  modes();
  for(int i = 0; i<4; i++){modeCount += puzzleStates[i];}
  while(modeCount == 4){
    reset();
    scrollText(solution, length_of_solution, 0); 
    Serial.println("done!");}}
