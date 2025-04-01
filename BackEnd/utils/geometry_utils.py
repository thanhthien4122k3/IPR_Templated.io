# utils/geometry_utils.py
import math

def is_point_inside(x, y, width, height, rotation, mouse_x, mouse_y):
    """Check if a point (mouse_x, mouse_y) is inside a rectangle defined by (x, y, width, height) with rotation."""
    # Convert to local coordinates
    local_x = mouse_x - x
    local_y = mouse_y - y
    # Convert rotation to radians and negate it
    angle_rad = math.radians(-rotation)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    # Rotate the point to match the rectangle's orientation
    rotated_x = local_x * cos_a + local_y * sin_a
    rotated_y = -local_x * sin_a + local_y * cos_a
    # Check if the rotated point is within bounds
    return 0 <= rotated_x <= width and 0 <= rotated_y <= height

def is_near_border(x, y, width, height, mouse_x, mouse_y, buffer=5, proximity_threshold=15):
    """Check if a point (mouse_x, mouse_y) is near a border or corner of a rectangle."""
    # Define border coordinates with buffer
    border_x, border_y = x - buffer, y - buffer
    border_width, border_height = width + 2 * buffer, height + 2 * buffer

    # Define corners and edges for resizing
    corners = {
        "top-left": (border_x, border_y),
        "top-right": (border_x + border_width, border_y),
        "bottom-left": (border_x, border_y + border_height),
        "bottom-right": (border_x + border_width, border_y + border_height)
    }
    edges = {
        "top": ((border_x, border_y), (border_x + border_width, border_y)),
        "left": ((border_x, border_y), (border_x, border_y + border_height)),
        "right": ((border_x + border_width, border_y), (border_x + border_width, border_y + border_height)),
        "bottom": ((border_x, border_y + border_height), (border_x + border_width, border_y + border_height))
    }

    # Check proximity to corners
    for name, (cx, cy) in corners.items():
        if math.sqrt((mouse_x - cx) ** 2 + (mouse_y - cy) ** 2) < proximity_threshold:
            return True, name

    # Check proximity to edges
    for name, ((start_x, start_y), (end_x, end_y)) in edges.items():
        length = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
        if length == 0:
            continue
        t = max(0, min(1, ((mouse_x - start_x) * (end_x - start_x) + (mouse_y - start_y) * (end_y - start_y)) / (length ** 2)))
        proj_x, proj_y = start_x + t * (end_x - start_x), start_y + t * (end_y - start_y)
        if math.sqrt((mouse_x - proj_x) ** 2 + (mouse_y - proj_y) ** 2) < proximity_threshold:
            return True, name

    return False, None