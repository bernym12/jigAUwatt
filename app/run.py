import quart.flask_patch
from quart import Quart, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from quart import current_app, g, flash
# from flask_wtf import FlaskForm
# from wtforms import RadioField
from bs4 import BeautifulSoup
from flask_caching import Cache
import click
from app import app
import asyncio
from tasmota_device_controller.tasmotadevicecontroller import TasmotaDevice
from tasmota_device_controller.tasmotadevicecontroller import tasmota_types as t
from pathlib import Path
import sqlite3 as sql
from sqlite3 import IntegrityError
from datetime import datetime
# db_name = 'ip.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['DEBUG'] = True
# this variable, db, will be used for all SQLAlchemy commands
# db = SQLAlchemy(app)
cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Quart(__name__)
cache.init_app(app)



@app.route('/', methods=['GET', 'POST'])
async def index():
    return await render_template('index.html', result=None)


@app.route('/ip', methods=['GET', 'POST'])
async def toggle(cmd=None):
    if request.method == 'POST':
        cmd = '192.168.1.6_bottom'
        if('_') in cmd:
            ip, switch = cmd.split('_')
        else:
            return  redirect(url_for('add_ip'))
        device = await TasmotaDevice.connect(ip)
        if switch == 'top':
            setResult = await device.setPower(t.PowerType.TOGGLE, output=t.FriendlyNameOutputType.OUTPUT_1)
        else:
            setResult = await device.setPower(t.PowerType.TOGGLE, output=t.FriendlyNameOutputType.OUTPUT_2)
        print(setResult)
    con = sql.connect("app/database.db")
    cur = con.cursor()
    cur.execute("select ip from ips")
    rows = cur.fetchall()
    con.close()
    print(rows)
    rows = [val[0] for val in rows]
    return await render_template('index.html', result=rows)

@app.route('/add_ip', methods=['GET','POST'])
async def add_ip():
    if request.method == 'POST':
        # try:
        data = await (request.form)
        ip = data['ip']
        print(ip)
        # device = await TasmotaDevice.connect(ip)
        if data is not None:
            try:
                device = await TasmotaDevice.connect(ip)
                with sql.connect('app/database.db') as con:
                    cur = con.cursor()
                    cur.execute(f"INSERT INTO ips (ip) VALUES (?)", (ip,))
                    con.commit()
                    print("Added to database")
            except IntegrityError:
                print("IP already in database")
            except ConnectionError:
                print("Can't Locate Tasmota")
    con = sql.connect("app/database.db")
    cur = con.cursor()
    cur.execute("select ip from ips")
    rows = cur.fetchall()
    con.close()
    print(rows)
    rows = [val[0] for val in rows]
    return await render_template('index.html', result=rows)

@app.route('/update_graphs', methods=['GET', 'POST'])
async def update_graphs():
    device = await TasmotaDevice.connect(ip)
    data = (await device.getStatus(statusType = t.StatusType.CONNECTED_SENSOR))['StatusSNS']['ENERGY']['Power']


        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
