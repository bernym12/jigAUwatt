from quart import Quart, render_template, request
# from flask_wtf import FlaskForm
# from wtforms import RadioField
from app import app
import asyncio
from tasmota_device_controller.tasmotadevicecontroller import TasmotaDevice
from tasmota_device_controller.tasmotadevicecontroller import tasmota_types as t

app = Quart(__name__)

@app.route('/', methods=['GET', 'POST'])
async def index(states=list,states_to_str=str):
    # file1 = open("onoff.txt", "r+")

    if request.method == 'POST':
        # states: object = await request.form.getlist('1b_submit_button')
        device = await TasmotaDevice.connect('192.168.1.60')
        setResult = await device.setPower(t.PowerType.TOGGLE, output=t.FriendlyNameOutputType.OUTPUT_2)

        print(states)
        # do stuff here to send command to shelly once toggle button is pressed
        return await render_template('index.html')
    
    # device = await TasmotaDevice.connect()



    return await render_template('index.html')

# async def main():

#     # Get friendly name (of first output, which is the default output)
#     nameResult = await device.getFriendlyName(ouput=t.FriendlyNameOutputType.OUTPUT_2)
#     print(nameResult)  # Returns 'My Tasmota Plug'

#     # Get power of first output
#     getResult = await device.getPower()
#     print(getResult)  # Returns True (on)

    # Set power of first output to on
    # print(setResult)  # Returns True or False (depending if the device was switched on or off)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
