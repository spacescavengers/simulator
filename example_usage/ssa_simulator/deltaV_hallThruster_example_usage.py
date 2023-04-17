from thruster.HallThruster import HallThruster
import math

g = 9.81 # standard acceleration due to gravity

# Set up a HallThruster object with the desired parameters
power = 2000 # Power in watts
specific_impulse = 2500 # Specific impulse in seconds
mass_flow_rate = 0.5 # Mass flow rate in kg/s
thruster = HallThruster(power, specific_impulse, mass_flow_rate)

# Calculate the thrust provided by the thruster (in Newtons)
thrust = thruster.calculate_thrust()

# Calculate the initial and final masses of the satellite
mass_satellite = 1000 # Mass of the satellite in kg
mass_propellant = 500 # Mass of the propellant in kg
m_initial = mass_satellite + mass_propellant
m_final = mass_satellite

# Calculate the delta-V provided by the thruster
delta_v = specific_impulse * g * math.log(m_initial / m_final)

print("Thrust: {:.2f} N".format(thrust))
print("Delta-V: {:.2f} m/s".format(delta_v))