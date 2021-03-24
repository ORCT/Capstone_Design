// 상수형 선언자리
const int TIME_DELAY = 10;

//전역형 선언자리
String ser_data;



void setup()
{
    
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(7, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
    while(Serial.available() > 0)
    {
        char rec = Serial.read();
        ser_data += rec;
        
        //실행 영역

        if (rec == '3')
        {
            Serial.println(ser_data);
            func1(3);
        }
        else if (rec == '4')
        {
            Serial.println(ser_data);
            func1(4);
        }
        else if (rec == '5')
        {
            Serial.println(ser_data);
            func1(5);
        }
        else if (rec == '6')
        {
            Serial.println(ser_data);
            func1(6);
        }
        else if (rec == '#')
        {
            Serial.println(ser_data);
            func2(3);
        }
        else if (rec == '$')
        {
            Serial.println(ser_data);
            func2(4);
        }
        else if (rec == '%')
        {
            Serial.println(ser_data);
            func2(5);
        }
        else if (rec == '^')
        {
            Serial.println(ser_data);
            func2(6);
        }
        else
        {
            Serial.println('U');
        }

        //공통실행 끝부분

        ser_data = "";
        delay(TIME_DELAY);
    }
}


void func1(int _pin_num)
{
    digitalWrite(_pin_num, HIGH);
}

void func2(int _pin_num)
{
    digitalWrite(_pin_num, LOW);
}


// int mov_step(int num, int dir, int tic, int vel) {

//   digitalWrite(num - 1, dir);

//   for (int x = 0; x < tic; x++) {
//     digitalWrite(num, HIGH);
//     delayMicroseconds(vel);
//     digitalWrite(num, LOW);
//     delayMicroseconds(vel);
//   }
//   return 0;
// }
// void push() {
//   digitalWrite(SOL, HIGH);
//   delay(60);
//   digitalWrite(SOL, LOW);
//   delay(100);
// }

// void home_init() {   //Find Home position

//   while (Xhome == 0) { // Home
//     SW = digitalRead(LMITS);
//     if (Xhome == 0) {
//       if (SW == 1)
//         mov_step(XSTEP, RIGHT, 1, 2000);
//       else if (SW == 0) {      // SW ON
//         mov_step(XSTEP, LEFT, 30, 2000);
//         Xhome = 1;
//       }
//     }
//   }
//   while (Yhome == 0) {
//     P_in = digitalRead(PHOTO);
//     if (P_in == 1)
//       mov_step(YSTEP, RIGHT, 1, 2000);
//     else if (P_in == 0) {    // Paper Detected
//       delay(500);
//       mov_step(YSTEP, RIGHT, 210, 2000);
//       Yhome = 1;
//     }
//   }

//   delay(1000);
// }