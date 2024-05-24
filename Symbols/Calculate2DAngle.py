import numpy as np

def calculate_2d_angle(point1, point2, point3, point4, h, w):
    # Convert Mediapipe landmarks to numpy arrays (2D)
    p1 = np.array([point1['x'] * w, point1['y'] * h])
    p2 = np.array([(point2['x'] * w + point4['x'] * w) / 2, (point2['y'] * h + point4['y'] * h) / 2])
    p3 = np.array([point3['x'] * w, point3['y'] * h])
    
    # Calculate vectors
    vec1 = p1 - p2
    vec2 = p3 - p2
    
    # Calculate the angle between vectors
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if norm_product == 0:  # Prevent division by zero
        return 0
    cosine_angle = np.dot(vec1, vec2) / norm_product
    angle = np.arccos(cosine_angle)
    
    # Convert angle from radians to degrees
    angle_degrees = np.degrees(angle)
    return angle_degrees
