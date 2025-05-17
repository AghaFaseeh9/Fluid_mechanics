import matplotlib.pyplot as plt
import numpy as np


def set_dark_theme():
    plt.style.use("dark_background")
    plt.rcParams["figure.facecolor"] = "#1C1C1C"
    plt.rcParams["axes.facecolor"] = "#2D2D2D"
    plt.rcParams["axes.edgecolor"] = "#404040"
    plt.rcParams["axes.labelcolor"] = "white"
    plt.rcParams["xtick.color"] = "white"
    plt.rcParams["ytick.color"] = "white"
    plt.rcParams["grid.color"] = "#404040"
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["grid.alpha"] = 0.5


def get_inputs():
    num_points = int(input("Please enter the total number of measurement points: "))
    print("\nPlease select your preferred calculation method:")
    print("1. 0.6Y Method")
    print("2. Average of 0.8Y and 0.2Y Method")
    print("3. Surface Velocity Method")
    method_choice = int(input("\nEnter your choice (1, 2, or 3): "))
    return num_points, method_choice


def plot_measurements(points, depths, velocities, discharges, method_name):
    set_dark_theme()
    plt.figure(figsize=(15, 10))

    # Plot depths
    plt.subplot(221)
    plt.plot(points, depths, "-o", linewidth=2, markersize=8, color="#00BFFF")
    plt.title("Depth Profile", fontsize=12, pad=15, color="white")
    plt.xlabel("Measurement Points", fontsize=10)
    plt.ylabel("Depth (ft)", fontsize=10)
    plt.grid(True)

    # Plot velocities
    plt.subplot(222)
    plt.plot(points, velocities, "-o", linewidth=2, markersize=8, color="#FF6B6B")
    plt.title("Velocity Profile", fontsize=12, pad=15, color="white")
    plt.xlabel("Measurement Points", fontsize=10)
    plt.ylabel("Velocity (ft/s)", fontsize=10)
    plt.grid(True)

    # Plot discharges
    plt.subplot(223)
    plt.plot(points, discharges, "-o", linewidth=2, markersize=8, color="#98FB98")
    plt.title("Discharge Profile", fontsize=12, pad=15, color="white")
    plt.xlabel("Measurement Points", fontsize=10)
    plt.ylabel("Discharge (cusecs)", fontsize=10)
    plt.grid(True)

    # Plot cumulative discharge
    plt.subplot(224)
    cumulative_discharge = np.cumsum(discharges)
    plt.plot(
        points, cumulative_discharge, "-o", linewidth=2, markersize=8, color="#FF69B4"
    )
    plt.title("Cumulative Discharge", fontsize=12, pad=15, color="white")
    plt.xlabel("Measurement Points", fontsize=10)
    plt.ylabel("Cumulative Discharge (cusecs)", fontsize=10)
    plt.grid(True)

    plt.suptitle(f"Flow Analysis - {method_name}", fontsize=14, y=0.95, color="white")
    plt.tight_layout()
    plt.show()


def calculate_discharge_0_6y(num_points):
    total_discharge = 0
    depths = []
    velocities = []
    discharges = []

    for i in range(num_points):
        width = float(input("\nEnter the width between measurement points (in feet): "))
        depth_first = float(
            input("Enter the depth at the first measurement point (in feet): ")
        )
        depth_second = float(
            input("Enter the depth at the second measurement point (in feet): ")
        )
        velocity_first = float(
            input("Enter the velocity at the first measurement point (in ft/s): ")
        )
        velocity_second = float(
            input("Enter the velocity at the second measurement point (in ft/s): ")
        )
        avg_velocity = (velocity_first + velocity_second) / 2
        cross_section_area = ((depth_first + depth_second) / 2) * width
        point_discharge = cross_section_area * avg_velocity
        total_discharge += point_discharge

        # Store values for plotting
        depths.append((depth_first + depth_second) / 2)
        velocities.append(avg_velocity)
        discharges.append(point_discharge)

    # Create plots
    points = list(range(1, num_points + 1))
    plot_measurements(points, depths, velocities, discharges, "0.6Y Method")

    return round(total_discharge, 3)


def calculate_discharge_08y02y(num_points):
    total_discharge = 0
    depths = []
    velocities = []
    discharges = []

    for i in range(num_points):
        width = float(input("\nEnter the width between measurement points (in feet): "))
        depth_first = float(
            input("Enter the depth at the first measurement point (in feet): ")
        )
        depth_second = float(
            input("Enter the depth at the second measurement point (in feet): ")
        )
        velocity_08y_first = float(
            input("Enter the velocity at 0.8Y depth for first point (in ft/s): ")
        )
        velocity_08y_second = float(
            input("Enter the velocity at 0.8Y depth for second point (in ft/s): ")
        )
        velocity_02y_first = float(
            input("Enter the velocity at 0.2Y depth for first point (in ft/s): ")
        )
        velocity_02y_second = float(
            input("Enter the velocity at 0.2Y depth for second point (in ft/s): ")
        )
        avg_velocity_first = (velocity_08y_first + velocity_02y_first) / 2
        avg_velocity_second = (velocity_08y_second + velocity_02y_second) / 2
        avg_velocity = (avg_velocity_first + avg_velocity_second) / 2
        cross_section_area = ((depth_first + depth_second) / 2) * width
        point_discharge = cross_section_area * avg_velocity
        total_discharge += point_discharge

        # Store values for plotting
        depths.append((depth_first + depth_second) / 2)
        velocities.append(avg_velocity)
        discharges.append(point_discharge)

    # Create plots
    points = list(range(1, num_points + 1))
    plot_measurements(points, depths, velocities, discharges, "0.8Y/0.2Y Method")

    return round(total_discharge, 4)


def calculate_discharge_surface(num_points):
    conversion_factor = float(
        input("\nEnter the conversion factor for surface velocity: ")
    )
    surface_velocity = float(input("Enter the measured surface velocity (in ft/s): "))
    total_area = 0
    depths = []
    areas = []
    discharges = []

    for i in range(num_points):
        width = float(input("\nEnter the width between measurement points (in feet): "))
        depth_first = float(
            input("Enter the depth at the first measurement point (in feet): ")
        )
        depth_second = float(
            input("Enter the depth at the second measurement point (in feet): ")
        )
        point_area = ((depth_first + depth_second) / 2) * width
        total_area += point_area
        point_discharge = conversion_factor * point_area * surface_velocity

        # Store values for plotting
        depths.append((depth_first + depth_second) / 2)
        areas.append(point_area)
        discharges.append(point_discharge)

    # Create plots
    set_dark_theme()
    points = list(range(1, num_points + 1))
    plt.figure(figsize=(15, 10))

    # Plot depths
    plt.subplot(221)
    plt.plot(points, depths, "-o", linewidth=2, markersize=8, color="#00BFFF")
    plt.title("Depth Profile", fontsize=12, pad=15, color="white")
    plt.xlabel("Measurement Points", fontsize=10)
    plt.ylabel("Depth (ft)", fontsize=10)
    plt.grid(True)

    # Plot areas
    plt.subplot(222)
    plt.plot(points, areas, "-o", linewidth=2, markersize=8, color="#FF6B6B")
    plt.title("Cross-sectional Area Profile", fontsize=12, pad=15, color="white")
    plt.xlabel("Measurement Points", fontsize=10)
    plt.ylabel("Area (sq ft)", fontsize=10)
    plt.grid(True)

    # Plot discharges
    plt.subplot(223)
    plt.plot(points, discharges, "-o", linewidth=2, markersize=8, color="#98FB98")
    plt.title("Discharge Profile", fontsize=12, pad=15, color="white")
    plt.xlabel("Measurement Points", fontsize=10)
    plt.ylabel("Discharge (cusecs)", fontsize=10)
    plt.grid(True)

    # Plot cumulative discharge
    plt.subplot(224)
    cumulative_discharge = np.cumsum(discharges)
    plt.plot(
        points, cumulative_discharge, "-o", linewidth=2, markersize=8, color="#FF69B4"
    )
    plt.title("Cumulative Discharge", fontsize=12, pad=15, color="white")
    plt.xlabel("Measurement Points", fontsize=10)
    plt.ylabel("Cumulative Discharge (cusecs)", fontsize=10)
    plt.grid(True)

    plt.suptitle(
        "Flow Analysis - Surface Velocity Method", fontsize=14, y=0.95, color="white"
    )
    plt.tight_layout()
    plt.show()

    return round(conversion_factor * total_area * surface_velocity, 4)


def main():
    num_points, method_choice = get_inputs()
    if method_choice == 1:
        discharge = calculate_discharge_0_6y(num_points)
        print(
            f"\nTotal discharge calculated using 0.6Y method: {discharge} cubic feet per second (cusecs)"
        )
    elif method_choice == 2:
        discharge = calculate_discharge_08y02y(num_points)
        print(
            f"\nTotal discharge calculated using average of 0.2Y and 0.8Y method: {discharge} cubic feet per second (cusecs)"
        )
    elif method_choice == 3:
        discharge = calculate_discharge_surface(num_points)
        print(
            f"\nTotal discharge calculated using surface velocity method: {discharge} cubic feet per second (cusecs)"
        )


if __name__ == "__main__":
    main()
