all_values = """
		select 
			s.Id, s.Name, sd.Temperature, sd.Humidity, sd.Time 
		from 
			SensorData as sd 
		inner join 
			Sensor s 
		on 
			sd.SensorId=s.Id
"""


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
switches = """
		select 
			Id, Name, State
		from
			Switch
		"""
switches_set_state = """
		update 
			Switch
		set
			State=?
		where
			Id=?
		"""

