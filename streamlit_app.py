import streamlit as st
import numpy as np

# Page title
st.title("Jeppeleppes Takstuvning 🎈")

# Display the reference image (replace the URL if necessary)
image_url = "https://raw.githubusercontent.com/JF2182233/blank-app/refs/heads/main/cords-tak-3.png"
st.image(image_url)

# Input field for polygon coordinates (as comma-separated pairs)
polygon_input = st.text_area(
    "Ange koordinaterna för polygonens hörn som kommaseparerade par (t.ex. 0,0 0,10 20,10 20,0 6,0 10,5.7 14,0):",
    value="0,0 0,10 20,10 20,0 6,0 10,5.7 14,0"
)

# Input field for slice width
slice_width = st.number_input("Bredd i mm för varje plåt", value=1.0, step=0.1)

# Button to trigger the calculation
if st.button("Räkna ut vad som behövs"):

    # Parse the polygon vertices from the input text
    try:
        vertices = [
            tuple(map(float, point.split(','))) 
            for point in polygon_input.split()
        ]
        
        # Define edges based on parsed vertices
        edges = [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]

        # Function to find the intersection of a vertical line with a line segment
        def find_intersection(x, p1, p2):
            x1, y1 = p1
            x2, y2 = p2

            # Check if the line segment is vertical
            if x1 == x2:
                if x == x1:  # If the slice is on this vertical segment
                    return (min(y1, y2), max(y1, y2))  # Return the range as a tuple
                return None  # No intersection if the vertical slice doesn't match segment

            # Calculate the slope and intercept for the non-vertical line
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1

            # Calculate the y-coordinate of the intersection
            y = slope * x + intercept

            # Check if the intersection point (x, y) is within the bounds of the segment
            if min(x1, x2) <= x <= max(x1, x2):
                return y
            return None

        # Loop through each slice position and calculate floorboard heights
        floorboard_heights = []
        max_x = max(x for x, _ in vertices)

        for i in range(int(max_x / slice_width)):
            x_pos = i * slice_width
            y_intersections = []

            # Calculate intersections at the current slice boundary
            for edge in edges:
                intersection = find_intersection(x_pos, edge[0], edge[1])
                if intersection is not None:
                    if isinstance(intersection, tuple):  # Vertical segment case
                        y_intersections.extend(intersection)
                    else:
                        y_intersections.append(intersection)

            # Determine the height for this slice
            if y_intersections:
                max_height = max(y_intersections) - min(y_intersections)
                floorboard_heights.append((x_pos, max_height))

        # Display the calculated floorboard heights
        st.write("Plåt, positioner och längd:")
        for x_start, height in floorboard_heights:
            st.write(f"Plåt börjar vid x = {x_start:.1f} mm, höjd = {height:.2f} mm")
    
    except Exception as e:
        st.error("Error parsing polygon coordinates. Please ensure they are formatted correctly.")
        st.error(f"Details: {e}")
