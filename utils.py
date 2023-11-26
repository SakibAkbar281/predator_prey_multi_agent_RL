import math
import pygame
def calculate_angle(sprite1, sprite2):
    # Get the center positions of the sprites
    x1, y1 = sprite1.rect.center
    x2, y2 = sprite2.rect.center

    # Calculate the difference in positions
    dx = x2 - x1
    dy = y2 - y1

    # Calculate the angle using atan2
    # atan2 returns the angle in radians, so we convert it to degrees
    angle = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle)

    return angle_degrees

def is_sufficiently_different(angles, threshold=85):
    """
    Check if all angles in the list are at least 'threshold' degrees apart from each other.

    :param angles: List of angles (in degrees).
    :param threshold: Minimum difference in degrees required between any two angles.
    :return: True if all angles are sufficiently different, False otherwise.
    """
    for i in range(len(angles)):
        for j in range(i + 1, len(angles)):
            angle_diff = abs(angles[i] - angles[j])
            # Adjust for angles crossing the 360-degree line
            angle_diff = min(angle_diff, 360 - angle_diff)
            if angle_diff < threshold:
                return False
    return True

if __name__=="__main__":
    angles = [30, 30, 270]  # Example list of angles
    if is_sufficiently_different(angles):
        print("Angles are sufficiently different.")
    else:
        print("Angles are not sufficiently different.")