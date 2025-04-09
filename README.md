# AR-Glasses-for-Scenic-Spots-Based-on-Posture-Measurement
Head Positioning and Posture Measurement System Based on Augmented Reality Near-Eye Display


Project Overview
This project is a head positioning and posture measurement system based on augmented reality (AR) technology. It leverages sensor data and image processing to achieve precise head positioning and posture detection. The system is developed using Python and C++, integrating a graphical user interface (GUI), database management, serial communication, image processing, and Kalman filtering.

Features
User Management: Supports user registration and login, with user data stored in a SQL Server database.
Posture Measurement: Collects head posture data using the JY901 sensor and smooths it with Kalman filtering.
*Positioning: Performs accurate head positioning using GPS data and image processing techniques.
Graphical Interface: Provides an intuitive GUI for easy operation and data visualization.
Motor Control: Controls a stepper motor via Raspberry Pi to automatically adjust head position.

Technology Stack
Frontend: Tkinter (Python GUI library)
Backend: Python (GUI, serial communication, image processing), C++ (sensor data processing, motor control)
Database: SQL Server
Hardware: Raspberry Pi, JY901 sensor, stepper motor, GPS module

Installation and Setup

 1. Prerequisites
Python Version: 3.8 or higher
C++ Compiler: g++ (supporting C++11)
Database: SQL Server (pre-installed and configured)
Hardware: Raspberry Pi (with WiringPi library installed), JY901 sensor, stepper motor, GPS module

2. Install Dependencies

Python Dependencies
Run the following command to install required Python libraries:

```bash
pip install tkinter pillow pyproj opencv-python pymssql matplotlib
```

C++ Dependencies
Install the WiringPi library for Raspberry Pi GPIO control:

```bash
sudo apt-get install wiringpi
```

3. Database Configuration

Create a database named `test` in SQL Server and set up the `ID` table:

```sql
CREATE TABLE ID (
    username VARCHAR(50),
    password VARCHAR(50),
    userpwd VARCHAR(100)
);
```

Update the database connection settings in `gui.py` to match your SQL Server configuration, e.g.:

```python
conn = pymssql.connect('YourServerName', 'Username', 'Password', 'test')
```

4. Compile C++ Code

 Place the C++ files (`Kalman.h`, `Kalman.cpp`, `JY901.h`, `JY901.cpp`, `main.cpp`) in the same directory.
 Compile the code to generate the `kaltest` executable:

```bash
g++ -o kaltest main.cpp Kalman.cpp JY901.cpp -lwiringPi
```

Move the generated `kaltest` executable to the `/home/pi/Desktop/kal2/` directory.

Usage

1. Launch the System

Start the Python GUI program:

```bash
python gui.py
```

The system will display a login interface. Enter your username and password to log in, or click "Register" to create a new user.

2. Posture Measurement

After logging in, click the "Posture Measurement" button to enter the posture measurement interface.
Click "Run" to invoke `kaltest`, retrieve JY901 sensor data, and display it in the GUI's receiving area.
Input data to calculate slopes and visualize posture changes in a graph.

3. Positioning

From the main interface, select the "Positioning" button to enter positioning mode.
Enter position and distance data, then click "Calculate" to perform two-point or three-point positioning.
The system will display inferred points and positioning results, while also retrieving GPS data via serial port for display.

4. Motor Control

During posture measurement, the system automatically controls the stepper motor based on sensor data to adjust head position.

Notes

Ensure the Raspberry Pi is properly connected to the JY901 sensor, stepper motor, and GPS module.
Verify that image paths and serial device paths in the code match your setup; adjust if necessary.
Confirm that database connection details align with your SQL Server configuration.
Before running the program, ensure the C++ executable `kaltest` is compiled and located in the specified path.
