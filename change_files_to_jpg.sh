#!/bin/bash

# Define the directory to search and the file extension to search for
search_dir="images/resized_images"
search_extension=".jpg.jpg.jpg.jpg.jpg"

# Use find to locate all .JPG files and rename them to .jpg
find "$search_dir" -type f -name "*${search_extension}" -exec sh -c '
  for file do
    lowercase_file=$(echo "$file" | tr '[:upper:]' '[:lower:]')
    base=${lowercase_file%".jpg"}
    mv "$file" "${base}.jpg"
  done
' sh {} +