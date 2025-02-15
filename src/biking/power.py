from biking.conversions import kj2kcal


# Algorithm obtained from Duck.AI
def output_power(g, C_r, C_d, A, weight_lbs, elevation_gain_ft, speed_mph, distance_miles):
    # g is Acceleration due to gravity (m/s^2)
    # C_r is Rolling resistance coefficient for a cyclist
    # C_d is Drag coefficient for a cyclist
    # A is Frontal area in m^2

    # Unit conversions
    weight = weight_lbs * 0.453592
    elevation_gain = elevation_gain_ft * 0.3048
    speed = speed_mph * 0.44704
    distance = distance_miles * 1609.34

    time = distance / speed if speed else 0

    # force
    F_rr = C_r * weight * g  # force due to rolling resistance
    F_d = (1 / 2) * C_d * A * speed**2  # force due to air resistance
    F_g = weight * g * (elevation_gain / distance)  # force due to gravity, while climbing
    force = F_rr + F_d + F_g

    # power and energy
    power = force * speed
    energy_kj = power * time / 1000
    energy_kcal = kj2kcal(energy_kj)

    return power, energy_kj, energy_kcal
