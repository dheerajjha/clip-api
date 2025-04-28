# CLIP API

A simple FastAPI application that serves OpenAI's CLIP model for image-text similarity matching, optimized for CPU-only usage.

## Features

- `/predict`: Calculate similarity between an image and text
- `/encode_image`: Get embeddings for an image
- `/encode_text`: Get embeddings for text
- Swagger UI documentation at `/docs`

## Requirements

- Docker
- Python 3.9+ (if running without Docker)

## CPU-Only Configuration

This API is specifically configured to run on CPU-only environments. The PyTorch packages are installed with CPU-only versions to ensure compatibility with systems without GPUs. This configuration:

- Uses `torch==2.2.1+cpu`, `torchvision==0.17.1+cpu`, and `torchaudio==2.2.1+cpu`
- Includes the PyTorch CPU-specific index URL
- Explicitly sets the device to "cpu" in all model code
- Optimizes memory usage for CPU environments

## Quick Start

### Using the Provided Scripts

1. Start the server:
   ```
   ./start_server.sh
   ```
   This script will:
   - Create a virtual environment
   - Install all dependencies
   - Start the FastAPI server

2. In a new terminal, run the test script:
   ```
   ./run_test.sh
   ```
   This script will:
   - Create a test image
   - Test all API endpoints
   - Show the results

### Using Docker

1. Build the Docker image:
   ```
   docker build -t clip-api .
   ```

2. Run the container:
   ```
   docker run -p 80:80 clip-api
   ```

3. Access the API at http://localhost:80/docs

### Manual Setup (Without Scripts or Docker)

1. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 80
   ```

## Testing the API

### Using the Test Scripts

1. Start the server:
   ```
   ./start_server.sh
   ```

2. In a new terminal, create test images:
   ```
   python create_test_image.py
   ```
   This will create two test images: `test_image.jpg` and `blue_sky.jpg`.

3. Run the test script:
   ```
   python test_api.py
   ```
   This will:
   - Create a test image with text
   - Send it to the API with matching text
   - Send it to the API with non-matching text
   - Display the similarity scores

### API Usage with curl

#### Calculate Similarity

```bash
curl -X POST "http://localhost:80/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@your_image.jpg" \
  -F "text=your text description"
```

#### Get Image Embeddings

```bash
curl -X POST "http://localhost:80/encode_image" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@your_image.jpg"
```

#### Get Text Embeddings

```bash
curl -X POST "http://localhost:80/encode_text" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "text=your text description"
```

## How It Works

This API uses OpenAI's CLIP (Contrastive Language-Image Pre-training) model to understand the relationship between images and text. The model has been trained on a variety of image-text pairs and can be used for tasks like:

- Calculating similarity between images and text descriptions
- Generating embeddings for images and text that can be used for search or recommendation systems
- Zero-shot image classification

The API provides a simple interface to interact with the CLIP model without having to deal with the underlying machine learning code.
