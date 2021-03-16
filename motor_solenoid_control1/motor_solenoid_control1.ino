#include<ctype.h>
#include<stdlib.h>
#define SOLENOID_PIN 2
#define X_DIR_PIN 3
#define X_STEP_PIN 4
#define Y_DIR_PIN 5
#define Y_STEP_PIN 6
#define RIGHT OUTPUT  // Motor
#define LEFT LOW

#define MAX_REPOS 7

const int MOTOR_DELAY = 1000;
const int TIME_DELAY = 100;

const int TIME_DELAY = 10;
String ser_data;
char num_repos[MAX_REPOS];
int num_repos_iter = 0;
int dir_flag = 0;

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

        if (rec == 'p')
        {
            Serial.println(ser_data);
            digitalWrite(SOLENOID_PIN, HIGH);
        }
        else if (rec == 'P')
        {
            Serial.println(ser_data);
            digitalWrite(SOLENOID_PIN, LOW);
        }
        else if (rec == 'r')
        {
            Serial.println(ser_data);
            digitalWrite(X_DIR_PIN, HIGH);
        }
        else if (rec == 'l')
        {
            Serial.println(ser_data);
            digitalWrite(X_STEP_PIN, LOW);
        }
        else if (rec == 'd')
        {
            Serial.println(ser_data);
            dir_flag = 2;
        }

        else if (isdigit(rec) != 0)
        {
            Serial.println(ser_data);
            num_repos[num_repos_iter] = rec;
            num_repos_iter += 1;
        }
        else if (rec == '`')
        {
            int tmp = atoi(num_repos);
            Serial.println(tmp);
            for(int i = 0; i < MAX_REPOS; ++i)
            {
                num_repos[i] = '\0';
            }
            num_repos_iter = 0;
        }
        else
        {
            Serial.println('U');
        }

        ser_data = "";
        delay(TIME_DELAY);
    }
}

void ctrl_solenoid()
{

}