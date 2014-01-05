import re
import sqlite3
import subprocess


def strip(string):
    return re.sub("[^0-9a-zA-z.]", "", string)


def write_sensors_to_db(sensors):
    connection = sqlite3.connect("../db/elctrl.db")
    cursor = connection.cursor()
    for id, sensor in sensors.items():
        cursor.execute("select ID from SensorData where SensorID=? and Time=?", (id, sensor["time"]))
        if cursor.fetchone() is None:
            cursor.execute("insert into SensorData (SensorID, Temperature, Humidity, Time) values (?, ?, ?, ?)", (id, sensor["temperature"], sensor["humidity"], sensor["time"]))
    connection.commit()
    connection.close()


def execute_tdtool():
    p = subprocess.Popen(["tdtool", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.splitlines()


def parse_tdtool(lines):
    protocol_found = False
    pos_model = 0
    pos_id = 0
    pos_temp = 0
    pos_hum = 0
    pos_time = 0
    sensors = {}
    for line in lines:
        if protocol_found:
            model = strip(line[pos_model:pos_id - 1])
            if model.find("temperaturehumidity") != -1 or len(model) == 0:
                continue

            id = strip(line[pos_id:pos_temp - 1])
            sensors[id] = {}
            sensors[id]["temperature"] = strip(line[pos_temp:pos_hum - 1])
            sensors[id]["humidity"] = strip(line[pos_hum:pos_time - 1])
            sensors[id]["time"] = line[pos_time: len(line)].strip()

        elif line.startswith("PROTOCOL"):
            protocol_found = True
            pos_model = line.find("MODEL")
            pos_id = line.find("ID")
            pos_temp = line.find("TEMP")
            pos_hum = line.find("HUMIDITY")
            pos_time = line.find("LAST")

    return sensors


def read_file(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        return lines


if __name__ == '__main__':
    output = execute_tdtool()
    data = parse_tdtool(output)
    write_sensors_to_db(data)
