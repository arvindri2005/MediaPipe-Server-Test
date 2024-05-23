def detectU(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    little_tip = landmarks[20]

    # Check if middle, ring, or little finger is above thumb or index finger
    if middle_tip['y'] < thumb_tip['y'] or middle_tip['y'] < index_tip['y'] or \
       ring_tip['y'] < thumb_tip['y'] or ring_tip['y'] < index_tip['y'] or \
       little_tip['y'] < thumb_tip['y'] or little_tip['y'] < index_tip['y']:
        return "Not U"
    else:
        return "U"