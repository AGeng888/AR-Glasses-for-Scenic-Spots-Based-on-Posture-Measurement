#include <stdio.h>
#include <wiringPi.h>
#include <iostream>
#include "Kalman.h"
#include "JY901.h"

#define uchar unsigned char
#define uint unsigned int

unsigned long int counter;
int STBY = 2;
int PWMA = 1;
int AIN1 = 25;
int AIN2 = 6;
int PWMB = 24;
int BIN1 = 4;
int BIN2 = 5;

void left(int speed) {
    digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); digitalWrite(BIN1, LOW); digitalWrite(BIN2, LOW);
    delay(speed);
    digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, LOW); digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); digitalWrite(BIN1, LOW); digitalWrite(BIN2, LOW);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, LOW); digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH);
    delay(speed);
    digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH);
    delay(speed);
}

void right(int speed) {
    digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, LOW); digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); digitalWrite(BIN1, LOW); digitalWrite(BIN2, LOW);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW);
    delay(speed);
    digitalWrite(AIN1, LOW); digitalWrite(AIN2, LOW); digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW);
    delay(speed);
    digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW);
    delay(speed);
    digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); digitalWrite(BIN1, LOW); digitalWrite(BIN2, LOW);
    delay(speed);
}

int main(void) {
    wiringPiSetup();
    pinMode(STBY, OUTPUT);
    pinMode(PWMA, OUTPUT);
    pinMode(AIN1, OUTPUT);
    pinMode(AIN2, OUTPUT);
    pinMode(PWMB, OUTPUT);
    pinMode(BIN1, OUTPUT);
    pinMode(BIN2, OUTPUT);
    digitalWrite(STBY, HIGH);
    digitalWrite(PWMA, HIGH);
    digitalWrite(PWMB, HIGH);
    jy901_set_addr(0x50);
    int k = 1;
    double a[1000];
    printf("\ninit:%#x\n", jy901_init(&fd));
    printf("\ncali:%d\n", jy901_cali());
    if (INIT_SUCCESS == jy901_init(&fd)) {
        angle attitude;
        accel acceleration;
        omega w;
        jy901_cali();
        for (int n = 0; n < 20; n++) {
            float angle1 = 0.0f;
            Kalman temp;
            jy901_getAngle(&attitude);
            jy901_getAccel(&acceleration);
            jy901_getOmega(&w);
            angle1 = temp.getAngle(attitude.roll, w.wx, 0.5);
            std::cout << angle1 << std::endl;
            a[0] = 0.0;
            a[k] = angle1;
            if (a[k] - a[k - 1] > 1) {
                for (int i = 0; i < a[k] / 1.8; i++) left(2);
            }
            if (a[k] - a[k - 1] < -1) {
                for (int j = 0; j < (-a[k]) / 1.8; j++) right(2);
            }
            k++;
            delay(500);
        }
        digitalWrite(STBY, LOW);
        digitalWrite(PWMA, LOW);
        digitalWrite(AIN1, LOW);
        digitalWrite(AIN2, LOW);
        digitalWrite(PWMB, LOW);
        digitalWrite(BIN1, LOW);
        digitalWrite(BIN2, LOW);
    } else {
        printf("Initialization failed, err=%#x\n", jy901_init(&fd));
    }
    return 0;
}
