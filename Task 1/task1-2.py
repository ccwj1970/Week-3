import os
import urllib.request as request
import json
import csv

# Define the file path and file name
folder_path = "Task 1"  # Replace 'your_folder_path' with your folder path
file_path = os.path.join(folder_path, "mrt.csv")

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

# Write to CSV file
with open(file_path, "w", encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(["StationName", "AttractionTitle1", "AttractionTitle2", "AttractionTitle3", "AttractionTitle4", "AttractionTitle5", "AttractionTitle6"])

    
    # Create a dictionary to store data for each MRT station
    mrt_data = {}
    
    # Loop through slist1 to organize data by MRT station
    for item1 in slist1:
        SERIAL_NO1 = item1.get("SERIAL_NO", "")
        stitle1 = item1.get("stitle", "")
        
        # Loop through slist2 to find matching MRT
        for item2 in slist2:
            SERIAL_NO2 = item2.get("SERIAL_NO", "")
            MRT = item2.get("MRT", "")
    
            # If SERIAL NO matches, group by MRT station
            if SERIAL_NO1 == SERIAL_NO2:
                if MRT not in mrt_data:
                    mrt_data[MRT] = [stitle1]
                else:
                    mrt_data[MRT].append(stitle1)
    
    # Write the data to CSV, grouping by MRT station
    for mrt, stitles in mrt_data.items():
      writer.writerow([mrt] + [stitle.strip('"') for stitle in stitles])


print(f"Results have been written to {file_path}")
