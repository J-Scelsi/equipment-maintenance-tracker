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

    def to_dict(self):
        """Converts object to dictionary for JSON serialization."""
        return self.__dict__

class Asset:
    """Represents a physical asset (e.g., Computer Component, Automotive Part)."""
    next_id = 1
    
    def __init__(self, name, asset_type, location, status="Active"):
        # Assign a unique ID using the class variable and increment it
        self.asset_id = Asset.next_id
        Asset.next_id += 1
        
        self.name = name
        self.asset_type = asset_type
        self.location = location
        self.status = status 
        self.repair_history = [] # Stores a list of RepairLog objects

    def log_repair(self, description, technician="Self"):
        """Creates a new RepairLog object and adds it to the history."""
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        log = RepairLog(date_str, description, technician)
        self.repair_history.append(log)
        self.status = "Active" if "fixed" in description.lower() else self.status
        
    def __str__(self):
        """String representation for printing asset details."""
        return f"ID: {self.asset_id:<4} | Name: {self.name:<20} | Type: {self.asset_type:<15} | Status: {self.status}"

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
    data_to_save = []
    for asset in ASSET_LIST:
        asset_dict = {
            'asset_id': asset.asset_id,
            'name': asset.name,
            'asset_type': asset.asset_type,
            'location': asset.location,
            'status': asset.status,
            'repair_history': [log.to_dict() for log in asset.repair_history]
        }
        data_to_save.append(asset_dict)

    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print(f"\n[Success] Data saved to {DATA_FILE}.")
    except Exception as e:
        print(f"\n[Error] Failed to save data: {e}")

def add_new_asset():
    """Implements menu option 1: Collects input and creates a new Asset object."""
    print("\n--- Add New Asset ---")
    name = input("Asset Name (e.g., 'Laptop Power Supply'): ").strip()
    asset_type = input("Asset Type (e.g., 'Hardware', 'Tool', 'Vehicle Part'): ").strip()
    location = input("Location (e.g., 'Lab Shelf A', 'Garage Bay 3'): ").strip()

    if not all([name, asset_type, location]):
        print("[Error] All fields must be filled.")
        return

    new_asset = Asset(name, asset_type, location)
    ASSET_LIST.append(new_asset)
    print(f"\n[Success] Asset added: {new_asset}")
    
def find_asset(asset_id):
    """Utility function to find an asset by ID."""
    try:
        asset_id = int(asset_id)
        for asset in ASSET_LIST:
            if asset.asset_id == asset_id:
                return asset
        print(f"[Error] Asset with ID {asset_id} not found.")
        return None
    except ValueError:
        print("[Error] Invalid ID. Please enter a number.")
        return None

def log_asset_repair():
    """Implements menu option 2: Finds an asset and adds a RepairLog."""
    if not ASSET_LIST:
        print("\n[Warning] No assets in the system. Please add an asset first.")
        return
        
    print("\n--- Log Repair/Maintenance ---")
    asset_id = input("Enter Asset ID to log repair: ").strip()
    asset = find_asset(asset_id)

    if asset:
        description = input("Enter Repair Description (e.g., 'Replaced steering pump, status fixed'): ").strip()
        technician = input("Technician Name (or leave blank for 'Self'): ").strip() or "Self"
        
        asset.log_repair(description, technician)
        print(f"\n[Success] Repair logged for Asset ID {asset.asset_id} ({asset.name}).")
        if "fixed" in description.lower():
             asset.status = "Active"
             print(f"Status updated to: Active")
        elif "broken" in description.lower():
             asset.status = "Under Repair"
             print(f"Status updated to: Under Repair")
        else:
             print(f"Status remains: {asset.status}")


def view_asset_details():
    """Implements menu option 3: Views details of a specific asset."""
    if not ASSET_LIST:
        print("\n[Warning] No assets in the system.")
        return

    print("\n--- View Asset Details ---")
    query = input("Enter Asset ID or search keyword (Name/Type/Location): ").strip()
    
    found_assets = []
    
    # Try searching by ID first
    try:
        asset_id = int(query)
        asset = find_asset(asset_id)
        if asset:
            found_assets.append(asset)
    except ValueError:
        # Search by keyword if not an ID
        query_lower = query.lower()
        for asset in ASSET_LIST:
            if query_lower in asset.name.lower() or \
               query_lower in asset.asset_type.lower() or \
               query_lower in asset.location.lower():
                found_assets.append(asset)
    
    if not found_assets:
        print(f"[Warning] No assets found matching '{query}'.")
        return
        
    for asset in found_assets:
        print("\n" + "="*50)
        print(f"Asset ID: {asset.asset_id}")
        print(f"Name: {asset.name}")
        print(f"Type: {asset.asset_type}")
        print(f"Location: {asset.location}")
        print(f"Status: {asset.status}")
        print("-" * 50)
        print("Repair History:")
        if asset.repair_history:
            for log in asset.repair_history:
                print(f"  - {log}")
        else:
            print("  No repair history recorded.")
        print("="*50)

def view_all_assets():
    """Implements menu option 4: Prints a summary of all assets."""
    print("\n--- All Assets Summary ---")
    if not ASSET_LIST:
        print("[Warning] No assets in the system.")
        return
        
    print("ID   | Name                 | Type            | Status")
    print("-----|----------------------|-----------------|-----------------")
    for asset in ASSET_LIST:
        print(asset)
        
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
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            add_new_asset()
        elif choice == '2':
            log_asset_repair()
        elif choice == '3':
            view_asset_details()
        elif choice == '4':
            view_all_assets()
        elif choice == '5':
            save_tracker()
            print("Exiting Tracker. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 5.")
