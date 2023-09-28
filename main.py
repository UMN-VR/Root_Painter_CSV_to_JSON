# Import necessary modules
import csv
import json
import os
import shutil

# Set the paths to the input CSV file, the directory with the images, and the output directory
script_location = '/home/goldyosv7/Desktop/OpenCV-HTML-Demo/CSV-to-JSON/'
csv_filename = os.path.join(script_location, 'data/data.csv')
composites_directory = os.path.join(script_location, 'data/composites')
output_directory = os.path.join(script_location, 'output')

# Initialize the data structure to hold the data from the CSV file
crop_data = {}

# Open and read the CSV file
with open(csv_filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Process each row in the CSV file
    for row in csv_reader:
        # Extract the crop number and date from the file name
        file_name = row['file_name']
        crop_number = file_name[-4:]
        date = file_name[:8]
        area = float(row['area'])

        # Skip rows where the area is 3 or less
        if area <= 3:
            continue
        # Remove 'p' prefix from the crop number if present
        if crop_number.startswith('p'):
            crop_number = crop_number[1:]

        # Initialize data structures for new crop numbers and dates
        if crop_number not in crop_data:
            crop_data[crop_number] = {}
        if date not in crop_data[crop_number]:
            crop_data[crop_number][date] = []

        # Create a data entry for the current row, rounding the measurements as required
        entry = {
            'x': round(float(row['x']), 2),
            'y': round(float(row['y']), 2),
            'd': round(float(row['diameter']), 4),
            'a': round(float(row['area']), 4),
            'p': round(float(row['perimeter']), 4),
            'e': round(float(row['eccentricity']), 6)
        }
        
        # Add the entry to the data structure
        crop_data[crop_number][date].append(entry)

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Write the data to JSON files and move the corresponding images
for crop_number, data in crop_data.items():
    # Create a directory for each crop number
    crop_output_directory = os.path.join(output_directory, f'crop{crop_number}')
    os.makedirs(crop_output_directory, exist_ok=True)
    
    # Process each date for the current crop number
    for date, entries in data.items():
        # Write the data for the current date to a JSON file
        output_filename = os.path.join(crop_output_directory, f'{date}.json')
        with open(output_filename, 'w') as json_file:
            json.dump(entries, json_file, indent=1)
        print(f"JSON file created for crop {crop_number} on date {date}: {output_filename}")
        
        # Move the corresponding image to the crop number directory, renaming it to just the date
        original_image_path = os.path.join(composites_directory, f'{date}crop{crop_number}.jpg')
        new_image_path = os.path.join(crop_output_directory, f'{date}.jpg')
        
        # Use a try/except block to handle the case where the image file might not exist
        try:
            shutil.copy2(original_image_path, new_image_path)
        except FileNotFoundError:
            print(f"Warning: Image file not found: {original_image_path}")

print("All JSON files and images have been moved.")
