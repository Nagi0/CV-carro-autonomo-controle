import serial
import pandas as pd


def init_communication(port_num, baud_rate):
    try:
        s = serial.Serial(port=port_num, baudrate=baud_rate)
        print('Device Connected')
        return s
    except Exception as e:
        print(f'Error Specification: {e}')
        print("Connection Failed")


def get_data(ser):
    data_arduino = ser.readline()
    data_arduino = data_arduino.decode("utf-8")
    data_arduino = data_arduino.split(', ')
    data_list = []
    [data_list.append(d) for d in data_arduino]
    return data_list[:-1]


if __name__ == "__main__":
    s = init_communication("COM5", 9600)
    stored_data = []
    while True:
        data = get_data(s)
        print(data)
        stored_data.append(data)
        if float(data[0]) >= 10.0:
            break

    df = pd.DataFrame(stored_data, columns=['tempo', 'velocidade'])
    print(df)
    df.to_csv('motor speed--step value 0.2--sample 0.1s.csv')
