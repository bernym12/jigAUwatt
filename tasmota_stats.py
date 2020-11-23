import asyncio
from app.tasmota_device_controller.tasmotadevicecontroller import TasmotaDevice
from app.tasmota_device_controller.tasmotadevicecontroller import tasmota_types as t

async def main():
    device = await TasmotaDevice.connect('192.168.1.6')

    # Get friendly name (of first output, which is the default output)
    nameResult = await device.getFriendlyName(output=t.FriendlyNameOutputType.OUTPUT_2)
    # print(nameResult)  # Returns 'My Tasmota Plug'

    # Get power of first output
#    getResult = await device.getPower()\
#    print(getResult)  # Returns True (on)

    # Set power of first output to on
    # setResult = await device.setPower(t.PowerType.TOGGLE, output=t.FriendlyNameOutputType.OUTPUT_2)
    # print(setResult)  # Returns True or False (depending if the device was switched on or off)
    data = (await device.getStatus(statusType = t.StatusType.CONNECTED_SENSOR))['StatusSNS']['ENERGY']['Power']
    for i,item in enumerate(data):
        print(f"Outlet {i+1}: {item} Watts")
    # print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
