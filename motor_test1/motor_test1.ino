// 쓰이는 핀을 정의 합니다.
const int stepPin = 4;
const int dirPin = 3;

void setup() {
  // 두핀을 OUTPUT으로 정의 합니다.
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}


void loop() {
  digitalWrite(dirPin, HIGH); // 모터를 특정한 방향으로 설정합니다.

  // 모터가 한바퀴를 돌기위해서는 200펄스가 필요합니다.
  for (int x = 0; x < 200; x++) {
  digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }

  delay(1000); // 1초 딜레이
  digitalWrite(dirPin, LOW); // 모터를 반대 방향으로 설정합니다.

  // 모터가 세바퀴를 돌기위해서는 600 펄스가 필요합니다.
  for (int x = 0; x < 600; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }

  delay(1000); // 1초 딜레이
}