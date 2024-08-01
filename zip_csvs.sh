#!/bin/bash

for file in anon_output_merged/*.csv; do
    echo $file
    zip "${file}.zip" "$file"
done
