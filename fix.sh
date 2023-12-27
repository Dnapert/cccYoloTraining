#!/bin/bash
# I screwed up and accidentally named all of my files with .jpg.jpg.jpg.jpg extensions lol
# Define the directory to search
search_dir="images/resized_images"

# Use find to locate all files that have repeated .jpg extensions
find "$search_dir" -type f -name "*.jpg.jpg*" -exec bash -c '
  for file do
    # Construct the new filename by removing all occurrences of .jpg except the last one
    newname=$(echo "$file" | sed -r "s/(.jpg)+$/.jpg/")
    # Rename the file to the new name
    mv "$file" "$newname"
  done
' bash {} +
