#!/bin/bash

# Define the directory to search and the file extension to search for
search_dir="images"
search_extension="JPG"

# Use find to locate all .JPG files and rename them to .
find "$search_dir" -type f -name '*.$search_extension' -exec sh -c '
  for file do
    base=$(basename "$file" $search_extension)
    dir=$(dirname "$file")
    mv "$file" "$dir/${base}.jpg"
  done
' sh {} +
