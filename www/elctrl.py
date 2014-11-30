#!/usr/bin/env python

"""
elctrl web
"""


from bottle import request
import bottle
import bottle.ext.sqlite
import queries
import subprocess

APP = bottle.default_app()
APP.config.load_config("/home/jesmil/documents/elctrl/www/elctrl.conf")

SQLITE_PLUG = bottle.ext.sqlite.Plugin(
    dbfile=APP.config['db.file'],
    keyword='database')

APP.install(SQLITE_PLUG)


@APP.route("/")
@APP.route("/elctrl")
def elctrl():
    """
        Start page
    """
    return static("elctrl.html")


@APP.route("/sensors/<sensor_id>", method="GET")
def sensors_id_get(sensor_id, database):
    """
        Return sensor by id
    """
    sensors = {}
    cursor = database.cursor()
    cursor.execute(queries.SENSOR_VALUES_ALL)
    for row in cursor:
        name = row["Id"]
        if not name in sensors:
            sensors[row["Id"]] = {"Name": row["Name"], "Data": []}
        sensors[row["Id"]]["Data"].append(
            [row["Temperature"], row["Humidity"], row["Time"]])
    return sensors


@APP.route("/sensors", method="GET")
def sensors_get(database):
    """
        Return all sensors
    """
    sensors = {}
    cursor = database.cursor()
    cursor.execute(queries.SENSOR_VALUES_LATEST)
    for row in cursor:
        sensor_id = row["SensorId"]
        if not sensor_id in sensors:
            sensors[sensor_id] = {"Name": row["Name"], "Data": []}
        sensors[sensor_id]["Data"].append({
            "Temperature": row["Temperature"],
            "Humidity": row["Humidity"],
            "Time": row["Time"]})

    return sensors


@APP.route("/switches", method="GET")
def switches_get(database):
    """
        Return all power switches
    """
    switches = {}
    cursor = database.cursor()
    cursor.execute(queries.SWITCHES_ALL)
    for row in cursor:
        switch_id = row["Id"]
        switches[switch_id] = {"Name": row["Name"], "State": row["State"]}

    return switches


@APP.route("/switches/<switch_id>/state", method="POST")
def switches_state_post(switch_id, database):
    """
        Set state of power swith by id
    """
    if not "state" in request.json:
        return {}
    state = request.json["state"]
    if APP.config['environment.tdtool'] == "1":
        tdtool(switch_id, state)
    cursor = database.cursor()
    cursor.execute(queries.SWITCHES_SET_STATE, (state, switch_id))
    database.commit()

    return {"Id": switch_id, "State": state}


@APP.route("/static/:path#.+#", name="static")
def static(path):
    """
        Return static file
    """
    return bottle.static_file(path, root=APP.config['host.wwwroot'] + "static")


def tdtool(switch_id, state):
    """
        Call tdtool
    """
    args = ""
    if state == 0:
        args = "--off"
    else:
        args = "--on"
    subprocess.Popen(["tdtool", args, switch_id])

APP.run(
    host=APP.config['host.ip'],
    port=APP.config['host.port'],
    reloader=True)
