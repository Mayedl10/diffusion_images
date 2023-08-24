from PIL import Image
import os

input_folder = "out"
output_folder = "downscaled"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

files = os.listdir(input_folder)

for file in files:
    if file.endswith(".png"):
        image = Image.open(os.path.join(input_folder, file))

        thumbnail_size = (100, 100)

        image.thumbnail(thumbnail_size)

        image.save(os.path.join(output_folder, file))

        print(f"Resized {file} and saved to {output_folder}/{file}")

print("Done")
