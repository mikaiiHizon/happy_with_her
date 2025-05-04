import tkinter as tk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sympy import symbols, sympify, lambdify

theta_sym, phi_sym = symbols('theta phi')

def show_credits_popup():
    messagebox.showinfo(
        "Credits",
        "Created By: Hizon, Joseph Nathaniel\nCourse and Year: Computer Science 2nd Year"
    )

def evaluate_expression(expr, theta_value=None, phi_value=None):
    try:
        expr = sympify(expr)
        func = lambdify([theta_sym, phi_sym], expr, modules=["math"])
        return func(theta_value, phi_value)
    except Exception as e:
        raise ValueError(f"Invalid expression: {expr}. Error: {e}")

def polar_to_cartesian_2d(r_expr, theta_expr):
    try:
        theta_value = evaluate_expression(theta_expr)
        r_value = evaluate_expression(r_expr, theta_value=theta_value)
        x = r_value * math.cos(math.radians(theta_value))
        y = r_value * math.sin(math.radians(theta_value))
        return x, y, r_value, theta_value
    except ValueError as e:
        raise ValueError(f"Error in 2D calculation: {e}")

def polar_to_cartesian_3d(r_expr, phi_expr, theta_expr):
    try:
        theta_value = evaluate_expression(theta_expr)
        phi_value = evaluate_expression(phi_expr)
        r_value = evaluate_expression(r_expr, theta_value=theta_value, phi_value=phi_value)
        x = r_value * math.sin(math.radians(theta_value)) * math.cos(math.radians(phi_value))
        y = r_value * math.sin(math.radians(theta_value)) * math.sin(math.radians(phi_value))
        z = r_value * math.cos(math.radians(theta_value))
        return x, y, z, r_value, phi_value, theta_value
    except ValueError as e:
        raise ValueError(f"Error in 3D calculation: {e}")

def plot_2d_coordinates(x, y, r, theta):
    plt.figure(figsize=(8, 8))
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color='blue', label=f'R={r}, θ={theta}°')
    circle = plt.Circle((0, 0), r, color='orange', fill=False, linestyle='dotted', label=f'Circle of Radius R={r}')
    plt.gca().add_artist(circle)
    max_range = max(abs(x), abs(y), abs(r)) + 1
    plt.xlim(-max_range, max_range)
    plt.ylim(-max_range, max_range)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('2D Polar Coordinates Representation')
    plt.legend()
    plt.show()

def plot_3d_coordinates(x, y, z, r, phi, theta):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(0, 0, 0, x, y, z, color='blue', label=f'R={r}, θ={theta}°, φ={phi}°')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    sphere_x = r * np.outer(np.sin(v), np.cos(u))
    sphere_y = r * np.outer(np.sin(v), np.sin(u))
    sphere_z = r * np.outer(np.cos(v), np.ones_like(u))
    ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color='orange', alpha=0.3, label=f'Sphere of Radius R={r}')
    max_range = max(abs(x), abs(y), abs(z), abs(r)) + 1
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('3D Spherical Coordinates Representation')
    ax.legend()
    plt.show()

def calculate_2d():
    try:
        r_expr = r_entry.get()
        theta_expr = theta_entry.get()
        x, y, r, theta = polar_to_cartesian_2d(r_expr, theta_expr)
        result_label.config(text=f"Cartesian Coordinates: (x, y) = ({x:.2f}, {y:.2f})")
        plot_2d_coordinates(x, y, r, theta)
        show_conclusion_2d(r, theta, x, y)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def calculate_3d():
    try:
        r_expr = r_entry.get()
        phi_expr = phi_entry.get()
        theta_expr = theta_3d_entry.get()
        x, y, z, r, phi, theta = polar_to_cartesian_3d(r_expr, phi_expr, theta_expr)
        result_label.config(text=f"Cartesian Coordinates: (x, y, z) = ({x:.2f}, {y:.2f}, {z:.2f})")
        plot_3d_coordinates(x, y, z, r, phi, theta)
        show_conclusion_3d(r, phi, theta, x, y, z)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def reset_fields():
    r_entry.delete(0, tk.END)
    theta_entry.delete(0, tk.END)
    phi_entry.delete(0, tk.END)
    theta_3d_entry.delete(0, tk.END)
    result_label.config(text="Result will appear here.")
    conclusion_label.config(text="")

def show_conclusion_2d(r, theta, x, y):
    conclusion = (
        f"The calculation shows that the point lies at a distance of {r} units from the origin "
        f"and at an angle of {theta}° measured counterclockwise from the positive X-axis.\n"
        f"In Cartesian coordinates, this corresponds to the point ({x:.2f}, {y:.2f}).\n"
        "The graph visually represents this point as a vector originating from the origin."
    )
    conclusion_label.config(text=conclusion)

def show_conclusion_3d(r, phi, theta, x, y, z):
    conclusion = (
        f"The calculation shows that the point lies at a distance of {r} units from the origin.\n"
        f"The azimuthal angle (φ) is {phi}°, measured in the XY-plane from the positive X-axis.\n"
        f"The polar angle (θ) is {theta}°, measured from the positive Z-axis.\n"
        f"In Cartesian coordinates, this corresponds to the point ({x:.2f}, {y:.2f}, {z:.2f}).\n"
        "The graph visually represents this point in 3D space as a vector originating from the origin."
    )
    conclusion_label.config(text=conclusion)

root = tk.Tk()
root.title("Hizon Calculus Project - Polar Coordinates")
root.geometry("500x500")
root.configure(bg="#f0f8ff")

frame = tk.Frame(root, padx=15, pady=15, bg="#f0f8ff")
frame.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(frame, text="Polar Coordinates Calculator", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#333")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame, text="Radius (R):", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, sticky="w", pady=5)
r_entry = tk.Entry(frame, font=("Arial", 12))
r_entry.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Angle (θ in degrees):", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, sticky="w", pady=5)
theta_entry = tk.Entry(frame, font=("Arial", 12))
theta_entry.grid(row=2, column=1, pady=5)

tk.Label(frame, text="Azimuthal Angle (φ in degrees):", font=("Arial", 12), bg="#f0f8ff").grid(row=3, column=0, sticky="w", pady=5)
phi_entry = tk.Entry(frame, font=("Arial", 12))
phi_entry.grid(row=3, column=1, pady=5)

tk.Label(frame, text="Polar Angle (θ in degrees):", font=("Arial", 12), bg="#f0f8ff").grid(row=4, column=0, sticky="w", pady=5)
theta_3d_entry = tk.Entry(frame, font=("Arial", 12))
theta_3d_entry.grid(row=4, column=1, pady=5)

result_label = tk.Label(frame, text="Result will appear here.", font=("Arial", 12), bg="#f0f8ff", fg="blue", wraplength=400, justify="left")
result_label.grid(row=5, column=0, columnspan=2, pady=10)

conclusion_label = tk.Label(frame, text="", font=("Arial", 12, "italic"), bg="#f0f8ff", fg="green", wraplength=400, justify="left")
conclusion_label.grid(row=6, column=0, columnspan=2, pady=5)

button_frame = tk.Frame(frame, bg="#f0f8ff")
button_frame.grid(row=7, column=0, columnspan=2, pady=10)

calculate_2d_button = tk.Button(button_frame, text="Calculate 2D", font=("Arial", 12), command=calculate_2d, bg="#4caf50", fg="white")
calculate_2d_button.grid(row=0, column=0, padx=5)

calculate_3d_button = tk.Button(button_frame, text="Calculate 3D", font=("Arial", 12), command=calculate_3d, bg="#2196f3", fg="white")
calculate_3d_button.grid(row=0, column=1, padx=5)

reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 12), command=reset_fields, bg="#f44336", fg="white")
reset_button.grid(row=0, column=2, padx=5)

credits_button = tk.Button(button_frame, text="Show Credits", font=("Arial", 12), command=show_credits_popup, bg="#ff9800", fg="white")
credits_button.grid(row=0, column=3, padx=5)

root.mainloop()