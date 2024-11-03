import streamlit as st
import numpy as np
st.title("🎈 My new roofing app")
# Input fields for polygon dimensions
slice_width = st.number_input("Width of each floorboard slice (mm)", value=1.0)

# Define the vertices of the polygon
vertices = {
    'A': (0, 0),
    'B': (0, 10),
    'C': (20, 10),
    'D': (20, 0),
    'G': (6, 0),
    'F': (10, 5.7),  # Approximate peak
    'E': (14, 0)
}

# Rest of the code to calculate floorboard heights

floorboard_heights = []
for i in range(int(vertices['C'][0] / slice_width)):
    x_left = i * slice_width
    x_right = (i + 1) * slice_width
    # intersection calculations (same as previous code)

    # Print results
    st.write("Floorboard positions and heights:")
    for x_start, height in floorboard_heights:
        st.write(f"Floorboard starting at x = {x_start:.1f} mm, height = {height:.2f} mm")


st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
