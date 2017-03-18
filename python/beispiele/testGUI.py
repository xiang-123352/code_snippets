import pythrust
import asyncio

loop = asyncio.get_event_loop()
api = pythrust.API(loop)

api.spawn()

window = api.window(args="www.google.de")
window.show()

loop.run_forever()
