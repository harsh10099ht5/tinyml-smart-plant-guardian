from pathlib import Path
import time

import joblib
import serial


# --------------------------------------------------
# Configuration
# --------------------------------------------------

SERIAL_PORT = "COM3"      # Apna ESP32 COM port set karo
BAUD_RATE = 115200

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "ml" / "plant_model.pkl"


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "plant_model.pkl not found. First run train_model.py"
    )

saved_data = joblib.load(MODEL_PATH)

model = saved_data["model"]
features = saved_data["features"]

print("Trained model loaded successfully.")
print(f"Features: {features}")


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

    print(f"Connected to ESP32 on {SERIAL_PORT}")
    print("Waiting for sensor data...\n")

except serial.SerialException as error:
    print("Could not connect to ESP32.")
    print(f"Error: {error}")
    print("Check the COM port and USB connection.")
    raise SystemExit


# --------------------------------------------------
# Live prediction loop
# --------------------------------------------------

try:
    while True:
        raw_data = esp32.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not raw_data:
            continue

        # Ignore ESP32 status messages and CSV header
        if not raw_data[0].isdigit():
            continue

        values = raw_data.split(",")

        if len(values) != 4:
            print(f"Invalid data received: {raw_data}")
            continue

        try:
            soil_moisture = float(values[0])
            temperature = float(values[1])
            humidity = float(values[2])
            hours_since_watering = float(values[3])

        except ValueError:
            print("Invalid numeric data received.")
            continue

        sensor_data = [[
            soil_moisture,
            temperature,
            humidity,
            hours_since_watering
        ]]

        prediction = model.predict(sensor_data)[0]

        print("----------------------------------")
        print(f"Soil Moisture: {soil_moisture:.1f}%")
        print(f"Temperature: {temperature:.1f} °C")
        print(f"Humidity: {humidity:.1f}%")
        print(f"Hours Since Watering: {hours_since_watering:.1f}")
        print(f"Plant Condition: {prediction}")
        print("----------------------------------\n")

except KeyboardInterrupt:
    print("\nLive prediction stopped by user.")

finally:
    esp32.close()
    print("Serial connection closed.")