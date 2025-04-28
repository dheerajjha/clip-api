import requests
import os
import sys
import time
import argparse
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_test_image(text, filename="test_image.jpg", size=(300, 200)):
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

def test_health(base_url):
    """Test the health endpoint"""
    response = requests.get(f"{base_url}/health")
    if response.status_code == 200:
        print("✅ Health check passed")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_predict(base_url, image_path, text):
    """Test the predict endpoint"""
    with open(image_path, "rb") as img_file:
        files = {"image": (os.path.basename(image_path), img_file, "image/jpeg")}
        data = {"text": text}
        response = requests.post(f"{base_url}/predict", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Predict endpoint test passed")
        print(f"   Image: {result.get('image_filename')}")
        print(f"   Text: {result.get('text')}")
        print(f"   Similarity: {result.get('similarity'):.2f}%")
        return True
    else:
        print(f"❌ Predict endpoint test failed: {response.status_code}")
        print(response.text)
        return False

def test_encode_image(base_url, image_path):
    """Test the encode_image endpoint"""
    with open(image_path, "rb") as img_file:
        files = {"image": (os.path.basename(image_path), img_file, "image/jpeg")}
        response = requests.post(f"{base_url}/encode_image", files=files)
    
    if response.status_code == 200:
        result = response.json()
        features = result.get('features')
        print(f"✅ Encode image endpoint test passed")
        print(f"   Image: {result.get('image_filename')}")
        print(f"   Feature vector length: {len(features)}")
        print(f"   First 5 values: {features[:5]}")
        return True
    else:
        print(f"❌ Encode image endpoint test failed: {response.status_code}")
        print(response.text)
        return False

def test_encode_text(base_url, text):
    """Test the encode_text endpoint"""
    data = {"text": text}
    response = requests.post(f"{base_url}/encode_text", data=data)
    
    if response.status_code == 200:
        result = response.json()
        features = result.get('features')
        print(f"✅ Encode text endpoint test passed")
        print(f"   Text: {result.get('text')}")
        print(f"   Feature vector length: {len(features)}")
        print(f"   First 5 values: {features[:5]}")
        return True
    else:
        print(f"❌ Encode text endpoint test failed: {response.status_code}")
        print(response.text)
        return False

def main():
    parser = argparse.ArgumentParser(description="Test the CLIP API")
    parser.add_argument("--url", default="http://localhost:80", help="Base URL of the API")
    parser.add_argument("--image", help="Path to test image (will create one if not provided)")
    parser.add_argument("--text", default="a simple test image", help="Text to test with")
    args = parser.parse_args()
    
    base_url = args.url
    text = args.text
    
    # Create or use provided test image
    if args.image:
        image_path = args.image
    else:
        image_path = create_test_image(text)
    
    print(f"\n🔍 Testing CLIP API at {base_url}\n")
    
    # Wait for the server to be ready
    max_retries = 5
    for i in range(max_retries):
        try:
            if test_health(base_url):
                break
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                print(f"Server not ready, retrying in 2 seconds... ({i+1}/{max_retries})")
                time.sleep(2)
            else:
                print("❌ Could not connect to the server after multiple attempts")
                sys.exit(1)
    
    print("\n--- Testing Endpoints ---\n")
    
    # Test predict endpoint
    test_predict(base_url, image_path, text)
    print()
    
    # Test encode_image endpoint
    test_encode_image(base_url, image_path)
    print()
    
    # Test encode_text endpoint
    test_encode_text(base_url, text)
    
    print("\n✨ All tests completed!")

if __name__ == "__main__":
    main()
