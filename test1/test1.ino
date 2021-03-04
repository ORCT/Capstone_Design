String serData;
const int TIME_DELAY = 10;

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
    while (Serial.available() > 0)
    {
        char rec = Serial.read();
        serData += rec;

        if (rec == '3')
        {
            Serial.println(serData);
            func1(3);
            serData = "";
            delay(TIME_DELAY);
        }
        else if (rec == '4')
        {
            Serial.println(serData);
            func1(4);
            serData = "";
            delay(TIME_DELAY);
        }
        else if (rec == '#')
        {
            Serial.println(serData);
            func2(3);
            serData = "";
            delay(TIME_DELAY);
        }
        
        else if (rec == '$')
        {
            Serial.println(serData);
            func2(4);
            serData = "";
            delay(TIME_DELAY);
        }
        else
        {
            Serial.println('l');
            serData = "";
            delay(TIME_DELAY);
        }
    }
    delay(10);
}

void func1(int _pin_num)
{
    digitalWrite(_pin_num, HIGH);
}

void func2(int _pin_num)
{
    digitalWrite(_pin_num, LOW);
}