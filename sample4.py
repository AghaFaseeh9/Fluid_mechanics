import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple

# Page configuration and theme settings
st.set_page_config(page_title="Fluid Mechanics Discharge Calculator", page_icon="🌊", layout="wide")
plt.style.use("dark_background")
sns.set_theme(style="darkgrid", palette="dark")
for param in ["figure.facecolor", "axes.facecolor", "grid.color", "text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
    plt.rcParams[param] = "#1a1a1a" if param in ["figure.facecolor", "axes.facecolor"] else "white"

class DischargeCalculator:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all calculator data"""
        self.depths = []
        self.velocities = []
        self.discharges = []
        self.widths = []
        self.areas = []

    def get_measurements(self, point_num: int):
        """Get width and depth measurements for a point"""
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
        """Calculate area using average depth * width"""
        return ((depth1 + depth2) / 2) * width

    def plot_schematic(self, method_name: str):
        """Plot schematic diagram with velocity arrows"""
        try:
            fig, ax = plt.subplots(figsize=(12, 6), facecolor="#1a1a1a")
            ax.set_facecolor("#1a1a1a")
            ax.set_title(f"Schematic Diagram - {method_name}", color="white", pad=20)
            ax.set_xlabel("Position across stream (20 ft interval)", color="white")
            ax.set_ylabel("Depth (ft)", color="white")
            ax.invert_yaxis()

            positions = [i * 20 for i in range(len(self.depths))]
            stream_bed = [min(d1, d2) for d1, d2 in self.depths]

            # Plot stream bed and water area
            ax.plot(positions, stream_bed, color="#00ffff", linewidth=2, label="Stream Bed")
            
            # Plot water area and velocity arrows
            for i, ((d1, d2), x) in enumerate(zip(self.depths, positions)):
                avg_depth = (d1 + d2) / 2
                # Water area
                ax.fill_between([x - 5, x + 5], 0, avg_depth, color="#005577", alpha=0.5, 
                              label="Water Area" if i == 0 else None)
                
                # Velocity arrows
                if method_name == "0.6Y Method":
                    v1, v2 = self.velocities[i]
                    vel = (v1 + v2) / 2
                    color = "#ffcc00"
                    label = "Velocity (0.6Y)" if i == 0 else None
                elif method_name == "0.8Y/0.2Y Method":
                    v1, v2, v3, v4 = self.velocities[i]
                    vel = ((v1 + v3) / 2 + (v2 + v4) / 2) / 2
                    color = "#00ffcc"
                    label = "Velocity (0.8Y/0.2Y)" if i == 0 else None
                else:  # Surface Velocity Method
                    vel = st.session_state.get("surf_vel", 0)
                    color = "#ff00ff"
                    label = "Surface Velocity" if i == 0 else None

                ax.arrow(x, avg_depth / 2, 0, -vel, head_width=2, head_length=0.5,
                        fc=color, ec=color, label=label)

            ax.grid(True, alpha=0.3)
            legend = ax.legend(facecolor="#1a1a1a", edgecolor="#333333", fontsize=12)
            for text in legend.get_texts():
                text.set_color("white")

            st.pyplot(fig)
            plt.close(fig)

        except Exception as e:
            st.error(f"Error creating schematic: {e}")

    def display_section_results(self, section_num: int, area: float, velocities: dict, section_q: float, total_q: float):
        """Display results for a section"""
        st.info(f"Section {section_num} Results:")
        st.info(f"  Area: {round(area, 3)} sq ft")
        for name, value in velocities.items():
            st.info(f"  {name}: {round(value, 3)} ft/s")
        st.info(f"  Section discharge: {round(section_q, 3)} cusecs")
        st.info(f"Total discharge so far: {round(total_q, 3)} cusecs")

    def calculate_0_6y_method(self, n_points: int):
        """Calculate discharge using 0.6Y method"""
        total_q = 0
        st.subheader("0.6Y Method Measurements")
        section_areas, section_velocities, section_discharges = [], [], []

        for i in range(n_points):
            st.write(f"--- Measurement Point {i+1} ---")
            width, depth1, depth2 = self.get_measurements(i + 1)
            
            col1, col2 = st.columns(2)
            with col1:
                vel1 = st.number_input("Velocity at 0.6Y depth, first point (ft/s)", min_value=0.0, 
                                     key=f"06y_vel1_point{i+1}")
            with col2:
                vel2 = st.number_input("Velocity at 0.6Y depth, second point (ft/s)", min_value=0.0, 
                                     key=f"06y_vel2_point{i+1}")

            area = self.calc_area(width, depth1, depth2)
            avg_velocity = (vel1 + vel2) / 2
            section_q = area * avg_velocity
            
            section_areas.append(area)
            section_velocities.append(avg_velocity)
            section_discharges.append(section_q)
            total_q += section_q

            self.display_section_results(i+1, area, {"Average velocity": avg_velocity}, section_q, total_q)

        self.areas = section_areas
        self.velocities = [(v, v) for v in section_velocities]
        self.discharges = [total_q]
        self.plot_schematic("0.6Y Method")
        return total_q

    def calculate_0_8y_0_2y_method(self, n_points: int):
        """Calculate discharge using 0.8Y/0.2Y method"""
        total_q = 0
        st.subheader("0.8Y/0.2Y Method Measurements")
        section_areas, section_velocities, section_discharges = [], [], []

        for i in range(n_points):
            st.write(f"--- Measurement Point {i+1} ---")
            width, depth1, depth2 = self.get_measurements(i + 1)
            
            # Get velocities at 0.8Y depth
            st.write("Velocity measurements at 0.8Y depth:")
            col1, col2 = st.columns(2)
            with col1:
                vel_08_1 = st.number_input("Velocity at 0.8Y depth, first point (ft/s)", min_value=0.0, 
                                         key=f"08y_vel1_point{i+1}")
            with col2:
                vel_08_2 = st.number_input("Velocity at 0.8Y depth, second point (ft/s)", min_value=0.0, 
                                         key=f"08y_vel2_point{i+1}")

            # Get velocities at 0.2Y depth
            st.write("Velocity measurements at 0.2Y depth:")
            col3, col4 = st.columns(2)
            with col3:
                vel_02_1 = st.number_input("Velocity at 0.2Y depth, first point (ft/s)", min_value=0.0, 
                                         key=f"02y_vel1_point{i+1}")
            with col4:
                vel_02_2 = st.number_input("Velocity at 0.2Y depth, second point (ft/s)", min_value=0.0, 
                                         key=f"02y_vel2_point{i+1}")

            area = self.calc_area(width, depth1, depth2)
            avg_vel_08 = (vel_08_1 + vel_08_2) / 2
            avg_vel_02 = (vel_02_1 + vel_02_2) / 2
            avg_velocity = (avg_vel_08 + avg_vel_02) / 2
            section_q = area * avg_velocity

            section_areas.append(area)
            section_velocities.append((vel_08_1, vel_08_2, vel_02_1, vel_02_2))
            section_discharges.append(section_q)
            total_q += section_q

            self.display_section_results(i+1, area, 
                {"Average velocity at 0.8Y": avg_vel_08, 
                 "Average velocity at 0.2Y": avg_vel_02,
                 "Final average velocity": avg_velocity}, 
                section_q, total_q)

        self.areas = section_areas
        self.velocities = section_velocities
        self.discharges = [total_q]
        self.plot_schematic("0.8Y/0.2Y Method")
        return total_q

    def calculate_surface_velocity_method(self, n_points: int):
        """Calculate discharge using surface velocity method"""
        st.subheader("Surface Velocity Method Measurements")
        
        col1, col2 = st.columns(2)
        with col1:
            conv_factor = st.number_input("Surface velocity conversion factor", min_value=0.0, max_value=1.0,
                                        value=0.85, key="surf_conv_factor")
        with col2:
            surf_vel = st.number_input("Measured surface velocity (ft/s)", min_value=0.0, key="surf_vel")

        total_q = 0
        section_areas, section_discharges = [], []

        for i in range(n_points):
            st.write(f"--- Measurement Point {i+1} ---")
            width, depth1, depth2 = self.get_measurements(i + 1)
            
            area = self.calc_area(width, depth1, depth2)
            section_q = conv_factor * area * surf_vel
            
            section_areas.append(area)
            section_discharges.append(section_q)
            total_q += section_q

            self.display_section_results(i+1, area, 
                {"Surface velocity": surf_vel, "Conversion factor": conv_factor}, 
                section_q, total_q)

        self.areas = section_areas
        self.velocities = [(surf_vel, surf_vel) for _ in range(n_points)]
        self.discharges = [total_q]
        self.plot_schematic("Surface Velocity Method")
        return total_q

def main():
    st.title("🌊 Fluid Mechanics Discharge Calculator")
    
    st.sidebar.header("Calculation Method")
    method = st.sidebar.radio("Select method:", 
                            ["0.6Y Method", "0.8Y/0.2Y Average Method", "Surface Velocity Method"])
    
    n_points = st.sidebar.number_input("Number of measurement points", min_value=1, value=2)
    
    calculator = DischargeCalculator()
    
    if 'current_method' not in st.session_state:
        st.session_state.current_method = method
    elif st.session_state.current_method != method:
        calculator.reset()
        st.session_state.current_method = method
        st.rerun()

    if method == "0.6Y Method":
        calculator.calculate_0_6y_method(n_points)
    elif method == "0.8Y/0.2Y Average Method":
        calculator.calculate_0_8y_0_2y_method(n_points)
    else:
        calculator.calculate_surface_velocity_method(n_points)

if __name__ == "__main__":
    main()
