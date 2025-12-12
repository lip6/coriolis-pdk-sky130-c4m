#!/usr/bin/env python3
import os

input_file = "StdCellLib.spi"  # ton fichier d'origine

with open(input_file, "r") as f:
    lines = f.readlines()

output_dir = "cells"
os.makedirs(output_dir, exist_ok=True)

current_name = None
current_lines = []

for line in lines:
    if line.strip().startswith(".subckt"):
        # Si on commence une nouvelle subckt
        if current_name is not None:
            # Sauvegarder la précédente avant de passer à la suivante
            output_path = os.path.join(output_dir, f"{current_name}.spi")
            with open(output_path, "w") as out:
                out.writelines(current_lines)
            current_lines = []

        parts = line.strip().split()
        current_name = parts[1]  # le nom après .subckt
        current_lines = [line]

    elif line.strip().startswith(".ends"):
        current_lines.append(line)
        if current_name:
            output_path = os.path.join(output_dir, f"{current_name}.spi")
            with open(output_path, "w") as out:
                out.writelines(current_lines)
            current_name = None
            current_lines = []

    elif current_name is not None:
        current_lines.append(line)

print("✅ Fichiers séparés générés dans le dossier 'cells/'")
