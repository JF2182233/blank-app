import streamlit as st
import numpy as np
import math

# Title for the app
st.title("Jeppeleppes Takstuvning 🎈")

# Display reference image
image_url = "https://raw.githubusercontent.com/JF2182233/blank-app/refs/heads/main/cords-tak-3.png"
st.image(image_url)

# Input fields for polygon segment lengths and angles
st.write("Ange längd och vinkel mellan hörn:")

# Define the default lengths and angles between vertices
default_lengths = [10, 20, 10, 8, 8, 6]
default_angles = [math.radians(90), 0, math.radians(-90), math.radians(45), math.radians(0), math.radians(-45)]

# Input lengths and angles
lengths = [st.number_input(f"Längd {i+1}-{i+2}:", value=float(length), step=0.1) for i, length in enumerate(default_lengths)]
angles = [st.number_input(f"Vinkel {i+1}-{i+2} (i grader):", value=float(math.degrees(angle)), step=1.0) for i, angle in enumerate(default_angles)]
angles = [math.radians(angle) for angle in angles]  # Convert degrees to radians for calculation

# Input for slice width
slice_width = st.number_input("Bredd i mm för varje plåt:", value=0.5, step=0.1)

# Button to trigger calculation
if st.button("Räkna ut vad som behövs"):

# Reconstruct the vertices from side lengths
vertices = {}
vertices[1] = (0, 0)  # Starting at origin

# Initialize coordinates
x, y = vertices[1]

# Assign vertices using angles and lengths
angles = [0, 90, 0, -45, 0, 45]  # Relative angles in degrees between edges
lengths = [
    side_1_2,
    side_2_3,
    side_3_4,
    side_4_5,
    side_5_6,
    side_6_7
]

# Iteratively calculate positions based on lengths and angles
for i, (length, angle) in enumerate(zip(lengths, angles), start=2):
    angle_radians = np.radians(angle)
    x += length * np.cos(angle_radians)
    y += length * np.sin(angle_radians)
    vertices[i] = (round(x, 2), round(y, 2))

# Display vertices for debugging
st.write("Reconstructed vertices:")
for i, (vx, vy) in vertices.items():
    st.write(f"Vertex {i}: ({vx:.2f}, {vy:.2f})")


    # Define edges based on reconstructed vertices
    edges = [(i, i + 1) for i in range(1, len(vertices))] + [(len(vertices), 1)]  # Close the polygon

    # Debug message
    st.write("Debug: Calculating floorboard heights...")

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
    floorboard_heights.append((x_left, round(max_height, 2)))  # Round to 2 decimal places


    # Debug output to show calculated floorboard heights
    st.write("Debug: Floorboard Heights")
    st.write(floorboard_heights)

# Aggregate heights and count occurrences
height_counts = {}
for _, height in floorboard_heights:
    if height in height_counts:
        height_counts[height] += 1
    else:
        height_counts[height] = 1

# Display the aggregated floorboard heights in Swedish
st.write("Plåt, antal och höjd:")
for height, count in sorted(height_counts.items()):
    st.write(f"{count}x Plåt med höjd = {height:.2f} mm")

