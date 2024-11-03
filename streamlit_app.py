import streamlit as st
import numpy as np

# Title for the app
st.title("Jeppeleppes Takstuvning 🎈")

# Display reference image
image_url = "https://raw.githubusercontent.com/JF2182233/blank-app/refs/heads/main/cords-tak-3.png"
st.image(image_url)

# Input fields for polygon coordinates and slice width
st.write("Ange polygonens hörnkoordinater i formatet (x, y):")

# Define the default vertices for the polygon with numbers instead of letters
default_vertices = {
    1: (0, 0),
    2: (0, 10),
    3: (20, 10),
    4: (20, 0),
    5: (6, 0),
    6: (10, 5.7),  # Approximate position of the peak of the triangle
    7: (14, 0)
}

# Display inputs for each vertex
vertices = {}
for i, (default_x, default_y) in default_vertices.items():
    x = st.number_input(f"{i} x:", value=float(default_x), step=0.1)
    y = st.number_input(f"{i} y:", value=float(default_y), step=0.1)
    vertices[i] = (x, y)

# Define the polygon edges based on numbered points
edges = [
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 7),
    (7, 6),
    (6, 5),
    (5, 1)
]

# Input for slice width
slice_width = st.number_input("Bredd i mm för varje plåt:", value=0.5, step=0.1)

# Button to trigger calculation
if st.button("Räkna ut vad som behövs"):

    # Function to find the intersection of a vertical line with a line segment
    def find_intersection(x, p1, p2):
        (x1, y1), (x2, y2) = vertices[p1], vertices[p2]

        # Check if the line segment is vertical
        if x1 == x2:
            if x == x1:  # If the slice is on this vertical segment
                return min(y1, y2), max(y1, y2)
            return None  # No intersection if the vertical slice doesn't match segment

        # Calculate slope and intercept
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        # Calculate the y-coordinate of the intersection
        y = slope * x + intercept

        # Check if the intersection is within the bounds of the segment
        if min(x1, x2) <= x <= max(x1, x2):
            return y
        return None

    # Calculate floorboard heights for each slice position
    floorboard_heights = []

    for i in range(int(vertices[3][0] / slice_width)):
        x_left = i * slice_width
        x_right = (i + 1) * slice_width

        y_min_left, y_max_left = float('inf'), float('-inf')
        y_min_right, y_max_right = float('inf'), float('-inf')

        # Calculate left intersection heights
        for edge in edges:
            intersection = find_intersection(x_left, edge[0], edge[1])
            if intersection is not None:
                if isinstance(intersection, tuple):  # Vertical segment case
                    y_min_left, y_max_left = min(y_min_left, intersection[0]), max(y_max_left, intersection[1])
                else:
                    y_min_left, y_max_left = min(y_min_left, intersection), max(y_max_left, intersection)

        # Calculate right intersection heights
        for edge in edges:
            intersection = find_intersection(x_right, edge[0], edge[1])
            if intersection is not None:
                if isinstance(intersection, tuple):  # Vertical segment case
                    y_min_right, y_max_right = min(y_min_right, intersection[0]), max(y_max_right, intersection[1])
                else:
                    y_min_right, y_max_right = min(y_min_right, intersection), max(y_max_right, intersection)

        # Determine the maximum height for this floorboard
        max_height = max(y_max_left - y_min_left, y_max_right - y_min_right)
        floorboard_heights.append((x_left, max_height))

    # Display the calculated floorboard heights in Swedish
    st.write("Plåt, positioner och längd:")
    for x_start, height in floorboard_heights:
        st.write(f"Plåt börjar vid x = {x_start:.1f} mm, höjd = {height:.2f} mm")
