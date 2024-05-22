import asyncio
import websockets
import math
import json

async def echo(websocket):
    async for data in websocket:
        if data:  # check if data is not empty
            try:
                original_data = json.loads(data)
                print(classify_o_gesture(original_data))
                await websocket.send(classify_o_gesture(original_data))
            except json.JSONDecodeError:
                print("Received data is not a valid JSON string")

async def main():
    async with websockets.serve(echo, "localhost", 8000):
        await asyncio.Future()  # run forever

async def send_message():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, Server!")


def classify_o_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    # Calculate distances between thumb and other fingers
    distance_threshold = 0.1  # Adjust this threshold based on your preference
    distances = [
        calculate_distance(thumb_tip, index_tip),
        calculate_distance(thumb_tip, middle_tip),
        calculate_distance(thumb_tip, ring_tip),
        calculate_distance(thumb_tip, pinky_tip)
    ]
    
    # Check if all fingers are touching the thumb
    if all(distance < distance_threshold for distance in distances):
        return "O"
    
    return "Not O"

def classify_c_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    thumb_mcp = landmarks[1]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]

    # Calculate distances from the tips to the MCP joints
    distance_threshold = 0.05  # Adjust this threshold as needed
    thumb_open = calculate_distance(thumb_tip, thumb_mcp) > distance_threshold
    index_open = calculate_distance(index_tip, index_mcp) > distance_threshold
    middle_open = calculate_distance(middle_tip, middle_mcp) > distance_threshold
    ring_open = calculate_distance(ring_tip, ring_mcp) > distance_threshold
    pinky_open = calculate_distance(pinky_tip, pinky_mcp) > distance_threshold

    # Check if all fingers and thumb are open
    if thumb_open and index_open and middle_open and ring_open and pinky_open:
        return "C"
    return "Not C"


def calculate_distance(landmark1, landmark2):
    return math.sqrt((landmark1['x'] - landmark2['x'])**2 + (landmark1['y'] - landmark2['y'])**2)

asyncio.run(main())