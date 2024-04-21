import platform
import psutil
import os
from datetime import timedelta, datetime
import socket
import time
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Data structure to store collected parameters
data_collection = []

# Function to retrieve basic OS information
def get_os_info():
    os_name = platform.system()
    os_version = platform.version()
    processor_info = platform.processor()
    memory_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    disk_gb = round(psutil.disk_usage('/').free / (1024 ** 3), 2)
    current_user = platform.node()
    return os_name, os_version, processor_info, memory_gb, disk_gb, current_user

# Function to retrieve the IP address of the system
def get_ip_address():
    ip = socket.gethostbyname(socket.gethostname())
    return ip

# Function to retrieve the system uptime
def get_system_uptime():
    uptime_seconds = round(psutil.boot_time(), 0)
    uptime_delta = timedelta(seconds=uptime_seconds)
    uptime_str = str(uptime_delta)
    uptime_time = uptime_str.split(', ')[-1]
    return uptime_time

# Function to retrieve CPU usage
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent()
    return cpu_usage

# Function to retrieve running processes
def get_running_processes():
    running_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        running_processes.append((proc.info['pid'], proc.info['name'], proc.info['memory_percent']))
    return running_processes

# Function to retrieve disk partitions
def get_disk_partitions():
    disk_partitions = psutil.disk_partitions()
    return disk_partitions

# Function to retrieve environment variables
def get_environment_variables():
    environment_variables = os.environ
    return environment_variables

# Main function for data collection and analysis
def main():
    while True:
        os_name, os_version, processor_info, memory_gb, disk_gb, current_user = get_os_info()
        ip_address = get_ip_address()
        system_uptime = get_system_uptime()
        cpu_usage = get_cpu_usage()
        running_processes = get_running_processes()
        disk_partitions = get_disk_partitions()
        environment_variables = get_environment_variables()

        data_collection.append({
            "OS": {
                "Name": os_name,
                "Version": os_version,
                "Processor": processor_info,
                "Memory_GB": memory_gb,
                "Disk_GB": disk_gb,
                "User": current_user
            },
            "Network": {
                "IP_Address": ip_address
            },
            "Uptime": system_uptime,
            "CPU_Usage": cpu_usage,
            "Processes": running_processes,
            "Disk_Partitions": disk_partitions,
            "Environment_Variables": environment_variables
        })

        # Collect data every minute
        time.sleep(60)

        # Analyze data after collecting for a certain period (10 minutes for demonstration)
        if len(data_collection) >= 10:
            analyze_data()
            break

# Function to analyze collected data
def analyze_data():
    # Analyzing CPU Usage over Time
    cpu_data = [(datetime.now() - timedelta(minutes=i), data['CPU_Usage']) for i, data in enumerate(data_collection)]
    timestamps, cpu_usages = zip(*cpu_data)

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_usages, marker='o', linestyle='-')
    plt.title('CPU Usage Over Time')
    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.tight_layout()
    plt.show()

    # Analyzing Memory Usage by Processes
    process_data = {}
    for data in data_collection:
        for pid, name, memory_percent in data['Processes']:
            if name not in process_data:
                process_data[name] = []
            process_data[name].append(memory_percent)

    avg_memory_usage = {name: sum(memory_percent) / len(memory_percent) for name, memory_percent in process_data.items()}
    sorted_avg_memory = sorted(avg_memory_usage.items(), key=lambda x: x[1], reverse=True)

    print("Process with the highest average memory usage:")
    print(sorted_avg_memory[0])

    # Analyzing Available Disk Space over Time
    disk_data = [(datetime.now() - timedelta(minutes=i), data['OS']['Disk_GB']) for i, data in enumerate(data_collection)]
    timestamps, disk_space = zip(*disk_data)

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, disk_space, marker='o', linestyle='-')
    plt.title('Available Disk Space Over Time')
    plt.xlabel('Time')
    plt.ylabel('Available Disk Space (GB)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().yaxis.grid(True, linestyle='--')  # Add gridlines for the y-axis
    plt.tight_layout()
    plt.show()

    # Calculating Peak CPU Usage
    peak_cpu_usage = max(cpu_usages)
    print("Peak CPU Usage:", peak_cpu_usage)

    # Calculating Average Available Disk Space
    avg_disk_space = sum(disk_space) / len(disk_space)
    print("Average Available Disk Space:", avg_disk_space)

if __name__ == "__main__":
    main()




