
""" NACA Airfoil Generator: Visualize and Export Airfoil Coordinates """

__Author__ = """ Jesus Torres """

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import os

def generate_naca_airfoil(M, P, T, num_points=100):
    """
    Generate coordinates for a NACA airfoil.

    Args:
        M (float): Maximum camber as a decimal (e.g., 0.02 for 2% camber).
        P (float): Location of maximum camber as a decimal (e.g., 0.4 for 40% chord).
        T (float): Thickness as a decimal (e.g., 0.12 for 12% thickness).
        num_points (int): Number of points to generate for the airfoil.

    Returns:
        x, y: Arrays containing the x and y coordinates of the airfoil.
    """
    # Generate x-coordinates
    x = np.linspace(0, 1, num_points)

    # Calculate camber line and thickness distribution
    if P == 0.0:
        yc = np.zeros_like(x)
    else:
        yc = np.where(x < P, (M / P**2) * (2 * P * x - x**2), (M / (1 - P)**2) * ((1 - 2 * P) + 2 * P * x - x**2))
    yt = (T / 0.2) * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1036 * x**4)

    # Calculate airfoil coordinates
    xu = x - yt * np.sin(np.arctan2(yc, x))
    xl = x + yt * np.sin(np.arctan2(yc, x))
    yu = yc + yt * np.cos(np.arctan2(yc, x))
    yl = yc - yt * np.cos(np.arctan2(yc, x))

    return np.concatenate((xu[::-1], xl[1:])), np.concatenate((yu[::-1], yl[1:]))

def generate_naca_title(M, P, T):
    M_str = str(int(M * 100)).zfill(2)  # Format M as a two-digit integer with leading zeros
    P_str = str(int(P * 10))            # Format P as a one-digit integer
    T_str = str(int(T * 100))           # Format T as a two-digit integer

    return f"NACA {M_str}{P_str}{T_str} Airfoil"

def plot_naca_airfoil(M, P, T):
    x, y = generate_naca_airfoil(M, P, T)

    # Update the data of the existing airfoil_line plot
    airfoil_line.set_data(x, y)
    
    # Set a fixed aspect ratio and adjust the plot boundaries
    current_axes.set_aspect('equal', adjustable='box')
    current_axes.set_xlim(-0.1, 1.1)  # Adjust the x-axis limits as needed
    current_axes.set_ylim(-0.6, 0.6)  # Adjust the y-axis limits as needed
    current_axes.set_title(generate_naca_title(M, P, T))
    current_axes.set_xlabel("x")
    current_axes.set_ylabel("y")
    current_axes.grid()

    # Update the canvas
    canvas.draw()
    
# Create a function to generate and save the coordinates to a CSV file
def save_coordinates_to_csv(x, y):
    # Generate a unique filename on the desktop
    desktop_path = os.path.expanduser("~/Desktop")
    base_filename = "naca_airfoil_coordinates.csv"
    filename = base_filename
    
    # Check if the file already exists, and if so, add a number to the filename
    file_number = 1
    while os.path.exists(os.path.join(desktop_path, filename)):
        filename = f"{os.path.splitext(base_filename)[0]}_{file_number}.csv"
        file_number += 1
    
    # Save the coordinates to the CSV file
    with open(os.path.join(desktop_path, filename), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])  # Write header row
        for xi, yi in zip(x, y):
            writer.writerow([xi, yi])
    
    # Display a popup message with the saved filename
    messagebox.showinfo("CSV Saved", f"The CSV file has been saved as '{filename}' on the desktop.")
            
def generate_airfoil():
    M = float(M_entry.get())
    P = float(P_entry.get())
    T = float(T_entry.get())

    # Call the plot_naca_airfoil function to update the airfoil plot
    plot_naca_airfoil(M, P, T)

    # Save the coordinates to a CSV file on the desktop
    x, y = generate_naca_airfoil(M, P, T)
    save_coordinates_to_csv(x, y)

root = tk.Tk()
root.title("NACA Airfoil Generator")

# Define global variables for the Figure and Axes
fig = plt.figure(figsize=(4, 3))
current_axes = fig.add_subplot(111)

# Load the background image
bg_image = Image.open("background.jpg")  # Replace with the path to your background image
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Label to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Make the background image "transparent" so that it doesn't cover the widgets
bg_label.image = bg_photo
bg_label.lower(bg_label)  # Place the background label behind other widgets

# Create a Frame to hold the input boxes and the Generate button
input_frame = ttk.Frame(root)
input_frame.pack(side=tk.TOP, pady=50)  # Adjust pady to control vertical alignment

# Create and pack labels and entry fields for M, P, and T within the input frame
ttk.Label(input_frame, text="Maximum Camber (M):").pack()
M_entry = ttk.Entry(input_frame)
M_entry.pack()

ttk.Label(input_frame, text="Location of Maximum Camber (P):").pack()
P_entry = ttk.Entry(input_frame)
P_entry.pack()

ttk.Label(input_frame, text="Thickness (T):").pack()
T_entry = ttk.Entry(input_frame)
T_entry.pack()

# Create a Generate button within the input frame
generate_button = ttk.Button(input_frame, text="Generate Airfoil", command=generate_airfoil)
generate_button.pack()

# Create a Matplotlib figure with a smaller size
fig = plt.figure(figsize=(4, 3))
current_axes = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Initialize empty lines for the airfoil plot
airfoil_line, = current_axes.plot([], [], lw=2)

# Update the window's geometry information
root.update_idletasks()

# Create a Label widget for the note
note_label = tk.Label(root, text="Image By ojosujono96", font=("Helvetica", 8), fg="gray")
# Position the label at the bottom right
note_label.place(relx=1.0, rely=1.0, anchor='se')  # Places the label at the bottom right corner

# Start the Tkinter main loop
root.mainloop()
