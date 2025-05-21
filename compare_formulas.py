import pandas as pd
import numpy as np

def read_excel_formulas():
    try:
        # Read the Excel file
        df = pd.read_excel('fm cep excel.xlsx')
        print("Excel Formulas:")
        print(df)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def compare_calculations():
    # Test values
    width = 20.0  # ft
    depth1 = 4.833  # ft (4'-10")
    depth2 = 3.833  # ft (3'-10")
    vel1 = 2.5  # ft/s
    vel2 = 2.3  # ft/s
    
    # Area calculation
    area = ((depth1 + depth2) / 2) * width
    print(f"\nArea calculation:")
    print(f"Width: {width} ft")
    print(f"Depths: {depth1} ft, {depth2} ft")
    print(f"Area = (({depth1} + {depth2})/2) * {width} = {area:.3f} sq ft")
    
    # 0.6Y Method
    avg_vel = (vel1 + vel2) / 2
    q_06y = area * avg_vel
    print(f"\n0.6Y Method:")
    print(f"Velocities: {vel1} ft/s, {vel2} ft/s")
    print(f"Average velocity = ({vel1} + {vel2})/2 = {avg_vel:.3f} ft/s")
    print(f"Discharge = {area:.3f} * {avg_vel:.3f} = {q_06y:.3f} cusecs")
    
    # 0.8Y/0.2Y Method
    vel_08_1, vel_08_2 = 2.6, 2.4  # ft/s at 0.8Y
    vel_02_1, vel_02_2 = 2.3, 2.1  # ft/s at 0.2Y
    avg_vel_08 = (vel_08_1 + vel_08_2) / 2
    avg_vel_02 = (vel_02_1 + vel_02_2) / 2
    avg_velocity = (avg_vel_08 + avg_vel_02) / 2
    q_08y_02y = area * avg_velocity
    print(f"\n0.8Y/0.2Y Method:")
    print(f"0.8Y velocities: {vel_08_1} ft/s, {vel_08_2} ft/s")
    print(f"0.2Y velocities: {vel_02_1} ft/s, {vel_02_2} ft/s")
    print(f"Average at 0.8Y = ({vel_08_1} + {vel_08_2})/2 = {avg_vel_08:.3f} ft/s")
    print(f"Average at 0.2Y = ({vel_02_1} + {vel_02_2})/2 = {avg_vel_02:.3f} ft/s")
    print(f"Final average = ({avg_vel_08:.3f} + {avg_vel_02:.3f})/2 = {avg_velocity:.3f} ft/s")
    print(f"Discharge = {area:.3f} * {avg_velocity:.3f} = {q_08y_02y:.3f} cusecs")
    
    # Surface Velocity Method
    conv_factor = 0.85
    surf_vel = 3.0  # ft/s
    q_surface = conv_factor * area * surf_vel
    print(f"\nSurface Velocity Method:")
    print(f"Conversion factor: {conv_factor}")
    print(f"Surface velocity: {surf_vel} ft/s")
    print(f"Area: {area:.3f} sq ft")
    print(f"Discharge = {conv_factor} * {area:.3f} * {surf_vel} = {q_surface:.3f} cusecs")
    print(f"Step by step:")
    print(f"1. Area = (({depth1} + {depth2})/2) * {width} = {area:.3f} sq ft")
    print(f"2. Discharge = {conv_factor} * {area:.3f} * {surf_vel} = {q_surface:.3f} cusecs")

if __name__ == "__main__":
    print("Comparing formulas between Excel and Python code...")
    excel_data = read_excel_formulas()
    if excel_data is not None:
        compare_calculations() 