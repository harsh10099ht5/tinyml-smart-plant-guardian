import csv
import time
from pathlib import Path

import serial


# --------------------------------------------------
# Configuration
# --------------------------------------------------

SERIAL_PORT = "COM3"       # Apna ESP32 COM port yahan likho
BAUD_RATE = 115200
COLLECTION_TIME = 60       # Data collection time in seconds

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"
CSV_PATH = DATA_FOLDER / "sensors_reading.csv"


# --------------------------------------------------
# Create data folder
# --------------------------------------------------

DATA_FOLDER.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Connect to ESP32
# --------------------------------------------------

try:
    esp32 = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        timeout=2
    )

    time.sleep(2)

    print("Connected to ESP32 successfully.")
    print(f"Collecting data for {COLLECTION_TIME} seconds...\n")

except serial.SerialException as error:
    print("Could not connect to ESP32.")
    print(f"Error: {error}")
    print("Check your COM port and USB connection.")
    raise SystemExit


# --------------------------------------------------
# Create CSV file
# --------------------------------------------------

file_exists = CSV_PATH.exists()

with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "soil_moisture",
            "temperature",
            "humidity",
            "hours_since_watering",
            "label"
        ])

    start_time = time.time()

    while time.time() - start_time < COLLECTION_TIME:

        try:
            raw_data = esp32.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not raw_data:
                continue

            print(f"Received: {raw_data}")

            # Expected ESP32 output:
            # 45,28.5,65.0,2.0

            values = raw_data.split(",")

            if len(values) != 4:
                print("Invalid data format. Skipping...")
                continue

            soil_moisture = float(values[0])
            temperature = float(values[1])
            humidity = float(values[2])
            hours_since_watering = float(values[3])

            print("\nSelect plant condition:")
            print("1. Healthy")
            print("2. Needs Water")
            print("3. Excess Water")
            print("4. Unfavorable Temperature")

            label_choice = input("Enter label number: ").strip()

            labels = {
                "1": "Healthy",
                "2": "Needs Water",
                "3": "Excess Water",
                "4": "Unfavorable Temperature"
            }

            if label_choice not in labels:
                print("Invalid label. Data skipped.\n")
                continue

            label = labels[label_choice]

            writer.writerow([
                soil_moisture,
                temperature,
                humidity,
                hours_since_watering,
                label
            ])

            file.flush()

            print(f"Saved: {label}\n")

        except ValueError:
            print("Could not convert sensor data into numbers.")

        except KeyboardInterrupt:
            print("\nData collection stopped by user.")
            break


# --------------------------------------------------
# Close Serial connection
# --------------------------------------------------

esp32.close()

print("\nData collection completed.")
print(f"Dataset saved at: {CSV_PATH}")