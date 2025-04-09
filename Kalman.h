#ifndef _KALMAN_H_
#define _KALMAN_H_

class Kalman {
public:
    Kalman();
    float getAngle(float newAngle, float newRate, float dt);
    void setAngle(float angle);
    float getRate();
    void setQangle(float Q_angle);
    void setQbias(float Q_bias);
    void setRmeasure(float R_measure);
    float getQangle();
    float getQbias();
    float getRmeasure();

private:
    float Q_angle;  // 加速计的过程噪声方差
    float Q_bias;   // 陀螺仪偏差的过程噪声方差
    float R_measure; // 测量噪声方差
    float angle;    // 卡尔曼滤波计算的角度
    float bias;     // 陀螺仪偏差
    float rate;     // 无偏速率
    float P[2][2];  // 误差协方差矩阵
};

#endif
