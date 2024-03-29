import os
import cv2
import mediapipe as mp
import pytest
import numpy as np

from src.face_utilities import get_face_count, get_binary_mask, get_face_details, shoulder_angle_valid

current_dir = os.path.dirname(os.path.abspath(__file__))
testdata_path = os.path.join(current_dir, "testdata")


def data_path(filename: str) -> str:
    return os.path.join(testdata_path, filename)


testdata_detect_face_count = [
    ("one_face.jpg", 1),
    ("two_faces.jpg", 2),
    ("no_face.jpg", 0),
    ("rotated_face_1.jpg", 1),
]


@pytest.mark.parametrize("file, expected_face_count", testdata_detect_face_count)
def test_detect_face_count_returns_count(file: str, expected_face_count: int):
    filepath = data_path(file)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB))
    face_count, _ = get_face_count(image)
    assert face_count == expected_face_count


testdata_detect_face_rotation = [
    ("one_face.jpg", 2),
    ("rotated_face_1.jpg", -17),
    ("rotated_face_2.jpg", -27),
    ("rotated_face_3.jpg", -10),
    ("rotated_face_4.jpg", 2),
    ("rotated_face_5.jpg", 46),
    ("rotated_face_6.jpg", 4),
]


@pytest.mark.parametrize("file, expected_face_rotation", testdata_detect_face_rotation)
def test_get_face_angle(file: str, expected_face_rotation: float):
    filepath = data_path(file)
    image = cv2.imread(filepath)
    face_rotation, _, _ = get_face_details(image)
    assert face_rotation == pytest.approx(expected_face_rotation, abs=1)


testdata_get_background_mask = [
    ("one_face.jpg", "one_face.mask.jpg"),
    ("rotated_face_1.jpg", "rotated_face_1.mask.jpg"),
    ("rotated_face_4.jpg", "rotated_face_4.mask.jpg"),
    ("rotated_face_6.jpg", "rotated_face_6.mask.jpg"),
    ("three_faces.jpg",
     "three_faces.mask.jpg")
]


@pytest.mark.parametrize("original_file, expected_mask_file", testdata_get_background_mask)
def test_get_background_mask(original_file: str, expected_mask_file: str):
    original_img_path = data_path(original_file)
    expected_mask_path = data_path(expected_mask_file)

    image = mp.Image(image_format=mp.ImageFormat.SRGB,
                     data=cv2.cvtColor(cv2.imread(original_img_path), cv2.COLOR_BGR2RGB))
    expected_mask = cv2.imread(expected_mask_path, cv2.IMREAD_GRAYSCALE)
    generated_mask = get_binary_mask(image)

    # Ensure the generated mask is in grayscale (if it isn't already)
    if len(generated_mask.shape) == 3:
        generated_mask = cv2.cvtColor(generated_mask, cv2.COLOR_BGR2GRAY)

    difference = np.sum(np.abs(generated_mask.astype("float") - expected_mask.astype("float")))
    total = np.sum(expected_mask.astype("float"))
    percentage_diff = (difference / total) * 100

    print(f"Percentage difference: {percentage_diff}")

    assert percentage_diff <= 5


testdata_shoulder_angle_valid = [
    ("one_face.jpg", True)
]


@pytest.mark.parametrize("file, expected_shoulder_angle", testdata_shoulder_angle_valid)
def test_shoulder_angle_valid_returns_result(file: str, expected_shoulder_angle: bool):
    filepath = data_path(file)
    image = cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB)
    angle, is_shoulder_angle_valid = shoulder_angle_valid(image)
    assert is_shoulder_angle_valid == expected_shoulder_angle
