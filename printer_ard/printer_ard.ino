//d 1step: 0.24mm
//r&l 1step: 0.32mm

//X축 모터: A4988
//0.17A, 3.67k옴

//L모터: DRV8825
//0.11A, 1.23k옴

//R모터: DRV8825
//0.16A, 1.198k옴


#define LIMIT_PIN 9
#define SOLENOID_PIN 8
#define X_STEP_PIN 7
#define X_DIR_PIN 6
#define Y_STEP_PIN1 5
#define Y_DIR_PIN1 4
#define Y_STEP_PIN2 3
#define Y_DIR_PIN2 2

bool SOL_init = 0;

const int MOTOR_DELAY = 1000;

const int maxChar = 15;
char charVal[maxChar];
int charIter = 0;


void setup()
{
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(7, OUTPUT);
    pinMode(8, OUTPUT);
    pinMode(9, INPUT);
    Serial.begin(9600);
}

void loop()
{
    if(Serial.available() > 0)
    {
        char a = Serial.read();
        if(a == '`')
        {
            processSerial();
            Serial.println(charVal);

            //initializing part
            for(int i = 0; i < maxChar; ++i)
            {
                charVal[i] = '\0';
            }
            charIter = 0;
        }
        else
        {
            charVal[charIter] = a;
            charIter += 1;
        }
    }
}

int pick_integer(char* str) 
{ /* 문자열에서 숫자만 추출하는 함수 */
	int num=0, plus=0;
	
	for(int i=0; i < maxChar; i++)
    { //문자열의 길이만큼 반복
        if(str[i] > 47 && str[i] < 58) 
        {num = num*10 + str[i]-48;}		
	}
    return num;
}

void processSerial()
{
    char decision = charVal[0];
    int tmpInt = pick_integer(charVal);

    if(decision == 'p')
    {
        digitalWrite(SOLENOID_PIN, HIGH);
        delay(200);
    }
    else if(decision == 'P')
    {
        digitalWrite(SOLENOID_PIN, LOW);
        delay(70);
    }
    else if(decision == 'd')
    {
        ctrl_Y_motor_d(Y_DIR_PIN1, Y_DIR_PIN2, Y_STEP_PIN1, Y_STEP_PIN2, tmpInt);
    }
    else if(decision == 'u')
    {
        ctrl_Y_motor_u(Y_DIR_PIN1, Y_DIR_PIN2, Y_STEP_PIN1, Y_STEP_PIN2, tmpInt);
    }
    else if(decision == 'r')
    {
        ctrl_motor(X_DIR_PIN, X_STEP_PIN, HIGH, tmpInt);
    }
    else if(decision == 'l')
    {
         ctrl_motor(X_DIR_PIN, X_STEP_PIN, LOW, tmpInt);
    }
    else if(decision == 'i')
    {
        act_limit();
    }
}

void ctrl_motor(int motor_dir_pin, int motor_step_pin, int motor_dir, int motor_step)
{
    if(motor_dir == HIGH)
    {
        digitalWrite(motor_dir_pin, HIGH);
    }
    else
    {
        digitalWrite(motor_dir_pin, LOW);
    }
    for(int i = 0; i < motor_step * 4; ++i)
    {
        digitalWrite(motor_step_pin, HIGH);
        delayMicroseconds(MOTOR_DELAY);
        digitalWrite(motor_step_pin, LOW);
        delayMicroseconds(MOTOR_DELAY);
    }
}

void ctrl_Y_motor_d(int motor_dir_pin1, int motor_dir_pin2, int motor_step_pin1, int motor_step_pin2, int motor_step)
{
    digitalWrite(motor_dir_pin1, HIGH);
    digitalWrite(motor_dir_pin2, LOW);
    for(int i = 0; i < motor_step * 3; ++i)
    {
        digitalWrite(motor_step_pin1, HIGH);
        digitalWrite(motor_step_pin2, HIGH);
        delayMicroseconds(MOTOR_DELAY * 2);
        digitalWrite(motor_step_pin1, LOW);
        digitalWrite(motor_step_pin2, LOW);
        delayMicroseconds(MOTOR_DELAY * 2);
    }
}

void ctrl_Y_motor_u(int motor_dir_pin1, int motor_dir_pin2, int motor_step_pin1, int motor_step_pin2, int motor_step)
{
    digitalWrite(motor_dir_pin1, LOW);
    digitalWrite(motor_dir_pin2, HIGH);
    for(int i = 0; i < motor_step * 3; ++i)
    {
        digitalWrite(motor_step_pin1, HIGH);
        digitalWrite(motor_step_pin2, HIGH);
        delayMicroseconds(MOTOR_DELAY * 2);
        digitalWrite(motor_step_pin1, LOW);
        digitalWrite(motor_step_pin2, LOW);
        delayMicroseconds(MOTOR_DELAY * 2);
    }
}

void act_limit()
{
    while (SOL_init == 0)
    {
        bool limit_data = digitalRead(LIMIT_PIN);
        if (limit_data == 0)
        {
            ctrl_motor(X_DIR_PIN, X_STEP_PIN, LOW, 1);
        }
        else
        {
            ctrl_motor(X_DIR_PIN, X_STEP_PIN, HIGH, 30);
            SOL_init = 1;
        }
    }
}
