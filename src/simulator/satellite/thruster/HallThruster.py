import math

class HallThruster:
    '''Simple model of Hall Thruster'''
    def __init__(self, power, specific_impulse, mass_flow_rate):
        self.power = power # Power in watts
        self.specific_impulse = specific_impulse # Specific impulse in seconds
        self.mass_flow_rate = mass_flow_rate # Mass flow rate in kg/s
        
        self.thrust = None # Thrust in Newtons
        self.delta_v = None # Delta-V in m/s
        
    def calculate_thrust(self):
        e = 1.602e-19 # Elementary charge in Coulombs
        m_i = 4.48e-25 # Mass of ion in kg
        B = 1.2 # Magnetic field strength in Tesla
        L = 0.5 # Length of channel in meters
        R = 0.2 # Radius of channel in meters
        V = math.sqrt((2*self.power)/(self.mass_flow_rate*math.pi*R**2)) # Exhaust velocity in m/s
        isp = V/9.81 # Specific impulse in seconds
        
        ion_current = self.mass_flow_rate/m_i # Ion current in Amps
        thrust = ion_current*V*B*L # Thrust in Newtons
        
        self.thrust = thrust
        self.delta_v = isp*9.81
        
        return thrust
    
    def claculate