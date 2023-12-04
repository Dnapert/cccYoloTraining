#!/bin/bash

# Define the directory to search in
search_dir="data/resized_images"
search_pattern="*.jpg"

# Use find to locate all files that match the pattern and move them to the parent directory
find "$search_dir" -type f -name '*.jpg' -exec sh -c '
  for file do
    mv "$file" "$search_dir/${base}"
  done
' sh {} +
