class DischargeCalculator:
    def __init__(self):
        self.n_points = int(input("Number of measurement points: "))
        print("\nSelect method:")
        print("1. 0.6Y Method")
        print("2. 0.8Y/0.2Y Average Method")
        print("3. Surface Velocity Method")
        self.method = int(input("Enter method (1-3): "))

    def get_measurements(self):
        return (
            float(input("Width between points (ft): ")),
            float(input("Depth at first point (ft): ")),
            float(input("Depth at second point (ft): ")),
        )

    def calc_area(self, width, depth1, depth2):
        return ((depth1 + depth2) / 2) * width

    def calculate_0_6y_method(self):
        total_q = 0
        for _ in range(self.n_points):
            width, depth1, depth2 = self.get_measurements()
            vel1, vel2 = float(input("Velocity at first point (ft/s): ")), float(
                input("Velocity at second point (ft/s): ")
            )
            total_q += self.calc_area(width, depth1, depth2) * (vel1 + vel2) / 2
            print(f"Current discharge (0.6Y): {round(total_q, 3)} cusecs")
        return total_q

    def calculate_0_8y_0_2y_method(self):
        total_q = 0
        for _ in range(self.n_points):
            width, depth1, depth2 = self.get_measurements()
            vel_08_1, vel_08_2 = float(
                input("Velocity at 0.8Y depth, first point (ft/s): ")
            ), float(input("Velocity at 0.8Y depth, second point (ft/s): "))
            vel_02_1, vel_02_2 = float(
                input("Velocity at 0.2Y depth, first point (ft/s): ")
            ), float(input("Velocity at 0.2Y depth, second point (ft/s): "))
            avg_vel = ((vel_08_1 + vel_02_1) / 2 + (vel_08_2 + vel_02_2) / 2) / 2
            total_q += self.calc_area(width, depth1, depth2) * avg_vel
            print(f"Current discharge (0.8Y/0.2Y): {round(total_q, 4)} cusecs")
        return total_q

    def calculate_surface_velocity_method(self):
        conv_factor, surf_vel = float(
            input("Surface velocity conversion factor: ")
        ), float(input("Measured surface velocity (ft/s): "))
        total_area = sum(
            self.calc_area(*self.get_measurements()) for _ in range(self.n_points)
        )
        total_q = conv_factor * total_area * surf_vel
        print(f"Total discharge (surface): {round(total_q, 4)} cusecs")
        return total_q

    def calculate_discharge(self):
        methods = {
            1: self.calculate_0_6y_method,
            2: self.calculate_0_8y_0_2y_method,
            3: self.calculate_surface_velocity_method,
        }
        return methods.get(
            self.method, lambda: print("Error: Invalid method selection") or None
        )()


if __name__ == "__main__":
    DischargeCalculator().calculate_discharge()
