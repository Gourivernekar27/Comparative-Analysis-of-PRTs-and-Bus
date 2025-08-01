import os
import pandas as pd
import matplotlib.pyplot as plt

# Print the current working directory to verify the script's location
print("Current working directory:", os.getcwd())

# File names for bus limit 50 and 80
bus_limit_50_files = [
    "exp3_passengerdata_50_392.csv",
    "exp3_passengerdata_50_896.csv",
    "exp3_passengerdata_50_2968.csv",
    "exp3_passengerdata_50_4032.csv",
    "exp3_passengerdata_50_5040.csv",
    "exp3_passengerdata_50_7952.csv",
]

bus_limit_80_files = [
    "exp3_passengerdata_80_392.csv",
    "exp3_passengerdata_80_896.csv",
    "exp3_passengerdata_80_2968.csv",
    "exp3_passengerdata_80_4032.csv",
    "exp3_passengerdata_80_5040.csv",
    "exp3_passengerdata_80_7952.csv",
]

# Pod file names (first pod system)
pod_files = [
    "processed_392_pod_3.csv",
    "processed_896_pod_3.csv",
    "processed_2968_pod_3.csv",
    "processed_4032_pod_3.csv",
    "processed_5040_pod_3.csv",
    "processed_7952_pod_3.csv",
]

# Pod-optimized file names
pod_opt_files = [
    "processed_Excel392[3]_allocations.csv",
    "processed_Excel896[3]_allocations.csv",
    "processed_Excel2968[3]_allocations.csv",
    "processed_Excel4032[3]_allocations.csv",
    "processed_Excel5040[3]_allocations.csv",
    "processed_Excel7952[3]_allocations.csv",
]

# Function to calculate average waiting_time for any file
def get_average_waiting_time(file_name):
    try:
        df = pd.read_csv(file_name)
        df.columns = df.columns.str.strip()  # Trim spaces

        if 'waiting_time' not in df.columns:
            print(f"Error: 'waiting_time' column missing in {file_name}.")
            return None

        # Ensure column is numeric
        df['waiting_time'] = pd.to_numeric(df['waiting_time'], errors='coerce')

        # Drop NaN values
        df = df.dropna(subset=['waiting_time'])

        # Return average
        return df['waiting_time'].mean()

    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{file_name}': {e}")
        return None

# Unified passenger counts for the x-axis
passenger_counts = [392, 896, 2968, 4032, 5040, 7952]

# Calculate average waiting times for all systems
avg_waiting_time_50 = [get_average_waiting_time(file) for file in bus_limit_50_files]
avg_waiting_time_80 = [get_average_waiting_time(file) for file in bus_limit_80_files]
avg_waiting_time_pod = [get_average_waiting_time(file) for file in pod_files]
avg_waiting_time_pod_opt = [get_average_waiting_time(file) for file in pod_opt_files]

# Check for any processing errors
if None in avg_waiting_time_50 or None in avg_waiting_time_80 or None in avg_waiting_time_pod or None in avg_waiting_time_pod_opt:
    print("Warning: Some files could not be processed. Please check the errors above.")

# Plot all four series on the same graph
plt.figure(figsize=(12, 7))
plt.plot(passenger_counts, avg_waiting_time_50, marker='o', linestyle='-', color='blue', label='Bus, passenger limit 50')
plt.plot(passenger_counts, avg_waiting_time_80, marker='s', linestyle='-', color='green', label='Bus, passenger limit 80')
plt.plot(passenger_counts, avg_waiting_time_pod, marker='^', linestyle='-', color='red', label='Pods, uniformly distributed across stops')
plt.plot(passenger_counts, avg_waiting_time_pod_opt, marker='d', linestyle='-', color='purple', label='Pods, optimally distributed across stops')

plt.axhline(y=1800, color='black', linestyle=':', label='30 min (1800s)')
# Labels and title
plt.title('Experiment 3: Average Waiting Time vs. Number of Passengers (with Optimised Pod)')
plt.xlabel('Number of Passengers')
plt.ylabel('Average Passenger Waiting Time(seconds)')
plt.grid(True)
plt.xticks(passenger_counts)
plt.legend()
plt.show()

# Save the plot
plt.savefig('average_waiting_time_comparison_exp3_pod_opt.png')

# Show the plot
plt.show()