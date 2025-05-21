import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple

# Page configuration
st.set_page_config(
    page_title="Fluid Mechanics Discharge Calculator",
    page_icon="🌊",
    layout="wide"
)

# Dark theme settings
plt.style.use("dark_background")
sns.set_theme(style="darkgrid", palette="dark")
plt.rcParams["figure.facecolor"] = "#1a1a1a"
plt.rcParams["axes.facecolor"] = "#1a1a1a"
plt.rcParams["grid.color"] = "#333333"
plt.rcParams["text.color"] = "white"
plt.rcParams["axes.labelcolor"] = "white"
plt.rcParams["xtick.color"] = "white"
plt.rcParams["ytick.color"] = "white"

class DischargeCalculator:
    def __init__(self):
        self.depths: List[Tuple[float, float]] = []
        self.velocities: List = []
        self.discharges: List[float] = []
        self.widths: List[float] = []
        self.areas: List[float] = []

    def get_measurements(self, point_num: int):
        st.subheader(f"Measurement Point {point_num}")
        col1, col2, col3 = st.columns(3)
        with col1:
            width = st.number_input("Width between points (ft)", min_value=0.0, key=f"width_{point_num}")
        with col2:
            depth1 = st.number_input("Depth at first point (ft)", min_value=0.0, key=f"depth1_{point_num}")
        with col3:
            depth2 = st.number_input("Depth at second point (ft)", min_value=0.0, key=f"depth2_{point_num}")

        self.widths.append(width)
        self.depths.append((depth1, depth2))
        return width, depth1, depth2

    def calc_area(self, width, depth1, depth2):
        # Area = average depth * width
        return ((depth1 + depth2) / 2) * width

    def plot_schematic(self, method_name: str):
        try:
            fig, ax = plt.subplots(figsize=(12, 6), facecolor="#1a1a1a")
            ax.set_facecolor("#1a1a1a")
            ax.set_title(f"Schematic Diagram - {method_name}", color="white", pad=20)
            ax.set_xlabel("Position across stream (20 ft interval)", color="white")
            ax.set_ylabel("Depth (ft)", color="white")
            ax.invert_yaxis()

            positions = [i * 20 for i in range(len(self.depths))]
            mid_depths = [(d1 + d2) / 2 for d1, d2 in self.depths]
            stream_bed = [min(d1, d2) for d1, d2 in self.depths]

            # Plot stream bed with label
            ax.plot(positions, stream_bed, color="#00ffff", linewidth=2, label="Stream Bed")

            # Fill water area with label (only add label to first fill for legend)
            for i, ((d1, d2), x) in enumerate(zip(self.depths, positions)):
                avg_depth = (d1 + d2) / 2
                if i == 0:
                    ax.fill_between([x - 5, x + 5], 0, avg_depth, color="#005577", alpha=0.5, label="Water Area")
                else:
                    ax.fill_between([x - 5, x + 5], 0, avg_depth, color="#005577", alpha=0.5)

                # Velocity arrows with method-specific color and label
                if method_name == "0.6Y Method":
                    v1, v2 = self.velocities[i]
                    vel = (v1 + v2) / 2
                    if i == 0:
                        ax.arrow(x, avg_depth / 2, 0, -vel, head_width=2, head_length=0.5, fc="#ffcc00", ec="#ffcc00", label="Velocity (0.6Y)")
                    else:
                        ax.arrow(x, avg_depth / 2, 0, -vel, head_width=2, head_length=0.5, fc="#ffcc00", ec="#ffcc00")
                elif method_name == "0.8Y/0.2Y Method":
                    v1, v2, v3, v4 = self.velocities[i]
                    vel = ((v1 + v3) / 2 + (v2 + v4) / 2) / 2
                    if i == 0:
                        ax.arrow(x, avg_depth / 2, 0, -vel, head_width=2, head_length=0.5, fc="#00ffcc", ec="#00ffcc", label="Velocity (0.8Y/0.2Y)")
                    else:
                        ax.arrow(x, avg_depth / 2, 0, -vel, head_width=2, head_length=0.5, fc="#00ffcc", ec="#00ffcc")
                else:  # Surface Velocity Method
                    surf_vel = self.discharges[-1] / sum(self.areas) if sum(self.areas) > 0 else 0
                    if i == 0:
                        ax.arrow(x, avg_depth / 2, 0, -surf_vel, head_width=2, head_length=0.5, fc="#ff00ff", ec="#ff00ff", label="Surface Velocity")
                    else:
                        ax.arrow(x, avg_depth / 2, 0, -surf_vel, head_width=2, head_length=0.5, fc="#ff00ff", ec="#ff00ff")

            ax.grid(True, alpha=0.3)
            # Add legend with white text
            legend = ax.legend(facecolor="#1a1a1a", edgecolor="#333333", fontsize=12)
            for text in legend.get_texts():
                text.set_color("white")

            st.pyplot(fig)
            plt.close(fig)

        except Exception as e:
            st.error(f"Error creating schematic: {e}")

    def calculate_0_6y_method(self, n_points: int):
        total_q = 0
        for i in range(n_points):
            width, depth1, depth2 = self.get_measurements(i + 1)
            col1, col2 = st.columns(2)
            with col1:
                vel1 = st.number_input("Velocity at first point (ft/s)", min_value=0.0, key=f"vel1_{i}")
            with col2:
                vel2 = st.number_input("Velocity at second point (ft/s)", min_value=0.0, key=f"vel2_{i}")

            self.velocities.append((vel1, vel2))
            # Area * Average Velocity
            area = self.calc_area(width, depth1, depth2)
            avg_velocity = (vel1 + vel2) / 2
            q = area * avg_velocity
            total_q += q
            self.discharges.append(total_q)
            st.info(f"Current discharge (0.6Y): {round(total_q, 3)} cusecs")

        self.plot_schematic("0.6Y Method")
        return total_q

    def calculate_0_8y_0_2y_method(self, n_points: int):
        total_q = 0
        for i in range(n_points):
            width, depth1, depth2 = self.get_measurements(i + 1)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                vel_08_1 = st.number_input("Velocity at 0.8Y depth, first point (ft/s)", min_value=0.0, key=f"vel_08_1_{i}")
            with col2:
                vel_08_2 = st.number_input("Velocity at 0.8Y depth, second point (ft/s)", min_value=0.0, key=f"vel_08_2_{i}")
            with col3:
                vel_02_1 = st.number_input("Velocity at 0.2Y depth, first point (ft/s)", min_value=0.0, key=f"vel_02_1_{i}")
            with col4:
                vel_02_2 = st.number_input("Velocity at 0.2Y depth, second point (ft/s)", min_value=0.0, key=f"vel_02_2_{i}")

            self.velocities.append((vel_08_1, vel_08_2, vel_02_1, vel_02_2))
            
            # Calculate average velocity using 0.8Y and 0.2Y method
            avg_vel_08 = (vel_08_1 + vel_08_2) / 2  # Average at 0.8Y
            avg_vel_02 = (vel_02_1 + vel_02_2) / 2  # Average at 0.2Y
            avg_velocity = (avg_vel_08 + avg_vel_02) / 2  # Final average velocity
            
            # Calculate discharge
            area = self.calc_area(width, depth1, depth2)
            q = area * avg_velocity
            total_q += q
            self.discharges.append(total_q)
            st.info(f"Current discharge (0.8Y/0.2Y): {round(total_q, 4)} cusecs")

        self.plot_schematic("0.8Y/0.2Y Method")
        return total_q

    def calculate_surface_velocity_method(self, n_points: int):
        col1, col2 = st.columns(2)
        with col1:
            conv_factor = st.number_input("Surface velocity conversion factor", min_value=0.0)
        with col2:
            surf_vel = st.number_input("Measured surface velocity (ft/s)", min_value=0.0)

        total_area = 0
        total_q = 0
        for i in range(n_points):
            width, depth1, depth2 = self.get_measurements(i + 1)
            area = self.calc_area(width, depth1, depth2)
            self.areas.append(area)
            total_area += area
            
            # Calculate discharge for this section
            q = conv_factor * area * surf_vel
            total_q += q
            self.discharges.append(total_q)
            st.info(f"Total discharge (surface): {round(total_q, 4)} cusecs")

        self.plot_schematic("Surface Velocity Method")
        return total_q

def main():
    st.title("🌊 Fluid Mechanics Discharge Calculator")

    st.sidebar.header("Calculation Method")
    method = st.sidebar.radio(
        "Select method:",
        ["0.6Y Method", "0.8Y/0.2Y Average Method", "Surface Velocity Method"]
    )

    n_points = st.sidebar.number_input("Number of measurement points", min_value=1, value=2)

    calculator = DischargeCalculator()

    if method == "0.6Y Method":
        calculator.calculate_0_6y_method(n_points)
    elif method == "0.8Y/0.2Y Average Method":
        calculator.calculate_0_8y_0_2y_method(n_points)
    else:
        calculator.calculate_surface_velocity_method(n_points)

if __name__ == "__main__":
    main()
