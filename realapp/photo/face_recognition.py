import sys
import dlib
import os.path

# Image reading
from PIL import Image
import requests
from io import BytesIO

from .face_exceptions import MultiFaceException, NoFaceException, NoHistoryException

import numpy as np

import random

BASE = os.path.dirname(os.path.abspath(__file__))

def get_image_from_path(img_path):
    img = Image.open(img_path)
    return np.array(img)

def get_images_for_user(user):
    ''' Returns the history of verified faces for username as a list of image paths '''
    images = []

    if user.photo1:
        photo1 = Image.open(user.photo1) # UNTESTED
        images.append(np.array(photo1))
    if user.photo2:
        photo2 = Image.open(user.photo2) # UNTESTED
        images.append(np.array(photo2))
    if user.photo3:
        photo3 = Image.open(user.photo3) # UNTESTED
        images.append(np.array(photo3))

    random.shuffle(images)

    return images

def verify_img(img_path, user):
    ''' Takes an img path and verifies it against user with username '''
    # Get history of verified faces
    gt_faces = [get_images_for_user(user)[0]] # Get first image

    # If no faces to compare against, return false (not verified)
    if len(gt_faces) == 0:
        raise NoHistoryException("This user has no verified faces to compare against.")

    # Get model paths
    predictor_path = os.path.join(BASE,"shape_predictor_5_face_landmarks.dat")
    face_rec_model_path = os.path.join(BASE,"dlib_face_recognition_resnet_model_v1.dat")
    print(predictor_path)

    # Load face detectors
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(predictor_path)
    face_rec = dlib.face_recognition_model_v1(face_rec_model_path)

    # Read image from a path
    img = get_image_from_path(img_path)
    dets = detector(img, 1)

    # Euclidean distance initialization
    total_distance = 0
    average_distance = 0

    if len(dets) > 1:
        raise MultiFaceException("Error with image: Contains more than one face.")
    elif len(dets) == 0:
        raise NoFaceException("Error with image: Contains no faces.")
    else:
        # This should only process 1 face, since we already verified the photo.
        for k, d in enumerate(dets):
            # Get the landmarks/parts for the face in box d
            shape = sp(img, d)

            # Compute the 128D vector that describes the face
            face_descriptor = face_rec.compute_face_descriptor(img, shape)
            v = np.asarray([x for x in face_descriptor])

            for gt in gt_faces:
                gt_dets = detector(gt, 1)

                if len(gt_dets) != 1:
                    # There is more than one face or no faces
                    raise MultiFaceException("Error with ground truth: Contains more than one face.")
                else:
                    for k, d in enumerate(gt_dets):
                        # Compute the 128D vector for the history face
                        gt_shape = sp(gt, d)
                        gt_face_descriptor = face_rec.compute_face_descriptor(gt, gt_shape)
                        gt_v = np.asarray([x for x in gt_face_descriptor])

                        # Compare Euclidean distance
                        dist = np.linalg.norm(gt_v - v)

                        # Ensure we don't compare the face against itself
                        if dist == 0:
                            # Throw error that this face is from the history. User is uploading an old photo!
                            raise PastFaceException("This face has been used before. Please upload a current photo.")
                        else:
                            print("Euclidean distance: {0:.5f}".format(dist))
                            total_distance += dist

    # Output whether the faces are the same based on dist
    average_distance = total_distance / len(gt_faces)
    # print("Average distance from all faces: {0:.5f}".format(average_distance))

    # Set the Euclidean distance threshold to be 0.5
    # If average_distance <= threshold, return verified, else return not verified
    threshold = 0.5
    if average_distance <= threshold:
        # TODO: Add this face to the list of verified faces
        return True
    else:
        return False

if __name__ == "__main__":
    # For running on command line
    if len(sys.argv) != 3:
        print("To run: python face_recognition.py username face.jpg \n")
        exit()

    username = sys.argv[1] # the user we are verifying
    img_path = sys.argv[2] # the image to verify

    print("Processing file: {}".format(img_path))
    verified = verify_img(img_path, username)
