# -*- coding: utf-8 -*-
"""Gait Recognition Pre-Processing (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/164fqI7h-6iCbKU-JxYPAdVTZ00iDVjv_
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install mediapipe opencv-python

import cv2
import mediapipe as mp
import csv
import pandas as pd
import numpy as np
import math

import os
import cv2
import csv
import mediapipe as mp
from pathlib import Path

# Function to extract keypoints and write coordinates to CSV file
def extract_keypoints_and_write_to_csv(frame, mp_pose, keypoint_names, csv_writer):
    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using MediaPipe Pose
    results = mp_pose.process(rgb_frame)

    # Extract and write 3D coordinates to CSV file for named keypoints
    if results.pose_landmarks is not None and len(results.pose_landmarks.landmark) > 0:
        landmarks = []
        for landmark, name in zip(results.pose_landmarks.landmark, keypoint_names):
            x, y, z = landmark.x, landmark.y, landmark.z
            landmarks.extend([x, y, z])
        csv_writer.writerow(landmarks)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Directory containing .avi files
video_directory = '/content/drive/MyDrive/video_90/'

# Create a new folder for saving CSV files
output_folder = '/content/drive/MyDrive/CSV_Output_90/'
Path(output_folder).mkdir(parents=True, exist_ok=True)

# List all .avi files in the directory
video_files = [f for f in os.listdir(video_directory) if f.endswith('.avi')]

for video_file in video_files:
    # Open the video file
    video_path = os.path.join(video_directory, video_file)
    cap = cv2.VideoCapture(video_path)

    # List of keypoint names
    keypoint_names = ["Nose", "Left Eye", "Right Eye", "Left Ear", "Right Ear",
                      "Left Shoulder", "Right Shoulder", "Left Elbow", "Right Elbow",
                      "Left Wrist", "Right Wrist", "Left Hip", "Right Hip",
                      "Left Knee", "Right Knee", "Left Ankle", "Right Ankle"]

    # Create a CSV file for writing
    csv_file_path = os.path.join(output_folder, f'{os.path.splitext(video_file)[0]}.csv')
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write header to CSV file
        header = []
        for name in keypoint_names:
            header += [f"{name}_x"] + [f"{name}_y"] + [f"{name}_z"]
        csv_writer.writerow(header)

        while cap.isOpened():
            # Read a frame from the video
            ret, frame = cap.read()
            if not ret:
                break

            # Extract keypoints and write coordinates to CSV file for named keypoints
            extract_keypoints_and_write_to_csv(frame, pose, keypoint_names, csv_writer)

    # Release the video capture object
    cap.release()

    print(f"Keypoint coordinates for named keypoints in {video_file} have been saved to {csv_file_path}")

import os
import pandas as pd
import numpy as np

# Directory containing .csv files
csv_directory = '/content/drive/MyDrive/CSV_Output_90/'

# List all .csv files in the directory
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

# Initialize an empty list to store DataFrames
dataframes = []

# Iterate through all .csv files and read them into DataFrames
for csv_file in csv_files:
    csv_path = os.path.join(csv_directory, csv_file)
    dataframe = pd.read_csv(csv_path)

    # Labeling based on the first three characters of the CSV file name
    label = int(csv_file[:3].lstrip('0'))
    dataframe['Label'] = label  # Adding a new column 'Label' with the assigned label
    dataframes.append(dataframe)

# Concatenate DataFrames horizontally while keeping column names intact
concatenated_data = pd.concat(dataframes, axis=0)

# Reorder columns with 'Label' as the first column
concatenated_data = concatenated_data[['Label'] + [col for col in concatenated_data.columns if col != 'Label']]

# Convert the concatenated DataFrame to a NumPy array
concatenated_matrix = concatenated_data.to_numpy()

# Save the concatenated matrix as a new CSV file
output_csv_path = '/content/drive/MyDrive/Concatenated_Output_With_Labels.csv'
concatenated_data.to_csv(output_csv_path, index=False)

print(f"The concatenated matrix with labels has been saved as {output_csv_path}")

type(concatenated_data)

concatenated_data.shape

keypoints_data = pd.read_csv('/content/drive/MyDrive/Concatenated_Output_With_Labels.csv')

# Extracting coordinates of neck

neck_x, neck_y, neck_z = [], [], []

# X-Coordinate
for right_values_x in np.array(keypoints_data['Right Shoulder_x']):
  neck_x.append(right_values_x)
for i in range(len(np.array(keypoints_data['Left Shoulder_x']))):
  neck_x[i]+=np.array(keypoints_data['Left Shoulder_x'])[i]
  neck_x[i] = neck_x[i]/2
# print(neck_x)



# Y-Coordinate
for right_values_y in np.array(keypoints_data['Right Shoulder_y']):
  neck_y.append(right_values_y)
for i in range(len(np.array(keypoints_data['Left Shoulder_y']))):
  neck_y[i]+=np.array(keypoints_data['Left Shoulder_y'])[i]
  neck_y[i] = neck_y[i]/2
# print(neck_y)



# Z-Coordinate
for right_values_z in np.array(keypoints_data['Right Shoulder_z']):
  neck_z.append(right_values_z)
for i in range(len(np.array(keypoints_data['Left Shoulder_z']))):
  neck_z[i]+=np.array(keypoints_data['Left Shoulder_z'])[i]
  neck_z[i] = neck_z[i]/2
# print(neck_z)

# Extracting coordinates of hip joint

hip_x, hip_y, hip_z = [], [], []

# X-Coordinate
for right_values_x in np.array(keypoints_data['Right Hip_x']):
  hip_x.append(right_values_x)
for i in range(len(np.array(keypoints_data['Left Hip_x']))):
  hip_x[i]+=np.array(keypoints_data['Left Hip_x'])[i]
  hip_x[i] = hip_x[i]/2
# print(hip_x)



# Y-Coordinate
for right_values_y in np.array(keypoints_data['Right Hip_y']):
  hip_y.append(right_values_y)
for i in range(len(np.array(keypoints_data['Left Hip_y']))):
  hip_y[i]+=np.array(keypoints_data['Left Hip_y'])[i]
  hip_y[i] = hip_y[i]/2
# print(hip_y)



# Z-Coordinate
for right_values_z in np.array(keypoints_data['Right Hip_z']):
  hip_z.append(right_values_z)
for i in range(len(np.array(keypoints_data['Left Hip_z']))):
  hip_z[i]+=np.array(keypoints_data['Left Hip_z'])[i]
  hip_z[i] = hip_z[i]/2
# print(hip_z)

# hip_z = np.array(hip_z)
# hip_z

reshaped_neck_x, reshaped_neck_y, reshaped_neck_z = np.array(neck_x).reshape(-1,1), np.array(neck_y).reshape(-1,1), np.array(neck_z).reshape(-1,1)
reshaped_hip_x, reshaped_hip_y, reshaped_hip_z = np.array(hip_x).reshape(-1,1), np.array(hip_y).reshape(-1,1), np.array(hip_z).reshape(-1,1)


final_keypoints_data = np.concatenate((np.array(keypoints_data), reshaped_neck_x, reshaped_neck_y, reshaped_neck_z,
                                                          reshaped_hip_x, reshaped_hip_y, reshaped_hip_z), axis=1)
# print(pd.DataFrame(result_array))
# final_keypoints_data

def affine_transformation(all_points, x_neck, y_neck, theta):

  di_array = [y_neck, x_neck]
  sin_theta, cos_theta = math.sin(theta), math.cos(theta)
  Ma_array = np.array([[cos_theta, 0-sin_theta, 1-cos_theta, sin_theta], [sin_theta, cos_theta, 0-sin_theta, 1-cos_theta]])
  new_all_points=[]

  for data in range(len(all_points)):
    if (data%3 != 2):
      di_array = [all_points[data]] +di_array
      if (len(di_array)==4):
        di_array.reverse()
        di_array = np.transpose(np.array(di_array))
        result = np.matmul(Ma_array, di_array)
        # print(result[2])
        x = result[0]
        y = result[1]
        new_all_points = new_all_points + [x,y]  + [all_points[data+1]]
        # print(new_all_points)
        di_array = [y_neck, x_neck]
  new_all_points = np.array(new_all_points)
  return ((new_all_points))
  # print(new_all_points.shape)

# 51 --> neck_x       56 --> hip_z

# Determination of angle of rotation
phi = 0.1
count = 0
for data in final_keypoints_data:
  arg = (data[52]-data[55])/(data[53]-data[56])
  theta = np.radians(math.atan(arg))
  # print(theta)
  if theta >= phi:
    data[:51] = affine_transformation(data[:51], data[51], data[52], theta)
    # affine_transformation(data[:51], data[51], data[52], theta)
    # print(theta)
# pd.DataFrame(final_keypoints_data)

h_unif = 225

# Specify the starting column index and the interval
start_column = 1
interval = 3

# Select columns based on the specified criteria
selected_columns = final_keypoints_data[:, start_column::interval]

# Find the maximum and minimum values for each selected column
max_values = np.max(selected_columns, axis=0)
min_values = np.min(selected_columns, axis=0)
scaling_factors = [(h_unif)/(max_values[i]-min_values[i]) for i in range(len(max_values))]
# scaling_factors

# print(len(scaling_factors))

# print(scaling_factors)
scaling_factors_copy = scaling_factors
for frame in ((final_keypoints_data[:,1:])):
  scaling_factors = scaling_factors_copy
  for joint in range(len(frame)):
    # print(len(frame))
    # print(joint)
    count+=1
    if (joint % 3 == 0 or joint % 3 == 1):
      # print(joint, ":",scaling_factors[0])
      frame[joint] *= scaling_factors[0]
    if (joint % 3 == 2):
      if (len(scaling_factors)==0):
        break
      else:
        scaling_factors = scaling_factors[1:]
# pd.DataFrame(final_keypoints_data)

for frame in ((final_keypoints_data[:,1:])):
  # neck_x, neck_y = frame[51], frame[52]
  # print(neck_x)
  for joint in range(len(frame)):
    if (joint % 3 == 0):
      frame[joint] -= frame[52]
    if (joint % 3 == 1):
      frame[joint] -= frame[53]
pd.DataFrame(final_keypoints_data)

final_keypoints_data.shape

type(pd.DataFrame(final_keypoints_data))

# Save the concatenated matrix as a new CSV file
output_csv_path = '/content/drive/MyDrive/Concatenated_Output_With_Labels_Normalised.csv'
pd.DataFrame(final_keypoints_data).to_csv(output_csv_path, index=False)

"""##Starts from here"""

# # Load your dataset
# file_path = "/content/drive/MyDrive/Concatenated_Output_With_Labels_Normalised.csv"
# df = pd.read_csv(file_path)

# # Assuming your data is arranged such that the first column is the label, and the rest are input features
# labels = df.iloc[:, 0]
# data = df.iloc[:, 1:]

# # Convert labels to one-hot encoding
# labels_one_hot = tf.keras.utils.to_categorical(labels - 1, num_classes=62)

# print(len(data))

# # Reshape data for convolutional layers
# data = np.array(data).reshape((42234, 57, 1, 1))

# # # Data augmentation
# # datagen = ImageDataGenerator(
# #     horizontal_flip=True,
# #     preprocessing_function=lambda x: x + np.random.normal(scale=0.01, size=x.shape) if np.random.rand() < 0.3 else x
# # )

# # Model architecture using Functional API
# inputs = tf.keras.Input(shape=(57, 1))

# # Convolutional Layer 1
# x = layers.Conv1D(32, (3,), strides=1)(inputs)
# x = layers.PReLU()(x)

# # Convolutional Layer 2
# x = layers.Conv1D(64, (3,), strides=1)(x)
# x = layers.PReLU()(x)

# # Pooling Layer 1
# x = layers.MaxPooling1D(pool_size=2, strides=2)(x)

# # Convolutional Layer 3
# x = layers.Conv1D(64, (3,), strides=1)(x)
# x = layers.PReLU()(x)

# # Convolutional Layer 4
# x = layers.Conv1D(64, (3,), strides=1)(x)
# x = layers.PReLU()(x)

# # Eltwise 1
# # x = layers.Add()([x, previous_layer_output])

# # Convolutional Layer 5
# x = layers.Conv1D(128, (3,), strides=1)(x)
# x = layers.PReLU()(x)

# # Pooling Layer 2
# x = layers.MaxPooling1D(pool_size=2, strides=2)(x)

# # Convolutional Layer 6
# x = layers.Conv1D(128, (3,), strides=1)(x)
# x = layers.PReLU()(x)

# # Convolutional Layer 7
# x = layers.Conv1D(128, (3,), strides=1)(x)
# x = layers.PReLU()(x)

# # Eltwise 2
# # x = layers.Add()([x, previous_layer_output])

# # Flatten
# x = layers.Flatten()(x)

# # Fully Connected Layer
# outputs = layers.Dense(62, activation='softmax')(x)

# # Create model
# model = tf.keras.Model(inputs=inputs, outputs=outputs)

# # Compile the model
# opt = Adam(learning_rate=1e-5)
# model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

# # Train the model
# # history = model.fit(datagen.flow(data,batch_size=32), epochs=40, steps_per_epoch=len(data) // 32, verbose=1)
# history = model.fit(data, labels_one_hot, batch_size=32, epochs=40000, steps_per_epoch=len(data) // 32, verbose=1)