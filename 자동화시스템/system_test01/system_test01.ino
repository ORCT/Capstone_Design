String serData;
#define SOL 8    // Solenoid
#define RIGHT OUTPUT  // Motor
#define LEFT LOW
#define PHOTO 10      // Sensor
#define LMITS 9
#define XDIR 4
#define XSTEP 5
#define YDIR 6
#define YSTEP 7

bool P_in;          // Sensor
bool SW;
bool Xhome = 0;
bool Yhome = 0;

void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  Serial.begin(9600);
  Serial.println("Arduino is ready!");
}

void loop() {
  while(Serial.available() > 0){
    char rec = Serial.read();
    serData += rec;

    if (rec=='r'){
      Serial.println(serData);
      digitalWrite(2, HIGH);
      delay(10);
      digitalWrite(2, LOW);
      serData="";
    }
    else if (rec=='R'){
      Serial.println(serData);
      digitalWrite(3, HIGH);
      delay(10);
      digitalWrite(3, LOW);
      serData="";
    }
    else if (rec=='l'){
      Serial.println(serData);
      digitalWrite(4, HIGH);
      delay(10);
      digitalWrite(4, LOW);
      serData="";
    }
    else if (rec=='L'){
      Serial.println(serData);
      digitalWrite(5, HIGH);
      delay(10);
      digitalWrite(5, LOW);
      serData="";
    }
    else if (rec=='d'){
      Serial.println(serData);
      digitalWrite(6, HIGH);
      delay(10);
      digitalWrite(6, LOW);
      serData="";
    }
    else if (rec=='D'){
      Serial.println(serData);
      digitalWrite(7, HIGH);
      delay(10);
      digitalWrite(7, LOW);
      serData="";
    }
    else if (rec=='p'){
      Serial.println(serData);
      digitalWrite(8, HIGH);
      delay(10);
      digitalWrite(8, LOW);
      serData="";
    }
    else
    {
      Serial.println("Unknown");
      serData="";
    }
  }
delay(10);
}

int step_Mov(int num, int dir, int tic) {

  digitalWrite(num - 1, dir);

  for (int x = 0; x < tic; x++) {
    digitalWrite(num, HIGH);
    delayMicroseconds(1000);
    digitalWrite(num, LOW);
    delayMicroseconds(1000);
  }
  return 0;
}
void Push() {
  digitalWrite(Solenoid, HIGH);
  delay(60);
  digitalWrite(Solenoid, LOW);
}
