#!/bin/bash

# Define the directory to search in and the file type
search_dir="2"
search_pattern="*.jpg"

# Use find to locate all files that match the pattern and move them to the parent directory
find "$search_dir" -type f -name '*.jpg' -exec sh -c '
  for file do
    mv "$file" "images/${base}"
  done
' sh {} 
