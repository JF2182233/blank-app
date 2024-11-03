import streamlit as st
import numpy as np

# Page title
st.title("Jeppeleppes takstuvning 🎈")

import streamlit as st

# Replace with the actual raw image URL
image_url = "https://raw.githubusercontent.com/JF2182233/blank-app/refs/heads/main/cords-tak-3.png"

st.image(image_url)

# Input field for polygon coordinates (as comma-separated pairs)
polygon_input = st.text_area(
    "Ange koordinaterna för polygonens hörn som kommaseparerade par (t.ex. 0,0 0,10 20,10 20,0 0,14 10,4 0,6):",
    value="0,0 0,10 20,10 20,0 0,14 10,4 0,6"
)

# Input field for slice width
slice_width = st.number_input("Bredd i mm för varje plåt", value=1.0, step=0.1)

# Button to trigger the calculation
if st.button("Calculate Floorboard Heights"):

    # Parse the polygon vertices from the input text
    try:
        vertices = [
            tuple(map(float, point.split(','))) 
            for point in polygon_input.split()
        ]
        
        # Define a helper function to find the intersection height at a given x-coordinate
        def find_intersection(x, p1, p2):
            # Line segment slope (dy/dx) and intercept calculations
            if p2[0] != p1[0]:  # Avoid division by zero for vertical lines
                slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
                y_intercept = p1[1] - slope * p1[0]
                y_at_x = slope * x + y_intercept
            else:
                y_at_x = max(p1[1], p2[1])  # Use the higher y for vertical lines
            return y_at_x if min(p1[0], p2[0]) <= x <= max(p1[0], p2[0]) else None
        
        # List to store floorboard heights
        floorboard_heights = []
        
        # Loop through each x position from left to right in increments of slice_width
        x_positions = np.arange(0, max(x for x, _ in vertices), slice_width)
        
        for x_start in x_positions:
            y_intersections = []
            
            # Find intersections with each polygon edge
            for i in range(len(vertices)):
                p1 = vertices[i]
                p2 = vertices[(i + 1) % len(vertices)]
                y = find_intersection(x_start, p1, p2)
                
                if y is not None:
                    y_intersections.append(y)
            
            # If we have intersections, calculate height of the floorboard at this x position
            if len(y_intersections) >= 2:
                height = abs(max(y_intersections) - min(y_intersections))
                floorboard_heights.append((x_start, height))
        
        # Display the calculated floorboard heights
        st.write("Floorboard positions and heights:")
        for x_start, height in floorboard_heights:
            st.write(f"Floorboard starting at x = {x_start:.1f} mm, height = {height:.2f} mm")
    
    except Exception as e:
        st.error("Error parsing polygon coordinates. Please ensure they are formatted correctly.")
        st.error(f"Details: {e}")
