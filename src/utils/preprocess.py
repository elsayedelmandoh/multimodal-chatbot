def preprocess_stop_sequences(stop_sequences: str) -> Optional[List[str]]:
    return [seq.strip() for seq in stop_sequences.split(",")] if stop_sequences else None

def preprocess_image(image: Image.Image) -> Image.Image:
    image_height = int(image.height * IMAGE_WIDTH / image.width)
    return image.resize((IMAGE_WIDTH, image_height))