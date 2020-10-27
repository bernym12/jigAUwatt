import asyncio
from tasmotadevicecontroller import TasmotaDevice
from tasmotadevicecontroller import tasmota_types as t

async def main():
    device = await TasmotaDevice.connect('192.168.43.139')

    # Get friendly name (of first output, which is the default output)
    nameResult = await device.getFriendlyName(ouput=t.FriendlyNameOutputType.OUTPUT_2)
    print(nameResult)  # Returns 'My Tasmota Plug'

    # Get power of first output
    getResult = await device.getPower()
    print(getResult)  # Returns True (on)

    # Set power of first output to on
    setResult = await device.setPower(t.PowerType.OFF, output=t.FriendlyNameOutputType.OUTPUT_2)
    print(setResult)  # Returns True or False (depending if the device was switched on or off)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())