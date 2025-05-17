def get_inputs():
    num_measurement_points = int(input("Enter the number of measurement points: "))
    print("\nSelect the calculation method:")
    print("1. 0.6Y Method")
    print("2. Average of 0.8Y and 0.2Y Method")
    print("3. Surface Velocity Method")
    method_choice = int(input("\nEnter your choice (1, 2, or 3): "))
    return num_measurement_points, method_choice


def calculate_discharge_0_6y(num_points):
    total_discharge = 0
    for _ in range(num_points):
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
    return round(total_discharge, 3)


def calculate_discharge_0_8y_0_2y(num_points):
    total_discharge = 0
    for _ in range(num_points):
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
    return round(total_discharge, 4)


def calculate_discharge_surface(num_points):
    conversion_factor = float(
        input("\nEnter the conversion factor for surface velocity: ")
    )
    surface_velocity = float(input("Enter the measured surface velocity (in ft/s): "))
    total_area = 0

    for _ in range(num_points):
        width = float(input("\nEnter the width between measurement points (in feet): "))
        depth_first = float(
            input("Enter the depth at the first measurement point (in feet): ")
        )
        depth_second = float(
            input("Enter the depth at the second measurement point (in feet): ")
        )

        point_area = ((depth_first + depth_second) / 2) * width
        total_area += point_area

    return round(conversion_factor * total_area * surface_velocity, 4)


def main():
    num_points, method_choice = get_inputs()

    if method_choice == 1:
        discharge = calculate_discharge_0_6y(num_points)
        print(
            f"\nTotal discharge calculated using 0.6Y method: {discharge} cubic feet per second (cusecs)"
        )
    elif method_choice == 2:
        discharge = calculate_discharge_0_8y_0_2y(num_points)
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
