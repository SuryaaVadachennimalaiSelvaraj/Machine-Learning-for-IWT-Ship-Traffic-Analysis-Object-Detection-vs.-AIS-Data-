import cv2
import numpy as np
import torch
import json
import pandas as pd
import sys
import datetime

# Get JSON file in argument of the script
json_file = sys.argv[1]
video_file = sys.argv[2]
start_time = sys.argv[3]

# Initialize a dictionary that saves previous ship's centroids, Direction and counted status
previous_ships = []

def calculate_centroid(box):
    x1, y1, x2, y2 = box
    centroid_x = (x1 + x2) / 2    
    centroid_y = (y1 + y2) / 2
    return (centroid_x, centroid_y)

def calculate_distance(centroid1, centroid2):
    x1, y1 = centroid1
    x2, y2 = centroid2
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


# Load YOLO and import my weights
model = torch.hub.load('ultralytics/yolov5', 'custom', path="C:/Users/surya/yolov5/best.pt")    

# Load video
cap = cv2.VideoCapture(video_file)

# Set minimum confidence threshold for detections
conf_thresh = 0.75

# Reference line for counting for right to left direction
ref_line = 1000

# Define centroid distance threshold for ship matching
centroid_distance_threshold = 25

#initialize a parameter for the number of frames to skip
skip_frames = 20

#Initialize counts
left_to_right_count = 0
right_to_left_count = 0

#Initialize frame count
count_frames = 0
#print total number of frames in the video
print("Total number of frames: " + str(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

FPS = cap.get(cv2.CAP_PROP_FPS)

while True:
    # Read frame from video
    ret, frame = cap.read()
   
    # Stop if end of video or if its a blank frame
    if frame is None:
        break

    # Count the frame number
    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    # process every other frame
    if frame_number % skip_frames != 0:
        continue
        
    # Count the frames that are processed
    count_frames = count_frames + 1

    # Pass frame through YOLOv5s model
    detections = model(frame)

    # get detections with confidence higher than conf_thresh
    detections = detections.pred[0][detections.pred[0][:, 4] > conf_thresh]

    # loop through detections 
    for detection in detections:
        # get confidence score and class index
        confidence = detection[4]
        class_index = int(detection[5])

        # chech if the confidence is higher than the threshold
        if confidence > conf_thresh:
            # get bounding box coordinates 
            x1, y1, x2, y2 = detection[:4].detach().numpy().astype(np.int32)

            #centroid of the bounding box
            centroid_x,centroid_y = calculate_centroid((x1, y1, x2, y2))

            # Check if the current centroid is near any previous centroid only then consider it as the same ship
            matched_ship = None
            previous_centroid = None
            for ship in previous_ships:
                previous_centroid = ship["centroid"]
                if isinstance(previous_centroid, np.ndarray):
                    for centroid in previous_centroid:
                        distance = calculate_distance(centroid, (centroid_x, centroid_y))
                        if distance < centroid_distance_threshold:
                            previous_centroid = centroid
                            matched_ship = ship
                            break
                else:
                    distance = calculate_distance(previous_centroid, (centroid_x, centroid_y))
                    if distance < centroid_distance_threshold:
                        matched_ship = ship
                        break                    
            
            # Also check if direction is not assigned and save the direction based on the previous centroid centre point, even if the difference is small
            if matched_ship is not None and matched_ship["direction"] is None:
                prev_centroid_x, prev_centroid_y = previous_centroid
                # print("Previous centroid: " + str(previous_centroid) + "\n")
                if centroid_x > prev_centroid_x and centroid_y > prev_centroid_y:
                    matched_ship["direction"] = "Left to Right"
                    print("Direction assigned: Left to Right for " + str(matched_ship) + "\n")
                    #print co-ordinates of the ship
                    # print("Ship co-ordinates: " + str((x1, y1, x2, y2)) + "\n")
                    
                elif centroid_x < prev_centroid_x and centroid_y < prev_centroid_y:
                    matched_ship["direction"] = "Right to Left"
                    print("Direction assigned: Right to Left for " + str(matched_ship) + "\n")
                    # print("Ship co-ordinates: " + str((x1, y1, x2, y2)) + "\n")
                   
            # Update the centroid of the matched ship if its relatively close to the previous centroid
            if matched_ship is not None:
                if isinstance(previous_centroid, np.ndarray):
                    for centroid in previous_centroid:
                        if calculate_distance(centroid, (centroid_x, centroid_y)) < centroid_distance_threshold:
                            matched_ship["centroid"] = (centroid_x, centroid_y)
                            break
                else:
                    matched_ship["centroid"] = (centroid_x, centroid_y)
            
            # If no match found, create a new ship 
            if matched_ship is None:
                matched_ship = {"centroid": (centroid_x, centroid_y), "direction": None, "counted": False}
                # Print values of the new ship
                print("New ship found: " + str(matched_ship) + "+++++++++++++\n")
                previous_ships.append(matched_ship)

          #Check if the box border is crossing the line and cross check with the direction of the ship
            if matched_ship["direction"] == "Right to Left" and x1 < ref_line and not matched_ship["counted"]:
                # print values of the matched ship
                right_to_left_count += 1
                # print("Coordinates of the matched ship: " + str((x1, y1, x2, y2)) + "\n")
                matched_ship["counted"] = True
                print("Ship crossed the line from Right to Left: " + str(matched_ship) + "\n\n")
                # Also based on FPS and current frame number, note the time of crossing the line
                match_time = (frame_number / cap.get(cv2.CAP_PROP_FPS))
                matched_ship["counted_frame"] = frame_number
                # print("Time of crossing the line: " + str(match_time) + " seconds\n")
                matched_ship["time"] = match_time

                print("Ship crossed the line from Left to Right: " + str(matched_ship) + "\n\n")

            elif matched_ship["direction"] == "Left to Right" and x2 > ref_line and not matched_ship["counted"]:
                # print values of the matched ship
                left_to_right_count += 1
                #print coordinates of the matched ship in the frame
                # print("Coordinates of the matched ship: " + str((x1, y1, x2, y2)) + "\n")
                matched_ship["counted"] = True
                # Also based on FPS and current frame number, note the time of crossing the line
                match_time = (frame_number / cap.get(cv2.CAP_PROP_FPS))
                matched_ship["counted_frame"] = frame_number
                # print("Time of crossing the line: " + str(match_time) + " seconds\n")
                matched_ship["time"] = match_time

                print("Ship crossed the line from Left to Right: " + str(matched_ship) + "\n\n")
                           

            # Draw bounding box to fit the detected object
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw centroids for ships
            cv2.circle(frame, (int(centroid_x), int(centroid_y)), 5, (0, 255, 0), -1)
    
    # Draw reference line for counting
    cv2.line(frame, (ref_line, 0), (ref_line, 720), (0, 0, 255), 2)
    
    # Display counts on frame
    cv2.putText(frame, "Left to Right: " + str(left_to_right_count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, "Right to Left: " + str(right_to_left_count), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Display frame
    cv2.imshow("YOLOv5", frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

# Print counts
print("Left to Right: " + str(left_to_right_count))
print("Right to Left: " + str(right_to_left_count))
print("Total number of frames: " + str(count_frames) + "\n\n")

# Print total number of ships which is the sum of left to right and right to left
print("Total number of ships: " + str(left_to_right_count + right_to_left_count) + "\n\n")


# based on the start time of the video, calculate the time of crossing the line for each ship
start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
for ship in previous_ships:
    if ship["counted"]:
        # Find the time of crossing the line and save as string in the ship dictionary in format YYYY-MM-DD HH:MM:SS
        time_of_crossing = start_time + datetime.timedelta(seconds=ship["time"])
        ship["time"] = time_of_crossing.strftime("%Y-%m-%d %H:%M:%S")
        print(ship)

# Load JSON file
with open(json_file) as f:
    json_data = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(json_data)

# Convert timestamp to datetime
df['timeLastUpdate'] = pd.to_datetime(df['timeLastUpdate'], unit='ms')

# Sort DataFrame by timestamp in ascending order
df = df.sort_values('timeLastUpdate')

# add a column to the DataFrame to save the matched ship(yes/no)
df["Matched ship"] = ""

# create a column to the dataframe to save the number of matches per range or timestamp
df["Number of matches"] = ""
# assign 0 to all the entries in the column
df["Number of matches"] = 0
# make the varable type as int
df["Number of matches"] = df["Number of matches"].astype(int)


# add a column to save the timelasupdate as a range of values
df["'timeLastUpdate': ['first', 'last']"] = ""

# if multiple entries with the same mmsi, keep one entry with the timestamp value being the range of the first and last timestamp, enter this value in the new column
# After a range is obtained for a ship, delete all other entries with the same mmsi
for index, row in df.iterrows():
    if df[df["mmsi"] == row["mmsi"]].shape[0] > 1:
        df.at[index, "'timeLastUpdate': ['first', 'last']"] = {"first": df[df["mmsi"] == row["mmsi"]]["timeLastUpdate"].iloc[0], "last": df[df["mmsi"] == row["mmsi"]]["timeLastUpdate"].iloc[-1]}
        df.drop(df[df["mmsi"] == row["mmsi"]].index[1:], inplace=True)


        
# Try to mach the previous_ships list by comparing the time of crossing the line with the timeLastUpdate
for ship in previous_ships:
    for index, row in df.iterrows():
        if ship["counted"]:
            # convert timeLastUpdate to datetime
            timeLastUpdate = row["timeLastUpdate"]
            # Convert time of crossing the line to datetime
            time_of_crossing = datetime.datetime.strptime(ship["time"], "%Y-%m-%d %H:%M:%S")
            # print("Time of crossing the line: " + str(time_of_crossing) + " Time Last Update  " + str(timeLastUpdate) +   "\n")                       
            # if the time last update is a range of values, check if the time of crossing the line is in that range
            if isinstance(row["'timeLastUpdate': ['first', 'last']"], dict):
                    # if time of crossing the line is in the range of timeLastUpdate, then match the ship
                if time_of_crossing >= row["'timeLastUpdate': ['first', 'last']"]["first"] and time_of_crossing <= row["'timeLastUpdate': ['first', 'last']"]["last"]:
                    df.at[index, "Matched ship"] = "Yes"
                    # increase the number of matches for that range
                    df.at[index, "Number of matches"] = df.at[index, "Number of matches"] + 1
                    print("Matched ship: " + str(ship) + " with " + str(row["mmsi"]) + "\n")
                    break
            # if the time last update is not a range of values, check if the time of crossing the line is within 2 minutes of the timeLastUpdate
            else:
                if time_of_crossing >= timeLastUpdate - datetime.timedelta(minutes=2) and time_of_crossing <= timeLastUpdate + datetime.timedelta(minutes=2):
                    df.at[index, "Matched ship"] = "Yes"
                    # increase the number of matches for that range
                    df.at[index, "Number of matches"] = df.at[index, "Number of matches"] + 1
                    print("Matched ship: " + str(ship) + " with " + str(row["mmsi"]) + "\n")
                    break

# Also print the sum of the number of matches column in the end of the column
print("Total number of matches: " + str(df["Number of matches"].sum()) + "\n\n")

# Save only timeLastUpdate, mmsi column and if the ship is matched to that entry into excel file from the DataFrame and print it to excel and save it in the same folder as the script
df.to_excel("AIS_data.xlsx", columns=["timeLastUpdate","'timeLastUpdate': ['first', 'last']", "mmsi", "Matched ship", "Number of matches"], index=False)

import matplotlib.pyplot as plt
# plot a bargraph of the number of matches per timelasupdate
df.plot.bar(x="mmsi", y="Number of matches", rot=90)
#decrease the size of the label on x axis
plt.xticks(fontsize=5)
#make the label of y axis whole numbers instead of decimals
plt.yticks(np.arange(0, 10, 1))
plt.show()
#save the plot as a png file
plt.savefig("Number of matches per mmsi.png")


