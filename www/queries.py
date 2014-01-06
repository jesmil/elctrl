"""
    SQL-queries
"""

SENSOR_VALUES_ALL = """
        select
            s.Id, s.Name, sd.Temperature, sd.Humidity, sd.Time
        from
            SensorData as sd
        inner join
            Sensor s
        on
            sd.SensorId=s.Id
"""

SENSOR_VALUES_LATEST = """
        select
            s.Name,
            sd.SensorId,
            sd.Temperature,
            sd.Humidity,
            max(sd.Time) as Time
        from
            SensorData as sd
        inner join
            Sensor s
        on
            sd.SensorId = s.Id
        group by
            sd.SensorId
        """

SWITCHES_ALL = """
        select
            Id, Name, State
        from
            Switch
        """

SWITCHES_SET_STATE = """
        update
            Switch
        set
            State=?
        where
            Id=?
        """
