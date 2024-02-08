import argparse
from PIL import Image
from pathlib import Path

def replace_colors(image_path, new_image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))

            if (r == g == b) and (70 < r < 120):
                image.putpixel((x,y), (0,0,0))
                continue

            image.putpixel((x, y), (255, 255, 255))

    image.convert("RGB").save(new_image_path)

def main():
	parser = argparse.ArgumentParser(description="Mask generator")
	parser.add_argument("--path", help="Path to directory with road images")

	args = parser.parse_args()

	directory = Path(args.path)

	for file in directory.iterdir():
		if file.is_file():
			if file.suffix == '.png':
				if 'mask' in file.stem:
					continue

				file_path = file.resolve()
				new_file_path = file_path.with_name(f"{file.stem}_mask{file.suffix}")
				replace_colors(file_path, new_file_path)

if __name__ == "__main__":
	main()
