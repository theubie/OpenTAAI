#!/bin/bash

echo "Please select your preferred installation type:"
echo "A. NVIDIA GPU (requires CUDA)"
echo "B. CPU only"

read -p "Enter your selection [A/B]: " choice

if [ $choice == "A" ] || [ $choice == "a" ]
then
  pip install -r requirements.txt
elif [ $choice == "B" ] || [ $choice == "b" ]
then
  pip install -r requirements-cpu.txt
else
  echo "Invalid choice. Please enter A or B."
fi

echo "Done!"