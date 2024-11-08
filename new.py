import cv2
import matplotlib.pyplot as plt
import emoji
import time

def count_vehicles(image_path):
    # Load YOLO
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    # Get output layer names
    layer_names = net.getUnconnectedOutLayersNames()

    # Load image
    img = cv2.imread(image_path)
    height, width, channels = img.shape

    # Define region of interest (ROI)
    roi_x, roi_y, roi_w, roi_h = 0, 0, 800, 400  # Adjust these values based on your lane
    roi = img[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

    # Detecting objects within the ROI
    blob = cv2.dnn.blobFromImage(roi, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)

    # Information to extract
    class_ids = []
    confidences = []
    boxes = []

    # Mapping of class IDs to class labels
    class_labels = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light",
                    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
                    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
                    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
                    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
                    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
                    "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard",
                    "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
                    "scissors", "teddy bear", "hair drier", "toothbrush","ambulance"]

    # Iterate over detected objects within the ROI
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = scores.argmax()
            confidence = scores[class_id]
            if confidence > 0.5:  # Confidence threshold
                # Object detected
                center_x = int(detection[0] * roi_w)
                center_y = int(detection[1] * roi_h)
                w = int(detection[2] * roi_w)
                h = int(detection[3] * roi_h)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Convert ROI coordinates to full image coordinates
                x += roi_x
                y += roi_y

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-maximum suppression to remove redundant boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes and count vehicles
    num_vehicles = 0
    for i in range(len(boxes)):
        if i in indexes:
            num_vehicles += 1

    return num_vehicles

# List of image paths
image_paths = ["/Users/yogendrareddy/no1.webp", "/Users/yogendrareddy/no2.jpeg", "/Users/yogendrareddy/no3.jpeg", "/Users/yogendrareddy/no4.jpeg"]

# Count vehicles for each image
vehicle_counts = [count_vehicles(image_path) for image_path in image_paths]

# Find the image with the greatest number of vehicles
max_vehicles_index = vehicle_counts.index(max(vehicle_counts))

# Display the image with the most vehicles
max_vehicles_image = cv2.imread(image_paths[max_vehicles_index])
plt.imshow(cv2.cvtColor(max_vehicles_image, cv2.COLOR_BGR2RGB))
plt.show()

# Print the results
print("Number of vehicles for each image:", vehicle_counts)
print("Image with the most vehicles:", image_paths[max_vehicles_index])
print("Number of vehicles in the specified lane is", max(vehicle_counts))


def print_traffic_signal(lanes):
    # Find the index of the lane with the highest number
    max_index = vehicle_counts.index(max(vehicle_counts))
    gray_circle = '\u26AA'
    # Define the emojis for traffic signals
    green_light = emoji.emojize(':green_circle:')
    yellow_light = emoji.emojize(':yellow_circle:')
    gray_light = emoji.emojize(gray_circle)
    red_light = emoji.emojize(':red_circle:')
    print(f"Lane 1         Lane 2       Lane 3        Lane 4")
    # Print the lanes with traffic signals
    for i, lane in enumerate(vehicle_counts):
        
        if i == max_index:
            print(f" {gray_light} {gray_light} {green_light}     ", end="")
        else:
            print(f" {red_light} {gray_light} {gray_light}      ", end="")
    print()
    print(f"The lane {max_index+1} is now open for 60 seconds")
    time.sleep(30)
    print(f"Lane {max_index+1} is now about to be closed, checking all lanes once again!")
    for i, lane in enumerate(vehicle_counts):
        
        if i == max_index:
            print(f" {gray_light} {yellow_light} {gray_light}     ", end="")
        else:
            print(f" {red_light} {gray_light} {gray_light}      ", end="")
    print()
# Example usage

print("-" * 80)
print_traffic_signal(lanes)
print("-" * 80)
