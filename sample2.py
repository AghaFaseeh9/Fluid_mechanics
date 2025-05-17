import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple
import sys


class DischargeCalculator:
    def __init__(self):
        # Set dark theme
        plt.style.use("dark_background")
        sns.set_theme(style="darkgrid", palette="dark")
        plt.rcParams["figure.facecolor"] = "#1a1a1a"
        plt.rcParams["axes.facecolor"] = "#1a1a1a"
        plt.rcParams["grid.color"] = "#333333"
        plt.rcParams["text.color"] = "white"
        plt.rcParams["axes.labelcolor"] = "white"
        plt.rcParams["xtick.color"] = "white"
        plt.rcParams["ytick.color"] = "white"

        self.n_points = int(input("Number of measurement points: "))
        print("\nSelect method:")
        print("1. 0.6Y Method")
        print("2. 0.8Y/0.2Y Average Method")
        print("3. Surface Velocity Method")
        self.method = int(input("Enter method (1-3): "))

        # Initialize data storage
        self.depths: List[Tuple[float, float]] = []
        self.velocities: List[Tuple[float, float]] = []
        self.discharges: List[float] = []
        self.widths: List[float] = []
        self.areas: List[float] = []

    def get_measurements(self):
        width = float(input("Width between points (ft): "))
        depth1 = float(input("Depth at first point (ft): "))
        depth2 = float(input("Depth at second point (ft): "))
        self.widths.append(width)
        self.depths.append((depth1, depth2))
        return width, depth1, depth2

    def calc_area(self, width, depth1, depth2):
        return ((depth1 + depth2) / 2) * width

    def plot_results(self, method_name: str):
        try:
            plt.figure(figsize=(10, 6), facecolor="#1a1a1a")

            points = range(1, len(self.depths) + 1)

            if method_name == "0.6Y Method":
                # Plot velocity and discharge for 0.6Y method
                vel1 = [v[0] for v in self.velocities]
                vel2 = [v[1] for v in self.velocities]
                plt.plot(
                    points,
                    vel1,
                    "o-",
                    label="First Point Velocity",
                    color="#00ff00",
                    linewidth=2,
                )
                plt.plot(
                    points,
                    vel2,
                    "o-",
                    label="Second Point Velocity",
                    color="#ff00ff",
                    linewidth=2,
                )
                plt.plot(
                    points,
                    self.discharges,
                    "o--",
                    label="Discharge",
                    color="#ff4500",
                    linewidth=2,
                )
                plt.title("0.6Y Method - Velocity and Discharge", color="white", pad=20)
                plt.ylabel(
                    "Velocity (ft/s) / Discharge (cusecs)", color="white", labelpad=10
                )

            elif method_name == "0.8Y/0.2Y Method":
                # Plot average velocities and discharge for 0.8Y/0.2Y method
                vel_08_1 = [v[0] for v in self.velocities]
                vel_08_2 = [v[1] for v in self.velocities]
                vel_02_1 = [v[2] for v in self.velocities]
                vel_02_2 = [v[3] for v in self.velocities]
                avg_vels = [
                    ((v1 + v2) / 2 + (v3 + v4) / 2) / 2
                    for v1, v2, v3, v4 in zip(vel_08_1, vel_08_2, vel_02_1, vel_02_2)
                ]
                plt.plot(
                    points,
                    avg_vels,
                    "o-",
                    label="Average Velocity",
                    color="#00ff00",
                    linewidth=2,
                )
                plt.plot(
                    points,
                    self.discharges,
                    "o--",
                    label="Discharge",
                    color="#ff4500",
                    linewidth=2,
                )
                plt.title(
                    "0.8Y/0.2Y Method - Average Velocity and Discharge",
                    color="white",
                    pad=20,
                )
                plt.ylabel(
                    "Velocity (ft/s) / Discharge (cusecs)", color="white", labelpad=10
                )

            else:  # Surface Velocity Method
                # Plot cross-sectional area and discharge for surface method
                plt.plot(
                    points,
                    self.areas,
                    "o-",
                    label="Cross-sectional Area",
                    color="#00ff00",
                    linewidth=2,
                )
                plt.plot(
                    points,
                    self.discharges,
                    "o--",
                    label="Discharge",
                    color="#ff4500",
                    linewidth=2,
                )
                plt.title(
                    "Surface Velocity Method - Area and Discharge",
                    color="white",
                    pad=20,
                )
                plt.ylabel(
                    "Area (sq ft) / Discharge (cusecs)", color="white", labelpad=10
                )

            plt.xlabel("Measurement Point", color="white", labelpad=10)
            plt.grid(True, alpha=0.2, linestyle="--")
            plt.legend(facecolor="#1a1a1a", edgecolor="#333333")

            # Add padding around the plot
            plt.tight_layout(pad=2.0)
            plt.show()

        except KeyboardInterrupt:
            print("\nPlot closed by user")
            sys.exit(0)
        except Exception as e:
            print(f"\nError displaying plot: {e}")
            sys.exit(1)

    def calculate_0_6y_method(self):
        total_q = 0
        for _ in range(self.n_points):
            width, depth1, depth2 = self.get_measurements()
            vel1, vel2 = float(input("Velocity at first point (ft/s): ")), float(
                input("Velocity at second point (ft/s): ")
            )
            self.velocities.append((vel1, vel2))
            total_q += self.calc_area(width, depth1, depth2) * (vel1 + vel2) / 2
            self.discharges.append(total_q)
            print(f"Current discharge (0.6Y): {round(total_q, 3)} cusecs")
        self.plot_results("0.6Y Method")
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
            self.velocities.append((vel_08_1, vel_08_2, vel_02_1, vel_02_2))
            avg_vel = ((vel_08_1 + vel_02_1) / 2 + (vel_08_2 + vel_02_2) / 2) / 2
            total_q += self.calc_area(width, depth1, depth2) * avg_vel
            self.discharges.append(total_q)
            print(f"Current discharge (0.8Y/0.2Y): {round(total_q, 4)} cusecs")
        self.plot_results("0.8Y/0.2Y Method")
        return total_q

    def calculate_surface_velocity_method(self):
        conv_factor, surf_vel = float(
            input("Surface velocity conversion factor: ")
        ), float(input("Measured surface velocity (ft/s): "))
        total_area = 0
        for _ in range(self.n_points):
            width, depth1, depth2 = self.get_measurements()
            area = self.calc_area(width, depth1, depth2)
            self.areas.append(area)
            total_area += area
            total_q = conv_factor * total_area * surf_vel
            self.discharges.append(total_q)
            print(f"Total discharge (surface): {round(total_q, 4)} cusecs")
        self.plot_results("Surface Velocity Method")
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
    try:
        DischargeCalculator().calculate_discharge()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
