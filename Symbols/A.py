import math

# Function to calculate the distance between two landmarks
def calculate_distance(landmark1, landmark2):
    return math.sqrt((landmark1['x'] - landmark2['x'])**2 + (landmark1['y'] - landmark2['y'])**2)

# Function to check if all fingers except the thumb are closed
def fingers_closed(landmarks, threshold=0.1):
    finger_tips = [landmarks[i] for i in [8, 12, 16, 20]]  # Tips of index, middle, ring, and pinky fingers
    finger_mcp = [landmarks[i] for i in [5, 9, 13, 17]]    # MCP joints of index, middle, ring, and pinky fingers

    return all(calculate_distance(tip, mcp) < threshold for tip, mcp in zip(finger_tips, finger_mcp))

# Function to classify the "A" gesture
def classifyAgesture(landmarks1, landmarks2, height, width):
    thumb_tip_1 = landmarks1[4]
    thumb_tip_2 = landmarks2[4]

    # Calculate distance between the thumb tips of both hands
    distance_threshold = 0.15  # Adjust this threshold as needed
    distance = calculate_distance(thumb_tip_1, thumb_tip_2)

    # Check if the thumb tips of both hands are touching and all other fingers are closed
    if distance < distance_threshold and fingers_closed(landmarks1) and fingers_closed(landmarks2):
        return "A", height, width
    return "Not A", height, width