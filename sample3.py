import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple
import sys

# Set page config
st.set_page_config(
    page_title="Fluid Mechanics Discharge Calculator",
    page_icon="🌊",
    layout="wide"
)

# Set dark theme for plots
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
        # Initialize data storage
        self.depths: List[Tuple[float, float]] = []
        self.velocities: List[Tuple[float, float]] = []
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
        return ((depth1 + depth2) / 2) * width

    def plot_results(self, method_name: str):
        try:
            fig = plt.figure(figsize=(10, 6), facecolor="#1a1a1a")
            points = range(1, len(self.depths) + 1)

            if method_name == "0.6Y Method":
                vel1 = [v[0] for v in self.velocities]
                vel2 = [v[1] for v in self.velocities]
                plt.plot(points, vel1, "o-", label="First Point Velocity", color="#00ff00", linewidth=2)
                plt.plot(points, vel2, "o-", label="Second Point Velocity", color="#ff00ff", linewidth=2)
                plt.plot(points, self.discharges, "o--", label="Discharge", color="#ff4500", linewidth=2)
                plt.title("0.6Y Method - Velocity and Discharge", color="white", pad=20)
                plt.ylabel("Velocity (ft/s) / Discharge (cusecs)", color="white", labelpad=10)

            elif method_name == "0.8Y/0.2Y Method":
                vel_08_1 = [v[0] for v in self.velocities]
                vel_08_2 = [v[1] for v in self.velocities]
                vel_02_1 = [v[2] for v in self.velocities]
                vel_02_2 = [v[3] for v in self.velocities]
                avg_vels = [((v1 + v2) / 2 + (v3 + v4) / 2) / 2 
                           for v1, v2, v3, v4 in zip(vel_08_1, vel_08_2, vel_02_1, vel_02_2)]
                plt.plot(points, avg_vels, "o-", label="Average Velocity", color="#00ff00", linewidth=2)
                plt.plot(points, self.discharges, "o--", label="Discharge", color="#ff4500", linewidth=2)
                plt.title("0.8Y/0.2Y Method - Average Velocity and Discharge", color="white", pad=20)
                plt.ylabel("Velocity (ft/s) / Discharge (cusecs)", color="white", labelpad=10)

            else:  # Surface Velocity Method
                plt.plot(points, self.areas, "o-", label="Cross-sectional Area", color="#00ff00", linewidth=2)
                plt.plot(points, self.discharges, "o--", label="Discharge", color="#ff4500", linewidth=2)
                plt.title("Surface Velocity Method - Area and Discharge", color="white", pad=20)
                plt.ylabel("Area (sq ft) / Discharge (cusecs)", color="white", labelpad=10)

            plt.xlabel("Measurement Point", color="white", labelpad=10)
            plt.grid(True, alpha=0.2, linestyle="--")
            plt.legend(facecolor="#1a1a1a", edgecolor="#333333")
            plt.tight_layout(pad=2.0)
            
            st.pyplot(fig)
            plt.close(fig)

        except Exception as e:
            st.error(f"Error displaying plot: {e}")

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
            total_q += self.calc_area(width, depth1, depth2) * (vel1 + vel2) / 2
            self.discharges.append(total_q)
            st.info(f"Current discharge (0.6Y): {round(total_q, 3)} cusecs")
        
        self.plot_results("0.6Y Method")
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
            avg_vel = ((vel_08_1 + vel_02_1) / 2 + (vel_08_2 + vel_02_2) / 2) / 2
            total_q += self.calc_area(width, depth1, depth2) * avg_vel
            self.discharges.append(total_q)
            st.info(f"Current discharge (0.8Y/0.2Y): {round(total_q, 4)} cusecs")
        
        self.plot_results("0.8Y/0.2Y Method")
        return total_q

    def calculate_surface_velocity_method(self, n_points: int):
        col1, col2 = st.columns(2)
        with col1:
            conv_factor = st.number_input("Surface velocity conversion factor", min_value=0.0)
        with col2:
            surf_vel = st.number_input("Measured surface velocity (ft/s)", min_value=0.0)
        
        total_area = 0
        for i in range(n_points):
            width, depth1, depth2 = self.get_measurements(i + 1)
            area = self.calc_area(width, depth1, depth2)
            self.areas.append(area)
            total_area += area
            total_q = conv_factor * total_area * surf_vel
            self.discharges.append(total_q)
            st.info(f"Total discharge (surface): {round(total_q, 4)} cusecs")
        
        self.plot_results("Surface Velocity Method")
        return total_q

def main():
    st.title("🌊 Fluid Mechanics Discharge Calculator")
    
    # Sidebar for method selection
    st.sidebar.header("Calculation Method")
    method = st.sidebar.radio(
        "Select method:",
        ["0.6Y Method", "0.8Y/0.2Y Average Method", "Surface Velocity Method"]
    )
    
    # Number of measurement points
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
