import matplotlib.pyplot as plt
import ast

def normalize_data(value):
    """Normalize the data as per the specified condition"""
    if value > 0:
        return 180 - value
    else:
        return -(180 + value)

def plot_hand_data(filename):
    # Load data from file
    with open(filename, 'r') as file:
        # Parse each line as a list of numbers
        right_hand_data = ast.literal_eval(file.readline().strip())
        right_hand_span = ast.literal_eval(file.readline().strip())
        left_hand_data = ast.literal_eval(file.readline().strip())
        left_hand_span = ast.literal_eval(file.readline().strip())
    
    # Normalize the data according to the new rule
    right_hand_data = [normalize_data(value) for value in right_hand_data]
    # right_hand_span = [normalize_data(value) for value in right_hand_span]
    left_hand_data = [normalize_data(value) for value in left_hand_data]
    # left_hand_span = [normalize_data(value) for value in left_hand_span]
    
    right_hand_data = right_hand_data[:1000]
    right_hand_span = right_hand_span[:1000]
    left_hand_data = left_hand_data[:1000]
    left_hand_span = left_hand_span[:1000]

    # Pad the shorter list with None values to match the length of the longer list
    max_len = max(len(right_hand_data), len(left_hand_data))
    right_hand_data.extend([None] * (max_len - len(right_hand_data)))
    right_hand_span.extend([None] * (max_len - len(right_hand_span)))
    left_hand_data.extend([None] * (max_len - len(left_hand_data)))
    left_hand_span.extend([None] * (max_len - len(left_hand_span)))
    
    # Generate frame numbers (x-axis)
    frames = list(range(1, max_len + 1))
    # frames = list(range(1, 1000))
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(frames, right_hand_data, label="Right Hand Angle", color="blue")
    plt.plot(frames, left_hand_data, label="Left Hand", color="red")
    # plt.plot(frames, right_hand_span, label="Right Hand Span", color="purple")
    # plt.plot(frames, left_hand_span, label="Left Hand Span", color="orange")
    
    # Add titles and labels
    plt.title(filename)
    plt.xlabel("Frame Number")
    plt.ylabel("Normalized Data Value (Adjusted around 180)")
    plt.legend()
    
    # Show the plot
    plt.show()

# Example usage
filename = 'angle_outputs/above_new/tense_hanon'  # Replace with your file name
plot_hand_data(filename)
