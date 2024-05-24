import asyncio
import websockets
import math
import json
from Symbols.U import classify_u_gesture
from Symbols.A import classifyAgesture

async def echo(websocket):
    async for data in websocket:
        if data:  # check if data is not empty
            try:

                #Geeting data send from socket
                originalData = json.loads(data)
                
                instruction = originalData.get('instructions', None)
                rightLandmarks = originalData.get('rightlandmarks', None)
                leftLandmarks = originalData.get('leftlandmarks', None)
                height = originalData.get('height', None)
                width = originalData.get('width', None)

                # Define a dictionary to act as a switch-case
                switch = {
                    'A': classifyAgesture,
                    'U': classify_u_gesture,
                    # Add more instructions as needed
                }

                # Get the function from switch dictionary with the instruction as key
                CheckAccuracy = switch.get(instruction, None)

                if CheckAccuracy:

                    # Call the function
                    gesture, accuracy, correct = CheckAccuracy(rightLandmarks,leftLandmarks, height, width)

                    # Send the response back to the client
                    response = {
                        'gesture': gesture,
                        'accuracy': accuracy,
                        'correct': correct
                    }
                    await websocket.send(json.dumps(response))

                else:
                    #Sign yet to implement
                    print(f"Unknown instruction: {instruction}")

            #Recived Data is invalid       
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