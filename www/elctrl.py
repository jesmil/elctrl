#!/usr/bin/env python

from bottle import request
import bottle
import bottle.ext.sqlite
import queries
import subprocess

app = bottle.default_app()
app.config.load_config("/home/jesmil/documents/elctrl/www/elctrl.conf")

plugin = bottle.ext.sqlite.Plugin(dbfile=app.config['db.file'])
app.install(plugin)


@app.route("/elctrl")
def elctrl():
	return static("elctrl.html")

@app.route("/sensors/<id>", method="GET")
def sensors_id_get(id, db):
    sensors = {}
    cursor = db.cursor()
    cursor.execute(queries.all_values)
    for row in cursor:
        name = row["Id"]
        if not sensors.has_key(name):
            sensors[row["Id"]] = {"Name": row["Name"], "Data": []}
        sensors[row["Id"]]["Data"].append([row["Temperature"], row["Humidity"], row["Time"]])
    return sensors

@app.route("/sensors", method="GET")
def sensors_get(db):
    sensors = {}
    cursor = db.cursor()
    cursor.execute(queries.latest_values)
    for row in cursor:
        sensor_id = row["SensorId"]
        if not sensors.has_key(sensor_id):
            sensors[sensor_id] = {"Name": row["Name"], "Data": []}
        sensors[sensor_id]["Data"].append({"Temperature": row["Temperature"], "Humidity": row["Humidity"], "Time": row["Time"]})
    
    return sensors


@app.route("/switches", method="GET")
def switches_get(db):
    switches = {}
    cursor = db.cursor()
    cursor.execute(queries.switches)
    for row in cursor:
        switch_id = row["Id"]
        switches[switch_id] = {"Name": row["Name"], "State":row["State"]}
        
    return switches

@app.route("/switches/<id>/state", method="POST")
def switches_state_post(id, db):
	if not request.json.has_key("state"):
		return {}
	state = request.json["state"]
	if app.config['environment.tdtool'] == "1":
		tdtool(id, state)
	cursor = db.cursor()
	cursor.execute(queries.switches_set_state, (state, id))
	db.commit()
	
	return {"Id": id, "State": state}



@app.route("/static/:path#.+#", name="static")
def static(path):
	return bottle.static_file(path, root=app.config['host.wwwroot'] + "static")

def tdtool(id, state):
	args = []
	if state == 0:
		args = "--off"
	else:
		args = "--on"
	p = subprocess.Popen(["tdtool", args, id])

app.run(host=app.config['host.ip'], port=app.config['host.port'], reloader=True)
