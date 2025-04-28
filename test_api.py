import requests
import os
from create_test_image import create_test_image

def test_clip_api():
    # Create a test image
    image_path = create_test_image("A simple test image")
    
    # API endpoint
    url = "http://localhost:8000/predict"
    
    # Text to compare with the image
    text = "A simple test image"
    
    # Open the image file
    with open(image_path, "rb") as img_file:
        # Prepare the files and data for the request
        files = {"image": (os.path.basename(image_path), img_file, "image/jpeg")}
        data = {"text": text}
        
        # Send the request
        print(f"Sending request to {url} with text: '{text}'")
        response = requests.post(url, files=files, data=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response
        result = response.json()
        print("\nAPI Response:")
        print(f"Image: {result.get('image_filename')}")
        print(f"Text: {result.get('text')}")
        print(f"Similarity: {result.get('similarity'):.2f}%")
        
        # Test with a different text
        different_text = "A blue sky with clouds"
        print(f"\nTesting with different text: '{different_text}'")
        
        # Open the image file again
        with open(image_path, "rb") as img_file:
            # Prepare the files and data for the request
            files = {"image": (os.path.basename(image_path), img_file, "image/jpeg")}
            data = {"text": different_text}
            
            # Send the request
            response = requests.post(url, files=files, data=data)
            
            # Parse the response
            result = response.json()
            print("\nAPI Response:")
            print(f"Image: {result.get('image_filename')}")
            print(f"Text: {result.get('text')}")
            print(f"Similarity: {result.get('similarity'):.2f}%")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_clip_api()
