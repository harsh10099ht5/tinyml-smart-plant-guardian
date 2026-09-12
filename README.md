# TinyML Smart Plant Guardian 🌱

An ESP32-based smart plant monitoring and decision-support system that uses sensor data and Machine Learning to estimate plant-condition states and trigger appropriate actions.

The project combines **Embedded Systems, Machine Learning, IoT concepts, and Edge AI** in a low-cost hardware prototype.

---

## 📌 Project Overview

Plants require suitable soil moisture, temperature, and humidity for healthy growth. Traditional automatic watering systems often rely on fixed thresholds, which may not adapt well to changing environmental conditions.

The **TinyML Smart Plant Guardian** collects environmental data using sensors and uses a lightweight machine-learning model to classify predefined plant-condition states.

Based on the predicted state, the system can:

- Display sensor readings and plant-condition predictions.
- Alert the user when watering may be required.
- Activate a low-voltage water pump through a control circuit.
- Perform inference locally on an ESP32 without requiring continuous cloud connectivity.

> **Important:** This is an educational prototype. The model predicts predefined sensor-based condition labels; it does not medically or scientifically diagnose plant health.

---

## 🎯 Project Objectives

1. Learn how to interface sensors with an ESP32.
2. Collect and organize real-world sensor data.
3. Build a labeled dataset for machine learning.
4. Train and evaluate a classification model using Python.
5. Deploy a lightweight model or embedded decision logic.
6. Control physical hardware based on model predictions.
7. Understand the limitations of ML models in real-world environments.
8. Document the complete hardware and software workflow.

---

## ✨ Features

- Real-time soil-moisture monitoring.
- Temperature and humidity measurement.
- Sensor-data logging in CSV format.
- Machine-learning-based classification.
- Local inference on a microcontroller.
- OLED display support.
- LED and buzzer alerts.
- Optional automatic watering using a low-voltage pump.
- Modular design for future improvements.

---

## 🧠 Machine Learning Approach

### Problem Type

Supervised learning — multiclass classification.

### Input Features

The initial model uses sensor and contextual features:

| Feature | Description |
|---|---|
| `soil_moisture` | Raw analog value from the soil sensor |
| `temperature` | Temperature in degrees Celsius |
| `humidity` | Relative humidity percentage |
| `hours_since_watering` | Approximate time since the last watering |

### Target Classes

| Class | Description |
|---|---|
| `healthy` | Sensor conditions fall within the defined suitable range |
| `needs_water` | Soil is relatively dry and watering may be required |
| `stress_risk` | Sensor conditions indicate a potentially unfavorable environment |

The class definitions must be established before labeling the dataset. They should be adapted to the selected plant species and growing conditions.

### Candidate Models

The project can begin with:

1. Decision Tree Classifier
2. Random Forest Classifier
3. Logistic Regression as a baseline
4. Small quantized neural network as an advanced TinyML extension

The first implementation should use a Decision Tree or Random Forest because these models are practical for small tabular datasets.

---

## 🏗️ System Architecture

```text
             ┌─────────────────────────┐
             │       Plant Pot         │
             └────────────┬────────────┘
                          │
             ┌────────────▼────────────┐
             │     Sensor Layer        │
             │                         │
             │  Soil Moisture Sensor   │
             │  DHT11 Temperature      │
             │  DHT11 Humidity         │
             └────────────┬────────────┘
                          │
                          ▼
             ┌─────────────────────────┐
             │       ESP32             │
             │                         │
             │  Data Acquisition       │
             │  Feature Preparation    │
             │  ML Inference           │
             └────────────┬────────────┘
                          │
                          ▼
             ┌─────────────────────────┐
             │   Plant Condition       │
             │   Classification        │
             └────────────┬────────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
       ┌──────────┐ ┌──────────┐ ┌──────────────┐
       │  OLED    │ │  Alerts  │ │ Water Pump   │
       │ Display  │ │ LED/Buzz │ │ Optional     │
       └──────────┘ └──────────┘ └──────────────┘
```

---

## 🔩 Hardware Components

### Required Components

| No. | Component | Purpose |
|---|---|---|
| 1 | ESP32 DevKit V1 | Main microcontroller |
| 2 | Capacitive soil-moisture sensor | Measures soil moisture |
| 3 | DHT11 sensor module | Measures temperature and humidity |
| 4 | Breadboard | Circuit prototyping |
| 5 | Jumper wires | Electrical connections |
| 6 | USB cable | Programming and power |
| 7 | LEDs | Status indication |
| 8 | Resistors | Current limiting |
| 9 | Buzzer | Audio alert |
| 10 | Plant pot and soil | Experimental setup |

### Optional Components

| Component | Purpose |
|---|---|
| 0.96-inch I2C OLED | Display readings and predictions |
| 5 V mini water pump | Automatic watering |
| Relay module or MOSFET driver | Pump switching |
| Water container | Water reservoir |
| Silicone tubing | Water delivery |
| External 5 V supply | Pump power |

---

## 💰 Estimated Budget

| Component Group | Approximate Cost |
|---|---:|
| ESP32 development board | ₹400–₹500 |
| Soil-moisture sensor | ₹100–₹180 |
| DHT11 module | ₹50–₹100 |
| Breadboard and jumper wires | ₹150–₹250 |
| OLED display | ₹100–₹180 |
| LEDs, buzzer and resistors | ₹50–₹100 |
| Plant pot and miscellaneous materials | ₹50–₹150 |
| **Estimated base prototype** | **₹900–₹1,460** |

An optional pump, driver circuit, tubing, and power supply may increase the total cost.

The final cost depends on the supplier, shipping charges, and the components selected.

---

## 🔌 Circuit Connections

The following pin mapping assumes an ESP32 DevKit V1, a 3.3 V-compatible capacitive moisture sensor, a DHT11 module, and a standard I2C OLED.

### Soil Moisture Sensor

| Sensor Pin | ESP32 Pin |
|---|---|
| VCC | 3V3 |
| GND | GND |
| AOUT | GPIO 34 |

### DHT11 Module

| DHT11 Pin | ESP32 Pin |
|---|---|
| VCC | 3V3 |
| GND | GND |
| DATA | GPIO 4 |

### OLED Display

| OLED Pin | ESP32 Pin |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

### LED Indicator

| LED Connection | ESP32 |
|---|---|
| GPIO through resistor | GPIO 2 |
| LED cathode | GND |

Use a suitable current-limiting resistor, such as 220 Ω.

### Buzzer

| Buzzer Connection | ESP32 |
|---|---|
| Positive terminal | GPIO 25 through a suitable driver if required |
| Negative terminal | GND |

Check whether the buzzer is an active or passive type and whether its current requirement is safe for direct GPIO operation.

---

## ⚠️ Pump Circuit and Safety

The pump must not be powered directly from an ESP32 GPIO pin.

Use a suitable transistor/MOSFET driver or compatible relay module.

### Recommended Pump Architecture

```text
ESP32 GPIO
    │
    ▼
MOSFET / Relay Driver
    │
    ▼
External Low-Voltage Supply
    │
    ▼
5 V Water Pump
```

Important safety rules:

- Use a suitable low-voltage DC pump.
- Use a separate supply capable of providing the pump's startup current.
- Connect the ESP32 and driver grounds when required by the driver design.
- Add a flyback diode when using a suitable DC motor switching circuit.
- Keep water away from the ESP32, breadboard, and exposed wiring.
- Do not use mains electricity.
- Test the pump control circuit without water before final assembly.

---

## 💻 Software Requirements

### Programming Languages

- Python
- C/C++ for ESP32 firmware

### Development Tools

- Arduino IDE
- Visual Studio Code
- Git
- GitHub

### Python Libraries

- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- Joblib
- PySerial

### Arduino Libraries

- DHT sensor library
- Adafruit Unified Sensor
- Wire
- Adafruit SSD1306
- Adafruit GFX Library

Install the Python dependencies:

```bash
pip install numpy pandas scikit-learn matplotlib joblib pyserial
```

---

## 📁 Project Structure

```text
tinyml-smart-plant-guardian/
│
├── data/
│   ├── raw_sensor_data.csv
│   ├── cleaned_sensor_data.csv
│   └── README.md
│
├── ml/
│   ├── collect_data.py
│   ├── preprocess_data.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── export_model.py
│   └── requirements.txt
│
├── firmware/
│   ├── sensor_test/
│   │   └── sensor_test.ino
│   ├── data_logger/
│   │   └── data_logger.ino
│   └── smart_plant/
│       └── smart_plant.ino
│
├── hardware/
│   ├── circuit_diagram.png
│   └── wiring_notes.md
│
├── docs/
│   ├── project_report.md
│   ├── experiments.md
│   └── results.md
│
├── README.md
└── .gitignore
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/tinyml-smart-plant-guardian.git
cd tinyml-smart-plant-guardian
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Python Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r ml/requirements.txt
```

### 4. Configure Arduino IDE

1. Install Arduino IDE.
2. Open Preferences.
3. Add ESP32 board support using the official Espressif Arduino installation instructions.
4. Select the appropriate ESP32 board.
5. Select the correct COM port.
6. Upload a test program.

Official documentation:

https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html

---

## 🧪 Development Workflow

### Phase 1: Hardware Testing

- Test ESP32 connectivity.
- Test soil-moisture sensor readings.
- Test DHT11 readings.
- Verify OLED display.
- Test LED and buzzer.
- Check power stability.

### Phase 2: Data Collection

Collect readings from the sensors and store them in CSV format.

Example dataset:

```csv
soil_moisture,temperature,humidity,hours_since_watering,label
2350,28.4,62.0,5.0,healthy
2700,29.1,58.0,12.0,needs_water
3100,31.5,42.0,24.0,stress_risk
```

> These values are illustrative only. Do not use them as a real training dataset.

Collect actual readings from the selected plant and label them using predefined criteria.

### Phase 3: Data Preprocessing

Tasks:

- Remove invalid readings.
- Handle missing values.
- Check sensor ranges.
- Analyze class distribution.
- Detect abnormal readings.
- Split the dataset into training and testing sets.

### Phase 4: Model Training

Train a baseline model using scikit-learn.

Recommended starting model:

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)
```

Train the model using the collected sensor data.

### Phase 5: Model Evaluation

Evaluate the model using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

Do not report accuracy without explaining the dataset size, class distribution, and test methodology.

### Phase 6: Embedded Deployment

Possible deployment approaches:

1. Export a shallow Decision Tree as C++ decision rules.
2. Use a compact neural network and a supported TinyML runtime.
3. Quantize the model if required.
4. Implement feature preparation consistently with training.
5. Run inference on the ESP32.

The deployed model must use the same feature order, units, and preprocessing assumptions as the training pipeline.

### Phase 7: Physical Control

Use the model output to:

- Display the predicted state.
- Activate a warning LED.
- Sound a buzzer when appropriate.
- Trigger a low-voltage pump only after safety checks.

For the first prototype, use a manual watering confirmation or LED indicator instead of automatic watering.

---

## 🧠 Example Model Training Code

The following is a baseline training example.

```python
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("../data/cleaned_sensor_data.csv")

features = [
    "soil_moisture",
    "temperature",
    "humidity",
    "hours_since_watering"
]

X = df[features]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(classification_report(y_test, predictions))

joblib.dump(model, "plant_model.pkl")

print("Model saved successfully.")
```

This code requires a real CSV dataset with valid labels. It is not a substitute for data collection or model validation.

---

## 📊 Evaluation and Experimentation

The project should record experimental results.

### Suggested Experiments

| Experiment | Purpose |
|---|---|
| Baseline Decision Tree | Establish initial performance |
| Random Forest | Compare with an ensemble model |
| Different tree depths | Study model complexity |
| Feature removal | Identify useful sensors |
| Sensor calibration | Improve data quality |
| Environmental variation | Test robustness |
| Embedded inference | Validate deployment |

### Results Table

Complete this table after experimentation:

| Metric | Result |
|---|---|
| Dataset size | To be measured |
| Number of classes | 3 |
| Training samples | To be measured |
| Testing samples | To be measured |
| Accuracy | To be measured |
| Macro F1-score | To be measured |
| Inference time | To be measured |
| Model size | To be measured |

---

## 📏 Sensor Calibration

Raw soil-moisture sensor readings are not universal.

Calibration procedure:

1. Insert the sensor into dry soil.
2. Record the raw value.
3. Insert the sensor into adequately moist soil.
4. Record the raw value.
5. Repeat measurements several times.
6. Check whether the sensor reading increases or decreases with moisture.
7. Use the observed range consistently in the dataset and firmware.

Avoid assuming that a raw reading of 2000 always means a particular moisture percentage.

The capacitive sensor should be calibrated for the specific soil and pot used in the experiment.

---

## 🔍 Limitations

- Soil-moisture readings depend on soil type and sensor placement.
- DHT11 has limited accuracy and resolution.
- The model depends on the quality of the labeled dataset.
- Sensor-based classes do not directly identify plant diseases.
- A small dataset may not generalize to different plants or environments.
- Environmental conditions can change rapidly.
- Automatic watering can damage plants if the model makes incorrect predictions.
- The initial system does not use image-based plant disease detection.

---

## 🚀 Future Improvements

- Add a light-intensity sensor.
- Add a water-level sensor.
- Add an ESP32-CAM for image classification.
- Train a compact neural network.
- Deploy a quantized TensorFlow Lite Micro model.
- Add a web dashboard.
- Store historical data.
- Add MQTT-based IoT communication.
- Add solar-powered operation.
- Improve plant-specific calibration.
- Compare model performance across multiple plant species.
- Implement confidence-based alerts.
- Add manual override for pump control.

---

## 📚 Learning Outcomes

By completing this project, the developer will gain experience in:

### Machine Learning

- Data collection
- Data cleaning
- Feature engineering
- Classification
- Model evaluation
- Model deployment

### Embedded Systems

- ESP32 programming
- GPIO and ADC
- I2C communication
- Sensor interfacing
- Power management
- Actuator control

### Software Engineering

- Python project organization
- Git and GitHub
- Version control
- Documentation
- Experiment tracking
- Reproducible development

---

## 🛠️ Troubleshooting

### ESP32 is not detected

- Check the USB cable.
- Try another USB port.
- Install the appropriate USB-to-serial driver.
- Select the correct COM port.
- Check the board selection in Arduino IDE.

### Soil sensor readings are unstable

- Check the power supply.
- Verify common ground.
- Keep wires short.
- Calibrate the sensor.
- Average multiple readings.
- Avoid placing the sensor near the pot edge.

### DHT11 returns NaN

- Check the DATA connection.
- Verify the correct GPIO pin.
- Confirm the sensor type.
- Add an appropriate delay between readings.
- Check the module's wiring.

### OLED is blank

- Verify SDA and SCL connections.
- Check the I2C address.
- Confirm the display voltage.
- Check the correct display dimensions.
- Scan the I2C bus if necessary.

### Model performs poorly

- Check class labels.
- Increase the quality and diversity of the dataset.
- Check class imbalance.
- Verify sensor calibration.
- Compare baseline models.
- Use a held-out test set.
- Avoid data leakage.

---

## 📜 License

This project is intended for educational and portfolio purposes.

Choose an appropriate open-source license before publishing the final project.

---

## 👨‍💻 Author

**Name:** YOUR_NAME

**Role:** Engineering Student | AI/ML Enthusiast

**GitHub:** https://github.com/YOUR_USERNAME

**Project:** TinyML Smart Plant Guardian

---

## ⭐ Acknowledgements

- Arduino and ESP32 community
- Python and scikit-learn developers
- Open-source embedded systems community
- TinyML and Edge AI learning resources

---

## 📌 Project Status

**Current status:** Planning and hardware prototyping

Future milestones:

- [ ] Purchase components
- [ ] Test ESP32
- [ ] Test sensors
- [ ] Build data logger
- [ ] Collect real dataset
- [ ] Train baseline model
- [ ] Evaluate model
- [ ] Deploy embedded inference
- [ ] Integrate OLED
- [ ] Add safe pump control
- [ ] Record demonstration
- [ ] Publish final results
