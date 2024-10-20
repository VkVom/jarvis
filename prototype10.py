import cv2

# Initialize video capture from default camera (0)
cap = cv2.VideoCapture(0)

# Variable to store the initial frame
ret, frame1 = cap.read()
prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

# Loop to continuously capture frames
while True:
    # Read current frame from the camera
    ret, frame2 = cap.read()
    if not ret:
        break
    
    # Convert to grayscale for better motion detection
    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Calculate the absolute difference between current frame and previous frame
    frame_diff = cv2.absdiff(prev_gray, gray)
    
    # Apply a threshold to convert the difference into a binary image
    _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
    
    # Dilate the thresholded image to fill in holes
    dilated = cv2.dilate(thresh, None, iterations=2)
    
    # Find contours of the moving objects
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw rectangles around the moving objects
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the frame with motion tracking
    cv2.imshow('Motion Tracking', frame2)
    
    # Update the previous frame
    prev_gray = gray
    
    # Exit the loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
