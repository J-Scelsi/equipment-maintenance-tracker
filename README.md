Equipment Maintenance Tracker (Python OOP Demo)

This command-line application is a demonstration of Object-Oriented Programming (OOP) in Python, designed to track the location, status, and repair history of physical assets.

This project directly connects real-world troubleshooting experience (from roles as an Automotive Technician and Computer Lab Manager) to foundational software design principles.

🛠️ Technical Focus

Object-Oriented Programming (OOP): Implementation of primary classes (Asset and RepairLog) using encapsulation, methods, and properties to model real-world objects.

Data Persistence (Serialization): Uses Python's built-in json module to serialize (save) and deserialize (load) complex object data to and from a local JSON file (assets_data.json).

Data Structure Management: Manages asset data in a dynamic list of Python objects within memory.

User Interaction: Simple Command-Line Interface (CLI) for data input and retrieval.

🚀 How to Run the Tracker

Clone the Repository:

git clone [https://github.com/J-Scelsi/equipment-maintenance-tracker.git](https://github.com/J-Scelsi/equipment-maintenance-tracker.git)
cd equipment-maintenance-tracker


Execute the Script:

python asset_tracker.py


(The script will automatically create assets_data.json if it doesn't exist.)

✨ Application Features

The application provides a menu-driven interface with the following capabilities:

Add New Asset: Creates a new Asset object with a unique ID, name, type, and location.

Log Repair/Maintenance: Updates an asset's repair history by creating and attaching a new RepairLog object. It can also automatically update the asset's status (e.g., to "Active" or "Under Repair") based on the description.

View Asset Details: Searches and displays all historical repair logs for a single asset via ID or keyword search (Name/Type/Location).

View All Assets (Summary): Prints a clean, formatted summary table of all assets currently in the system.
