#include<Wire.h>
#include<MPU6050.h>
MPU6050 mpu;
int16_t ax, ay, az, gx, gy, gz;
float accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
}

void loop() {
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  accel_x = (float)ax / 16384.0 * 9.81;
  accel_y = (float)ay / 16384.0 * 9.81;
  accel_z = (float)az / 16384.0 * 9.81;
  gyro_x = (float)gx / 131.0 * 0.0174533;
  gyro_y = (float)gy / 131.0 * 0.0174533;
  gyro_z = (float)gz / 131.0 * 0.0174533;
  
  Serial.print(accel_x);
  Serial.print(",");
  Serial.print(accel_y);
  Serial.print(",");
  Serial.print(accel_z);
  Serial.print(",");
  Serial.print(gyro_x);
  Serial.print(",");
  Serial.print(gyro_y);
  Serial.print(",");
  Serial.println(gyro_z);
  
  delay(100);
}
