import sqlite3


if __name__ == "__main__":
    con = sqlite3.connect("elctrl.db")
    cursor = con.cursor()

    cursor.execute("select * from Sensor")
    for row in cursor:
        print row

    latestValuesQuery = """ select 
			s.Id, s.Name, sd.Temperature, sd.Humidity, sd.Time  
		from 
			SensorData as sd 
		inner join 
			Sensor s 
		on 
			sd.SensorId=s.Id 
		order by 
			sd.Time desc 
		limit 12"""
		
		
    latest_values = """
		select 
			s.Name, sd.SensorId, sd.Temperature, sd.Humidity, max(sd.Time) as Time
		from 
			SensorData as sd
		inner join 
			Sensor s
		on 
			sd.SensorId = s.Id
		group by 
			sd.SensorId
		"""
    latestValuesQuery2 = """
		select 
			s.Name, sd.SensorId, sd.Temperature, sd.Humidity, max(sd.Time)  
		from 
			SensorData as sd
		inner join 
			Sensor s
		on 
			sd.SensorId = s.Id
		group by 
			sd.SensorId
		"""

    cursor.execute(latest_values)
    print cursor.rowcount
    for row in cursor:
        print row

    #cursor.execute("")
    con.close()
