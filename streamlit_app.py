import streamlit as st
import numpy as np
import math

# Title for the app
st.title("Jeppeleppes Takstuvning 🎈")

# Display reference image
image_url = "https://raw.githubusercontent.com/JF2182233/blank-app/refs/heads/main/cords-tak-3.png"
st.image(image_url)

# Input fields for polygon edge lengths and angles
st.write("Ange längder och vinklar för polygonens kanter:")

# Define the default edge lengths and angles (relative angles)
default_lengths = [10, 20, 10, 8, 6, 5.7, 6]  # Example values for each edge
default_angles = [90, 0, 90, -45, 45, 0]  # Example relative angles in degrees

# User inputs for edge lengths and angles
lengths = []
for i, default_length in enumerate(default_lengths, start=1):
    length = st.number_input(f"Längd för kant {i} (mm):", value=float(default_length), step=0.1)
    lengths.append(length)

angles = []
for i, default_angle in enumerate(default_angles, start=1):
    angle = st.number_input(f"Vinkel för hörn {i} (°):", value=float(default_angle), step=0.1)
    angles.append(math.radians(angle))  # Convert angles to radians for calculations

# Calculate vertex coordinates based on edge lengths and angles
vertices = {1: (0, 0)}  # Start from the origin
current_angle = 0  # Start facing "upward" along the y-axis

for i, (length, angle) in enumerate(zip(lengths, angles), start=2):
    x_prev, y_prev = vertices[i - 1]
    current_angle += angle
    x = x_prev + length * math.cos(current_angle)
    y = y_prev + length * math.sin(current_angle)
    vertices[i] = (x, y)

# Define the polygon edges based on numbered points
edges = [(i, i + 1) for i in range(1, len(vertices))]
edges[-1] = (len(vertices), 1)  # Close the polygon

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

    for i in range(int(max(x for x, y in vertices.values()) / slice_width)):
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
           
