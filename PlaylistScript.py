import os
import json
import zlib
import zipfile

def calculate_crc32(file_path):
    """Calculate the CRC32 checksum of a file."""
    crc = 0
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            crc = zlib.crc32(chunk, crc)
    return f"{crc & 0xFFFFFFFF:08X}"  # Return CRC32 as hexadecimal value

def extract_and_calculate_crc32(zip_path):
    """Extract the first file from a zip archive and calculate its CRC32 checksum."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        extracted_file = zip_ref.namelist()[0]
        extracted_file_path = zip_ref.extract(extracted_file, path=os.path.dirname(zip_path))
        crc32_checksum = calculate_crc32(extracted_file_path)
        os.remove(extracted_file_path)
        return crc32_checksum, extracted_file_path

def get_user_input():
    """Get user input for the paths and file settings."""
    rom_root_dir = input("Enter the root directory of your ROMs: ")
    output_dir = input("Enter the desired output directory for the playlist: ")
    output_name = input("Enter the desired output file name (without extension): ")
    file_extension = input("Enter the file extension to look for (e.g., .iso): ")
    db_name = input("Enter the database name to use in the playlist: ")
    use_crc32 = input("Do you want to calculate CRC32 checksums for the files? (yes/no): ").strip().lower() == "yes"
    handle_zip_files = input("Do you want to handle zip files and extract the contained file? (yes/no): ").strip().lower() == "yes"
    return rom_root_dir, output_dir, output_name, file_extension, db_name, use_crc32, handle_zip_files

def create_playlist():
    """Create an empty playlist dictionary."""
    return {
        "version": "1.0",
        "default_core_path": "DETECT",
        "default_core_name": "DETECT",
        "label_display_mode": 0,
        "right_thumbnail_mode": 0,
        "left_thumbnail_mode": 0,
        "sort_mode": 0,
        "items": []
    }

def process_files(rom_root_dir, file_extension, use_crc32, handle_zip_files, db_name):
    """Process the files in the given directory and add them to the playlist."""
    playlist = create_playlist()
    for root, dirs, files in os.walk(rom_root_dir):
        for file in files:
            full_path = os.path.join(root, file)
            crc32_checksum = "DETECT"

            if file.endswith(file_extension):
                if use_crc32:
                    crc32_checksum = calculate_crc32(full_path)
            elif handle_zip_files and file.endswith(".zip"):
                crc32_checksum, extracted_file_path = extract_and_calculate_crc32(full_path)
                full_path = extracted_file_path

            item = {
                "path": full_path,
                "label": os.path.splitext(file)[0],
                "core_path": "DETECT",
                "core_name": "DETECT",
                "crc32": crc32_checksum,
                "db_name": db_name
            }
            playlist["items"].append(item)

            if use_crc32:
                print(f"Processed file: {full_path}")
                print(f"CRC32 checksum: {crc32_checksum} (hexadecimal)")
            else:
                print(f"Processed file: {full_path} (CRC32: DETECT)")
    return playlist

def save_playlist(playlist, output_file):
    """Save the playlist to the output file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(playlist, f, indent=4)
    print(f"\nPlaylist saved to {output_file}")

def main():
    rom_root_dir, output_dir, output_name, file_extension, db_name, use_crc32, handle_zip_files = get_user_input()
    output_file = os.path.join(output_dir, f"{output_name}.lpl")
    playlist = process_files(rom_root_dir, file_extension, use_crc32, handle_zip_files, db_name)
    save_playlist(playlist, output_file)

if __name__ == "__main__":
    main()
