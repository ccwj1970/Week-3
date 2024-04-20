import os
import csv
import urllib.request as request 
import json 

# Define the file path and file name
folder_path = "Task 1"  # Replace 'your_folder_path' with your folder path
file_path = os.path.join(folder_path, "spot.csv")

# First URL
src1 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"

with request.urlopen(src1) as response: 
    data1 = json.load(response)  # Process JSON data format using the json module

# Second URL
src2 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

with request.urlopen(src2) as response: 
    data2 = json.load(response)  # Process JSON data format using the json module

# Extract data from both URLs
slist1 = data1["data"]["results"]
slist2 = data2["data"]
combined_slist = slist1 + slist2

# Create a dictionary to store SERIAL_NO and corresponding address from src2
serial_no_address_map = {}

# Iterate through data2 to populate the dictionary
for item in slist2:
    serial_no = item["SERIAL_NO"]
    address = item["address"]
    district = address.split("  ")[1][0:3] if address else ""
    serial_no_address_map[serial_no] = district


# Sort slist1 based on the stitle
sorted_slist1 = sorted(slist1, key=lambda x: x["stitle"])

# Write to CSV file
with open(file_path, "w", encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(["SpotTitle", "District", "Longitude", "Latitude", "FirstImageURL"])

    # Write the spot titles, district, longitude, latitude, and first image URL
    for spot in sorted_slist1: 
        serial_no = spot.get("SERIAL_NO", "")
        spot_title = spot.get("stitle", "")
        district = serial_no_address_map.get(serial_no, "")
        longitude = spot.get("longitude", "")
        latitude = spot.get("latitude", "")
        image_urls = spot.get("filelist", "").split("https://")
        first_image_url = "http://" + image_urls[1]
        writer.writerow([spot_title, district, longitude, latitude, first_image_url])

print(f"Spot information from both URLs has been written to {file_path}")