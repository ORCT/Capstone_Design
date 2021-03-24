const int stepPin1 = 4;
const int dirPin1 = 3;
const int stepPin2 = 6;
const int dirPin2 = 5;

void setup()
{
    pinMode(stepPin1, OUTPUT);
    pinMode(dirPin1, OUTPUT);
    pinMode(stepPin2, OUTPUT);
    pinMode(dirPin2, OUTPUT);
}

void loop()
{
    digitalWrite(dirPin1, HIGH);

    for (int x = 0; x < 200; x++)
    {
        digitalWrite(stepPin1, HIGH);
        delayMicroseconds(1000);
        digitalWrite(stepPin1, LOW);
        delayMicroseconds(1000);
    }
    delay(500);
    digitalWrite(dirPin2, HIGH);

    for (int x = 0; x < 200; x++)
    {
        digitalWrite(stepPin2, HIGH);
        delayMicroseconds(1000);
        digitalWrite(stepPin2, LOW);
        delayMicroseconds(1000);
    }
    delay(500);
}