import os
import json
import zlib

def calculate_crc32(file_path):
    crc = 0
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):  # Read file in chunks
            crc = zlib.crc32(chunk, crc)
    return f"{crc & 0xFFFFFFFF:08X}"  # Return CRC32 as hexadecimal value

# Get user input for the paths and file settings
rom_root_dir = input("Enter the root directory of your ROMs: ")
output_dir = input("Enter the desired output directory for the playlist: ")
output_name = input("Enter the desired output file name (without extension): ")
file_extension = input("Enter the file extension to look for (e.g., .iso): ")
db_name = input("Enter the database name to use in the playlist: ")
use_crc32 = input("Do you want to calculate CRC32 checksums for the files? (yes/no): ").strip().lower() == "yes"

output_file = os.path.join(output_dir, f"{output_name}.lpl")  # Full path to the output .lpl file

# Initialize the playlist
playlist = {
    "version": "1.0",
    "default_core_path": "DETECT",
    "default_core_name": "DETECT",
    "label_display_mode": 0,
    "right_thumbnail_mode": 0,
    "left_thumbnail_mode": 0,
    "sort_mode": 0,
    "items": []
}

# Walk through the ROM directory and process files
for root, dirs, files in os.walk(rom_root_dir):
    for file in files:
        if file.endswith(file_extension):  # Check if the file has the specified extension
            full_path = os.path.join(root, file)  # Get the full path to the ROM file
            crc32_checksum = calculate_crc32(full_path) if use_crc32 else "DETECT"  # Calculate or skip CRC32 checksum
            
            item = {
                "path": full_path,  
                "label": os.path.splitext(file)[0],  
                "core_path": "DETECT",  
                "core_name": "DETECT", 
                "crc32": crc32_checksum,  
                "db_name": db_name  
            }
            # Add the ROM entry to the playlist items
            playlist["items"].append(item)
            
            # Print the CRC32 checksum or indicate detection for verification
            if use_crc32:
                print(f"Processed {file_extension} file: {full_path}")
                print(f"CRC32 checksum: {crc32_checksum} (decimal)")
            else:
                print(f"Processed {file_extension} file: {full_path} (CRC32: DETECT)")

# Write the playlist to the output file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(playlist, f, indent=4)  # Use indent=4 for pretty printing

print(f"\nPlaylist saved to {output_file}")  # Print a message indicating where the playlist was saved
