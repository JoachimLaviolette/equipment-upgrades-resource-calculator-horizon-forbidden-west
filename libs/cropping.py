from PIL import Image

def crop_image(image_path: str) -> Image:
    print(f"Cropping image '{image_path}'...")

    image = Image.open(image_path)
    cropped_image = image.crop((2940, 280, 3800, 1200))

    return cropped_image