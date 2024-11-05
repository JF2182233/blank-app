import streamlit as st

# Title for the app
st.title("Floorboard Height Calculator 📏")

# Input fields for the lengths of distances between vertices and slice width
st.write("Enter the lengths of distances between consecutive vertices:")

# Input fields for side lengths
side_lengths = {}
for i in range(1, 8):
    side_lengths[i] = st.number_input(f"Length between vertex {i} and vertex {i+1}:", value=1.0, step=0.1)

# Define the edges based on numbered points
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
slice_width = st.number_input("Width of each floorboard slice in mm:", value=0.5, step=0.1)

# Button to trigger calculation
if st.button("Calculate Floorboard Heights"):

    # Calculate the coordinates of each vertex based on the provided side lengths
    vertices = {}
    vertices[1] = (0, 0)  # Starting vertex at (0, 0)
    for i in range(2, 8):
        x = vertices[i-1][0] + side_lengths[i-1]
        y = 0  # Assuming the polygon is on the x-axis
        vertices[i] = (x, y)

    # Function to find the intersection of a vertical line with a line segment
    def find_intersection(x, p1, p2):
        # Function remains the same

    # Initialize list to store floorboard heights
        floorboard_heights = []

    # Calculate floorboard heights for each slice position
    for i in range(int(vertices[3][0] / slice_width)):
        x_left = i * slice_width
        x_right = (i + 1) * slice_width

        # Perform calculations to determine floorboard heights and append to the list

    # Aggregate heights and count occurrences
    height_counts = {}
    for _, height in floorboard_heights:
        if height in height_counts:
            height_counts[height] += 1
        else:
            height_counts[height] = 1

    # Display the aggregated floorboard heights
    st.write("Floorboard Heights:")
    for height, count in sorted(height_counts.items()):
        st.write(f"{count}x Floorboard with height = {height:.2f} mm")
