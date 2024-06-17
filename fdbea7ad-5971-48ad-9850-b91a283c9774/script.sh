#!/bin/bash

# Directory containing the files (you can change this to the target directory)
TARGET_DIR="./Feed_Right_ec_9a_0c_b1_00_44"

# Ensure the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
  echo "Directory $TARGET_DIR does not exist."
  exit 1
fi

# Change to the target directory
cd "$TARGET_DIR" || exit

# Initialize counter
counter=1

# Loop through all files in the directory
for file in $(ls | sort -n); do
  # Extract file extension
  extension="${file##*.}"
  # Generate new file name
  new_name="${counter}.${extension}"
  # Rename the file
  mv "$file" "$new_name"
  # Increment counter
  ((counter++))
done

echo "Files have been renamed successfully."
