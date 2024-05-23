import asyncio
import websockets
import math
import json
from Symbols.U import detectU

async def echo(websocket):
    async for data in websocket:
        if data:  # check if data is not empty
            try:
                original_data = json.loads(data)
                instruction = original_data.get('instructions', None)
                landmarks = original_data.get('landmarks', None)
                print(instruction)
                print(landmarks)
                # Define a dictionary to act as a switch-case
                switch = {
                    'U': detectU,
                    # Add more instructions as needed
                }

                # Get the function from switch dictionary with the instruction as key
                func = switch.get(instruction, None)
                if func:
                    # Call the function
                     await websocket.send(func(landmarks))
                else:
                    print(f"Unknown instruction: {instruction}")
            except json.JSONDecodeError:
                print("Received data is not a valid JSON string")
            

async def main():
    async with websockets.serve(echo, "localhost", 8000):
        await asyncio.Future()  # run forever

async def send_message():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, Server!")

asyncio.run(main())