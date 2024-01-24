import cv2
import numpy as np
import os



# Load YOLO for motorbike and number plate detection
net_motorbike = cv2.dnn.readNet("yolov3-custom_7000.weights", "yolov3-custom1.cfg")


# Load YOLO for helmet detection
net_helmet = cv2.dnn.readNet("yolov3_custom_4000.weights", "yolov3_custom.cfg")


# Load classes for both models
with open("motorbike_number_plate.names", "r") as f:
    motorbike_classes = f.read().strip().split('\n')
layer_names = net_motorbike.getLayerNames()
output_layers = [layer_names[i - 1] for i in net_motorbike.getUnconnectedOutLayers()]

with open("helmet.names", "r") as f:
    helmet_classes = f.read().strip().split('\n')
layer_names_helmet = net_helmet.getLayerNames()
output_layers_helmet = [layer_names_helmet[i - 1] for i in net_helmet.getUnconnectedOutLayers()]

cap = cv2.VideoCapture('video.MOV')

# Create a directory to save license plate images
if not os.path.exists('license_plate_images'):
    os.mkdir('license_plate_images')

save_license_plate = False  # Flag to control license plate saving
license_plate_counter=1
# Create a dictionary to store information about each tracked motorbike
tracked_motorbikes = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # motorbike and number plate detection
    height, width, channels = frame.shape
    blob_motorbike = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net_motorbike.setInput(blob_motorbike)
    outs_motorbike = net_motorbike.forward(output_layers)

    # Helmet detection
    height_helmet, width_helmet, channels = frame.shape
    blob_helmet = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net_helmet.setInput(blob_helmet)
    outs_helmet = net_helmet.forward(output_layers_helmet)

    # Information to display on the frame
    motorbike_boxes = []
    motorbike_class_ids = []
    helmet_class_ids = []
    motorbike_confidences = []
    helmet_boxes = []
    helmet_confidences = []

    for out in outs_motorbike:
        for detection in out:
            scores = detection[5:]
            motorbike_class_id = np.argmax(scores)
            confidence = scores[motorbike_class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                motorbike_boxes.append([x, y, w, h])
                motorbike_confidences.append(float(confidence))
                motorbike_class_ids.append(motorbike_class_id)
                
    indexes = cv2.dnn.NMSBoxes(motorbike_boxes, motorbike_confidences, 0.5, 0.4)

    # Reset the flag to False at the beginning of each frame
    save_license_plate = False

    for out in outs_helmet:
        for detection in out:
            scores = detection[5:]
            helmet_class_id = np.argmax(scores)
            confidence = scores[helmet_class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * width_helmet)
                center_y = int(detection[1] * height_helmet)
                w = int(detection[2] * width_helmet)
                h = int(detection[3] * height_helmet)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                helmet_boxes.append([x, y, w, h])
                helmet_confidences.append(float(confidence))
                helmet_class_ids.append(helmet_class_id)

                if helmet_classes[helmet_class_id] != "helmet":
                   save_license_plate = True  # Set the flag to True when helmet is absent

    indexes_helmet = cv2.dnn.NMSBoxes(helmet_boxes, helmet_confidences, 0.5, 0.4)
 
    # Draw bounding boxes for motorbikes, number plates, and helmets
    for i in range(len(motorbike_boxes)):
        if i in indexes:
            x, y, w, h = motorbike_boxes[i]
            label = str(motorbike_classes[motorbike_class_ids[i]])

            # Customize this section to identify "motorbike" and "number plate" classes
            if label == "motorbike":
                color = (0, 255, 0)  # Green for motorbike
                # Check if this motorbike was already tracked
                motorbike_id = -1
                for tracked_id, tracked_info in tracked_motorbikes.items():
                    last_x, last_y, last_w, last_h = tracked_info['last_position']
                    # You may need to adjust this condition based on your specific case
                    if abs(x - last_x) < 80 and abs(y - last_y) < 80:
                        motorbike_id = tracked_id
                        break

                if motorbike_id == -1:
                    # This is a new motorbike, assign a new ID
                    motorbike_id = len(tracked_motorbikes) + 1
                    tracked_motorbikes[motorbike_id] = {'last_position': (x, y, w, h), 'license_plate_saved': False}   
                
                else:
                    # This motorbike was already tracked, update its position
                    tracked_motorbikes[motorbike_id]['last_position'] = (x, y, w, h)

            else:
                color = (0, 0, 255)  # Red for license plate

                # Check if the license plate needs to be saved for this motorbike
                if label == "license_plate"and save_license_plate and not tracked_motorbikes[motorbike_id]['license_plate_saved']:
                    # Crop the region of the number plate
                    number_plate_region = frame[y:y + h, x:x + w]
                    filename = f'license_plate_images/license_plate_{license_plate_counter}.jpg'
                    cv2.imwrite(filename, number_plate_region)
                    license_plate_counter+=1
                    tracked_motorbikes[motorbike_id]['license_plate_saved'] = True


            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    for k in range(len(helmet_boxes)):
        if k in indexes_helmet:
            x, y, w, h = helmet_boxes[k]
            label = str(helmet_classes[helmet_class_ids[k]])

            # Customize this section to identify "helmet" and "no_helmet" classes
            if label == "helmet":
                color = (0, 255, 0)  # Green for helmet
            else:
                color = (0, 0, 255)  # Red for no helmet

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Perform motorbike, number plate, and helmet detection

    cv2.imshow("Motorbike and Helmet Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()