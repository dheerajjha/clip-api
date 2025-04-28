from PIL import Image, ImageDraw, ImageFont

def create_test_image(text="Hello CLIP", filename="test_image.jpg", size=(300, 200)):
    """Create a simple test image with text on it"""
    # Create a new image with white background
    image = Image.new("RGB", size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Draw a colored rectangle
    draw.rectangle([(50, 50), (size[0]-50, size[1]-50)], fill=(200, 200, 240))
    
    # Add text
    draw.text((size[0]//2-40, size[1]//2-10), text, fill=(0, 0, 0))
    
    # Save the image
    image.save(filename)
    print(f"Created test image: {filename}")
    return filename

if __name__ == "__main__":
    # Create a test image with default parameters
    create_test_image()
    
    # Create another test image with custom text
    create_test_image("A blue sky", "blue_sky.jpg")
