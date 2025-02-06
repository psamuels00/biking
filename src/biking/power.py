from biking.conversions import kj2kcal


# Algorithm obtained from Perplexity AI
def output_power(g, C_d, A, cyclist_weight_lbs, bike_weight_lbs, elevation_gain_ft, speed_mph, total_distance_miles):
    # g is Acceleration due to gravity (m/s^2)
    # C_d is Drag coefficient for a cyclist
    # A is Frontal area in m^2

    # Unit conversions
    cyclist_weight_kg = cyclist_weight_lbs * 0.453592
    bike_weight_kg = bike_weight_lbs * 0.453592
    elevation_gain_m = elevation_gain_ft * 0.3048
    speed_mps = speed_mph * 0.44704
    total_distance_m = total_distance_miles * 1609.34

    # Calculate total weight
    total_weight = cyclist_weight_kg + bike_weight_kg

    # Calculate gravitational force
    F_g = total_weight * g

    # Calculate time taken based on distance and speed
    time_seconds = total_distance_m / speed_mps

    # Calculate power due to elevation gain (climbing)
    P_climb = F_g * (elevation_gain_m / time_seconds)

    # Calculate power due to maintaining speed
    P_speed = C_d * A * (speed_mps**3) / 2

    # Total power output
    P_total = P_climb + P_speed

    # Calculate total energy output in kJ and calories
    energy_kilojoules = P_total * time_seconds / 1000
    energy_calories = kj2kcal(energy_kilojoules)

    return P_total, energy_kilojoules, energy_calories
