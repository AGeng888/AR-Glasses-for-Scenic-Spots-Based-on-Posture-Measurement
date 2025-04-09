#ifndef _JY901_H_
#define _JY901_H_

#define default_addr 0x50
#define INTERFACE_ERR 0x01
#define DEVICE_ERR 0x02
#define INIT_SUCCESS 0x03
#define g 9.80665
#define default_control_word 0x07df

typedef struct {
    int roll;
    int pitch;
    int yaw;
} raw_angle;

typedef struct {
    int ax;
    int ay;
    int az;
} raw_accel;

typedef struct {
    float roll;
    float pitch;
    float yaw;
} angle;

typedef struct {
    float ax;
    float ay;
    float az;
} accel;

typedef struct {
    int longti[2];
    int lati[2];
    int gpsYaw;
    int gpsv[2];
    int accur;
    int sat_num;
} raw_gps;

typedef struct {
    float longti;
    float lati;
    float gpsYaw;
    float gpsv;
    float accur;
    int sat_num;
} gps;

typedef struct {
    int wx;
    int wy;
    int wz;
} raw_omega;

typedef struct {
    float wx;
    float wy;
    float wz;
} omega;

void jy901_set_addr(unsigned char actu_addr);
bool jy901_config(unsigned short int control_word);
bool jy901_cali();
unsigned char jy901_init(int *fd);
bool jy901_getAngle(angle *attitude);
bool jy901_getAccel(accel *rate);
bool jy901_getGPS(gps *gps);
void gpstest(raw_gps *gps);
bool jy901_getOmega(omega *w);
bool jy901_sleep(bool set);

#endif
