#include <wiringPiI2C.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "JY901.h"

bool is_inited = false;
unsigned char addr = default_addr;
unsigned char bit_buff = 0xff;
short unsigned int word_buff = 0xffff;
int fd;

void jy901_set_addr(unsigned char actu_addr) {
    addr = actu_addr;
    is_inited = false;
}

bool jy901_config(unsigned short int control_word) {
    if (is_inited) {
        return wiringPiI2CWriteReg16(fd, 0x02, control_word) >= 0;
    }
    return false;
}

bool jy901_cali() {
    int states[3] = {0, 0, 0};
    short unsigned int offset_buff[20][9];
    short unsigned int offset[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
    states[0] = wiringPiI2CWriteReg16(fd, 0x01, 0x0001);
    states[1] = wiringPiI2CWriteReg16(fd, 0x00, 0x0001);
    jy901_config(default_control_word);
    if (states[0] >= 0 && states[1] >= 0) {
        printf("Calibrating, please keep the sensor static for a while.\n");
        for (int j = 0; j < 20; j++)
            for (int i = 0; i + 0x34 < 0x3d; i++)
                offset_buff[j][i] = wiringPiI2CReadReg16(fd, i + 0x34);
        for (int j = 0; j < 9; j++)
            for (int i = 0; i < 20; i++)
                offset[j] += offset_buff[i][j];
        for (int i = 0; i < 9; i++)
            offset[i] /= 9;
        for (int i = 0; i < 9; i++) {
            states[0] = wiringPiI2CWriteReg16(fd, i + 0x05, offset[i]);
            if (states[0] < 0) {
                states[2] = states[0];
                break;
            }
        }
        states[0] = wiringPiI2CWriteReg16(fd, 0x00, 0x0001);
        if (states[0] >= 0 && states[2] >= 0) {
            printf("Calibration complete.\n");
            return true;
        } else {
            printf("Calibration failed.\n");
            return false;
        }
    } else {
        printf("Calibration failed.\n");
        return false;
    }
}

unsigned char jy901_init(int *fd) {
    *fd = wiringPiI2CSetup(addr);
    if (*fd >= 0) {
        bit_buff = wiringPiI2CReadReg8(*fd, 0x1a);
        if (addr == bit_buff) {
            jy901_cali();
            is_inited = true;
            return INIT_SUCCESS;
        } else {
            printf("device address mismatch:\nsetting:%#x\nactual:%#x\n", addr, bit_buff);
            return DEVICE_ERR;
        }
    }
    return INTERFACE_ERR;
}

bool jy901_getAngle(angle *attitude) {
    if (is_inited) {
        raw_angle buff;
        buff.roll = wiringPiI2CReadReg16(fd, 0x3d);
        buff.pitch = wiringPiI2CReadReg16(fd, 0x3e);
        buff.yaw = wiringPiI2CReadReg16(fd, 0x3f);
        attitude->roll = ((float)buff.roll) / 32768 * 180;
        attitude->pitch = ((float)buff.pitch) / 32768 * 180;
        attitude->yaw = ((float)buff.yaw) / 32768 * 180;
        return true;
    } else {
        printf("ERROR: sensor not initialized.\n");
        return false;
    }
}

bool jy901_getAccel(accel *rate) {
    if (is_inited) {
        raw_accel buff;
        buff.ax = wiringPiI2CReadReg16(fd, 0x34);
        buff.ay = wiringPiI2CReadReg16(fd, 0x35);
        buff.az = wiringPiI2CReadReg16(fd, 0x36);
        rate->ax = ((float)buff.ax) / 32768 * 16 * g;
        if (rate->ax >= 16 * g) rate->ax -= 32 * g;
        rate->ay = ((float)buff.ay) / 32768 * 16 * g;
        if (rate->ay >= 16 * g) rate->ay -= 32 * g;
        rate->az = ((float)buff.az) / 32768 * 16 * g;
        if (rate->az >= 16 * g) rate->az -= 32 * g;
        return true;
    } else {
        printf("ERROR: sensor not initialized.\n");
        return false;
    }
}

bool jy901_getGPS(gps *gps) {
    if (is_inited) {
        raw_gps buff;
        buff.longti[1] = wiringPiI2CReadReg16(fd, 0x4a);
        buff.longti[0] = wiringPiI2CReadReg16(fd, 0x49);
        buff.lati[1] = wiringPiI2CReadReg16(fd, 0x4c);
        buff.lati[0] = wiringPiI2CReadReg16(fd, 0x4b);
        buff.gpsYaw = wiringPiI2CReadReg16(fd, 0x4e);
        buff.gpsv[1] = wiringPiI2CReadReg16(fd, 0x50);
        buff.gpsv[0] = wiringPiI2CReadReg16(fd, 0x4f);
        buff.accur = wiringPiI2CReadReg16(fd, 0x56);
        gps->sat_num = wiringPiI2CReadReg16(fd, 0x55);
        gps->longti = ((float)((buff.longti[1] << 16) | buff.longti[0])) / 10000000;
        gps->lati = ((float)((buff.lati[1] << 16) | buff.lati[0])) / 10000000;
        gps->gpsYaw = ((float)buff.gpsYaw) / 100;
        gps->gpsv = (float)(((buff.gpsv[1] << 16) | buff.gpsv[0])) / 100000000;
        gps->accur = ((float)(buff.accur)) / 100;
        return true;
    } else {
        printf("ERROR: sensor not initialized.\n");
        return false;
    }
}

void gpstest(raw_gps *gps) {
    gps->longti[1] = wiringPiI2CReadReg16(fd, 0x4a);
    gps->longti[0] = wiringPiI2CReadReg16(fd, 0x49);
    gps->lati[1] = wiringPiI2CReadReg16(fd, 0x4c);
    gps->lati[0] = wiringPiI2CReadReg16(fd, 0x4b);
    gps->gpsYaw = wiringPiI2CReadReg16(fd, 0x4e);
    gps->gpsv[1] = wiringPiI2CReadReg16(fd, 0x50);
    gps->gpsv[0] = wiringPiI2CReadReg16(fd, 0x4f);
    gps->accur = wiringPiI2CReadReg16(fd, 0x56);
    gps->sat_num = wiringPiI2CReadReg16(fd, 0x55);
}

bool jy901_getOmega(omega *w) {
    if (is_inited) {
        raw_omega buff;
        buff.wx = wiringPiI2CReadReg16(fd, 0x37);
        buff.wy = wiringPiI2CReadReg16(fd, 0x38);
        buff.wz = wiringPiI2CReadReg16(fd, 0x39);
        w->wx = (float)(buff.wx) / 32768 * 2000;
        w->wy = (float)(buff.wy) / 32768 * 2000;
        w->wz = (float)(buff.wz) / 32768 * 2000;
        if (w->wx >= 2000) w->wx -= 4000;
        if (w->wy >= 2000) w->wy -= 4000;
        if (w->wz >= 2000) w->wz -= 4000;
        return true;
    } else {
        printf("ERROR: sensor not initialized.\n");
        return false;
    }
}

bool jy901_sleep(bool set) {
    if (is_inited) {
        return wiringPiI2CWriteReg16(fd, 0x22, set) >= 0;
    } else {
        printf("ERROR: sensor not initialized.\n");
        return false;
    }
}
