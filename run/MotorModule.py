import RPi.GPIO as GPIO
from time import sleep
import serial
import pandas as pd

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.EnaB, 100)
        self.pwmB.start(0)

    def moveF(self, speed=1.0, turn=0, t=1):
        speed *= 100
        turn *= 100

        left_speed = speed - turn
        right_speed = speed + turn

        if left_speed > 100:
            left_speed = 100
        elif left_speed < -100:
            left_speed = -100

        if right_speed > 100:
            right_speed = 100
        elif right_speed < -100:
           right_speed = -100

        self.pwmA.ChangeDutyCycle(abs(left_speed))
        self.pwmB.ChangeDutyCycle(abs(right_speed))

        if left_speed > 0:
            GPIO.output(self.In1A, GPIO.HIGH)
            GPIO.output(self.In2A, GPIO.LOW)
        else:
            GPIO.output(self.In1A, GPIO.LOW)
            GPIO.output(self.In2A, GPIO.HIGH)

        if right_speed > 0:
            GPIO.output(self.In1B, GPIO.HIGH)
            GPIO.output(self.In2B, GPIO.LOW)
        else:
            GPIO.output(self.In1B, GPIO.LOW)
            GPIO.output(self.In2B, GPIO.HIGH)

        sleep(t)

    def moveB(self, speed=1.0, turn=0, t=1):
        speed *= 100
        turn *= 100

        GPIO.output(self.In1A, GPIO.HIGH)
        GPIO.output(self.In2A, GPIO.LOW)
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1B, GPIO.HIGH)
        GPIO.output(self.In2B, GPIO.LOW)
        self.pwmB.ChangeDutyCycle(speed)
        sleep(t)

    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        sleep(t)

def main():
    motor1.stop(0.0001)
    s = init_communication("/dev/ttyUSB0", 9600)
    stored_data = []
    while True:
        data = get_data(s)
        stored_data.append(data)
        print(data)
        motor1.moveF(0.2, 0.0, 0.00001)
        if float(data[0]) >= 10.0:
            break

    motor1.stop(0.0001)

    df = pd.DataFrame(stored_data, columns=['tempo', 'velocidade'])
    print(df)
    df.to_csv('/home/pi/Documents/motor speed data--step 0,2--sample_rate 0,1s.csv', sep=',', index=False)


def init_communication(port_num, baud_rate):
    try:
        s = serial.Serial(port=port_num, baudrate=baud_rate)
        print('Device Connected')
        return s
    except Exception as e:
        print(e)
        print('Connection Falied')


def get_data(ser):
    data_arduino = ser.readline()
    data_arduino = data_arduino.decode("utf-8")
    data_arduino = data_arduino.split(", ")
    data_list = []
    [data_list.append(d) for d in data_arduino]
    return data_list[:-1]



if __name__ == '__main__':

    motor1 = Motor(2,3,4,17,22,27)
    main()
