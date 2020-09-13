import os
import re
import api as face_recognition
import numpy as np


train_dir = '/Users/abhivineet/Downloads/faces4'

def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]

X = []
y = []
verbose = False
for class_dir in os.listdir(train_dir):
    if not os.path.isdir(os.path.join(train_dir, class_dir)):
        continue

    print('starting {}.format', class_dir)

    for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
        image = face_recognition.load_image_file(img_path)
        face_bounding_boxes = face_recognition.face_locations(image)

        if len(face_bounding_boxes) != 1:
            # If there are no people (or too many people) in a training image, skip the image.
            if verbose:
                print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(
                    face_bounding_boxes) < 1 else "Found more than one face"))
        else:
            # Add face encoding for current image to the training set
            X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
            y.append(class_dir)
#The prediction part


 # Use the KNN model to find the best matches for the test face
#    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
#   are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]