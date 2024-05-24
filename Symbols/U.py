from Symbols.Calculate2DAngle import calculate_2d_angle

def classify_u_gesture(landmarks,landmarks2, h, w):

    index_finger_dip = landmarks[7]
    index_finger_mcp = landmarks[5]
    middle_finger_dip = landmarks[11]
    middle_finger_mcp = landmarks[9]
    wrist = landmarks[0]
    index_finger_tip = landmarks[8]
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    thumb_mcp = landmarks[2]
            
    angle_2d = calculate_2d_angle(index_finger_dip, index_finger_mcp, middle_finger_dip, middle_finger_mcp, h, w)
    a1 = calculate_2d_angle(index_finger_tip, index_finger_mcp, wrist, index_finger_mcp, h, w)
    a2 = calculate_2d_angle(thumb_tip, thumb_ip, thumb_mcp, thumb_ip, h, w)
    a3 = calculate_2d_angle(thumb_tip, wrist, index_finger_tip, wrist, h, w)

    index_tip = landmarks[8]
    index_dip = landmarks[7]
    index_mcp = landmarks[5]
    
    middle_tip = landmarks[12]
    middle_dip = landmarks[11]
    middle_mcp = landmarks[9]
    
    ring_tip = landmarks[16]
    ring_dip = landmarks[15]
    ring_mcp = landmarks[13]
    
    pinky_tip = landmarks[20]
    pinky_dip = landmarks[19]
    pinky_mcp = landmarks[17]

    correct = [0]*21
    a = 6
    correct[0] = 1
    correct[1] = 1
    correct[5] = 1
    correct[9] = 1
    correct[13] = 1
    correct[17] = 1
    
    if a1 > 165:
        a = a + 3
        for i in range(6, 9):
            correct[i] = 1
        
    if a2 > 165:
        a = a + 3
        for i in range(2, 5):
            correct[i] = 1
    
    if (middle_mcp['y'] < middle_tip['y']) and (middle_mcp['y'] < middle_dip['y']):
        a = a + 3
        for i in range(10, 13):
            correct[i] = 1
    
    if (ring_mcp['y'] < ring_tip['y']) and (ring_mcp['y'] < ring_dip['y']):
        a = a + 3
        for i in range(14, 17):
            correct[i] = 1
    
    if (pinky_mcp['y'] < pinky_tip['y']) and (pinky_mcp['y'] < pinky_dip['y']):
        a = a + 3
        for i in range(18, 21):
            correct[i] = 1
    
    if (index_dip['y'] < index_tip['y']):
        a = a - 2
        for i in range(6, 9):
            correct[i] = 0
            
    if (a3 < 15) or (a3 > 35):
        a = a - 2
        for i in range(9):
            correct[i] = 0

    a = 0
    for i in range(21):
        a = a + correct[i]
        
    accuracy = (a / 21) * 100
    
    if a == 21:
        return "U", accuracy, correct
    else:
        return "Not U", accuracy, correct