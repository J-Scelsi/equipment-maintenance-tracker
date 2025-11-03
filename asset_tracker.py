import json
import os
from datetime import datetime

# --- Configuration ---
DATA_FILE = "assets_data.json"

class RepairLog:
    """Represents a single maintenance or repair action."""
    def __init__(self, date, description, technician="System"):
        # We store the date as a formatted string
        self.date = date
        self.description = description
        self.technician = technician

    def __str__(self):
        """String representation for display."""
        return f"[{self.date} by {self.technician}]: {self.description}"

class Asset:
    """Represents a physical asset (e.g., Computer Component, Automotive Part).
    This class is the foundation of our OOP structure.
    """
    next_id = 1
    
    def __init__(self, name, asset_type, location, status="Active"):
        # Assign a unique ID using the class variable and increment it
        self.asset_id = Asset.next_id
        Asset.next_id += 1
        
        self.name = name
        self.asset_type = asset_type
        self.location = location
        self.status = status # e.g., 'Active', 'Under Repair', 'Retired'
        self.repair_history = [] # Stores a list of RepairLog objects

    def log_repair(self, description, technician="Self"):
        """Creates a new RepairLog object and adds it to the history."""
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        log = RepairLog(date_str, description, technician)
        self.repair_history.append(log)
        
    def __str__(self):
        """String representation for printing asset details."""
        return f"ID: {self.asset_id} | Name: {self.name} | Type: {self.asset_type} | Status: {self.status}"

def initialize_tracker():
    """Loads existing asset data from the JSON file or starts a new list."""
    global ASSET_LIST
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                
                # --- DESERIALIZATION ---
                ASSET_LIST = []
                max_id = 0
                for d in data:
                    # Recreate the Asset object from the dictionary data
                    asset = Asset(d['name'], d['asset_type'], d['location'], d['status'])
                    asset.asset_id = d['asset_id']
                    
                    # Recreate RepairLog objects for history
                    asset.repair_history = [
                        RepairLog(r['date'], r['description'], r['technician'])
                        for r in d['repair_history']
                    ]
                    
                    ASSET_LIST.append(asset)
                    if d['asset_id'] > max_id:
                        max_id = d['asset_id']
                
                # Update the class ID counter to avoid ID conflicts
                Asset.next_id = max_id + 1
                
                print(f"Loaded {len(ASSET_LIST)} assets from {DATA_FILE}.")
                
        except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
            print(f"Error loading data: {e}. Starting with empty asset list.")
            ASSET_LIST = []
    else:
        ASSET_LIST = []
        print("Starting with empty asset list.")

def save_tracker():
    """Saves the current ASSET_LIST to the JSON file (Serialization)."""
    # Custom encoding logic is needed because we can't save the raw object list
    data_to_save = []
    for asset in ASSET_LIST:
        # Convert the complex object structure into a simple dictionary for JSON
        asset_dict = {
            'asset_id': asset.asset_id,
            'name': asset.name,
            'asset_type': asset.asset_type,
            'location': asset.location,
            'status': asset.status,
            # Convert repair_history (list of RepairLog objects) to list of dictionaries
            'repair_history': [log.__dict__ for log in asset.repair_history]
        }
        data_to_save.append(asset_dict)

    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print(f"\n[Success] Data saved to {DATA_FILE}.")
    except Exception as e:
        print(f"\n[Error] Failed to save data: {e}")

def main_menu():
    """Displays the main command-line menu."""
    print("\n" + "="*40)
    print("  Equipment Maintenance Tracker (OOP Demo)")
    print("="*40)
    print("1. Add New Asset (Hardware/Part)")
    print("2. Log Repair/Maintenance")
    print("3. View Asset Details (ID/Search)")
    print("4. View All Assets (Summary)")
    print("5. Exit and Save")
    
    choice = input("Enter your choice (1-5): ")
    return choice


# --- Main Execution Loop ---
if __name__ == "__main__":
    # Global list to hold all Asset objects in memory
    global ASSET_LIST 
    ASSET_LIST = []

    initialize_tracker()
    
    # We will add the implementation functions (1, 2, 3, 4) in the next step
    while True:
        choice = main_menu()
        
        if choice == '1':
            print("\n[WIP] Adding asset functionality coming soon!")
        elif choice == '2':
            print("\n[WIP] Logging repair functionality coming soon!")
        elif choice == '3':
            print("\n[WIP] Viewing asset details coming soon!")
        elif choice == '4':
            print("\n[WIP] Viewing all assets functionality coming soon!")
        elif choice == '5':
            save_tracker()
            print("Exiting Tracker. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 5.")
