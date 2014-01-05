import sqlite3


def drop_and_create_sensors(cursor):
    drop_and_create = [
        "drop table if exists SensorData",
        "drop table if exists Sensor",
        "create table Sensor(Id integer primary key, Name text)",
        "create table SensorData(Id integer primary key asc, SensorId integer, Temperature real, Humidity real, Time text, foreign key(SensorId) references Sensor(Id))"
    ]

    for row in drop_and_create:
        cursor.execute(row)


def insert_defaults_sensors(cursor):
    insert_defaults = [
        "insert into Sensor (Id, Name) values(8,'Garaget')",
        "insert into Sensor (Id, Name) values(169,'Vinden')",
        "insert into Sensor (Id, Name) values(206,'Skateboardrummet')"
    ]
    for row in insert_defaults:
        cursor.execute(row)

def drop_and_create_switch(cursor):
    drop_and_create = [
        "drop table if exists Switch",
        "create table Switch(Id integer primary key, Name text, State boolean)"
    ]

    for row in drop_and_create:
        cursor.execute(row)


def insert_defaults_switch(cursor):
    insert_defaults = [
        "insert into Switch (Id, Name, State) values(1,'Uterum', 0)",
        "insert into Switch (Id, Name, State) values(2,'Bilen', 0)",
        "insert into Switch (Id, Name, State) values(3,'Vardagsrum', 0)",
        "insert into Switch (Id, Name, State) values(4,'Hallen', 0)",
        "insert into Switch (Id, Name, State) values(5,'Skateboardrum', 0)"
    ]
    for row in insert_defaults:
        cursor.execute(row)
        
def switches(cursor, con):
	drop_and_create_switch(cursor)
	con.commit()
	insert_defaults_switch(cursor)
	con.commit()

def sensors(cursor, con):
	drop_and_create_sensors(cursor)
	con.commit()
	insert_defaults_sensors(cursor)
	con.commit()
 

if __name__ == "__main__":
    con = sqlite3.connect("elctrl.db")
    cursor = con.cursor()
    #sensors(cursor, con)
    switches(cursor, con)
    cursor.execute("select * from Sensor")
    for row in cursor:
        print row
    #cursor.execute("select * from SensorData")
    #for row in cursor:
    #    print row
    
    cursor.execute("select * from Switch")
    for row in cursor:
		print row
