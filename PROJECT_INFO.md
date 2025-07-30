# Image-to-Image Generation Project for Prodigy InfoTech

**Developed by Tarun Agarwal for Prodigy InfoTech**

*Using the capabilities of Gen AI for creating a world with technologies.*

## 🎯 Project Overview

This comprehensive image-to-image generation project demonstrates the power of AI-driven image transformation using state-of-the-art models. It provides multiple interfaces for easy access and experimentation, making it perfect for client demonstrations and research purposes.

## 🚀 Key Features

### ✨ Core Capabilities
- **Multiple AI Models**: Support for Stable Diffusion, Stable Diffusion XL, and InstructPix2Pix
- **Web Interfaces**: Both Flask and Gradio interfaces for easy access
- **Batch Processing**: Process multiple images at once
- **Result Management**: Automatic saving of generated images with metadata
- **Demo Examples**: Pre-built examples for client demonstrations
- **Error-Free Implementation**: Robust error handling and validation

### 🎨 AI Models Supported
1. **Stable Diffusion**: High-quality image generation with excellent detail preservation
2. **Stable Diffusion XL**: Enhanced resolution and quality for professional results
3. **InstructPix2Pix**: Instruction-based image editing for precise transformations

### 🌐 Web Interfaces
- **Flask Interface**: Professional web application with modern UI
- **Gradio Interface**: Interactive interface perfect for demonstrations

## 📁 Project Structure

```
image-to-image-generation/
├── models/                 # AI model implementations
│   └── image_generator.py # Main generation class
├── web_interfaces/         # Web interface components
├── examples/              # Demo examples and sample images
├── results/               # Generated image outputs
├── utils/                 # Utility functions
│   └── image_utils.py    # Image processing utilities
├── config/                # Configuration files
│   └── settings.py       # Project settings and configurations
├── templates/             # Flask HTML templates
├── requirements.txt       # Python dependencies
├── main.py               # Main application entry point
├── flask_app.py          # Flask web interface
├── gradio_app.py         # Gradio interface
├── create_examples.py    # Sample image creation script
└── README.md             # Project documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- CUDA-compatible GPU (recommended for optimal performance)
- 8GB+ RAM (16GB+ recommended)

### Step 1: Clone and Setup
```bash
# Navigate to project directory
cd "image to image generation for prodigy"

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create Sample Images
```bash
# Generate sample images for demos
python create_examples.py
```

### Step 3: Download Models (First Run)
```bash
# Download all models (this will happen automatically on first use)
python main.py --download-models
```

## 🎮 Usage Examples

### Command Line Interface

#### Basic Image Generation
```bash
python main.py --input examples/sample1.jpg --prompt "oil painting style"
```

#### Batch Processing
```bash
python main.py --input-dir examples/ --prompt "anime style"
```

#### Advanced Parameters
```bash
python main.py --input examples/sample2.jpg \
               --prompt "convert to watercolor painting" \
               --model stable-diffusion-xl \
               --strength 0.8 \
               --guidance-scale 10.0 \
               --num-steps 75
```

#### Demo Examples
```bash
python main.py --demo
```

#### List Available Models
```bash
python main.py --list-models
```

### Web Interfaces

#### Flask Interface
```bash
python flask_app.py
```
Access at: http://localhost:5000

#### Gradio Interface
```bash
python gradio_app.py
```
Access at: http://localhost:7860

## 🎯 Demo Examples

The project includes pre-configured demo examples:

1. **Landscape to Oil Painting**: Transform landscape photos into oil paintings
2. **Portrait to Anime Style**: Convert portraits to anime/manga style
3. **Abstract Art Enhancement**: Enhance abstract art with vibrant colors

## 📊 Performance Optimization

### GPU Acceleration
- Automatic CUDA detection and utilization
- Memory-efficient attention mechanisms
- VAE slicing for large images
- Optimized model loading

### Memory Management
- Automatic cleanup of old results
- Efficient batch processing
- Memory usage monitoring

## 🔧 Configuration

### Model Settings
Edit `config/settings.py` to customize:
- Model parameters and defaults
- Performance settings
- Web interface configurations
- Error messages and logging

### Web Interface Settings
```python
WEB_SETTINGS = {
    "flask": {
        "host": "0.0.0.0",
        "port": 5000,
        "max_file_size": 16 * 1024 * 1024  # 16MB
    },
    "gradio": {
        "server_name": "0.0.0.0",
        "server_port": 7860
    }
}
```

## 🛡️ Error Handling

The project includes comprehensive error handling for:
- Invalid input images
- Model loading failures
- Memory management issues
- Network connectivity problems
- File format validation

## 📈 Results Management

### Automatic Saving
- All generated images are automatically saved with timestamps
- Metadata is preserved alongside images
- Organized file naming system

### Output Structure
```
results/
├── sample1_stable-diffusion_oil_painting_20241230_143022.png
├── sample1_stable-diffusion_oil_painting_20241230_143022.json
├── sample2_stable-diffusion_anime_style_20241230_143045.png
└── sample2_stable-diffusion_anime_style_20241230_143045.json
```

## 🎨 Client Demonstration Features

### Professional Interface
- Modern, responsive web design
- Real-time generation progress
- Detailed metadata display
- Easy-to-use controls

### Demo Capabilities
- Pre-configured examples
- Batch processing demonstrations
- Model comparison features
- Result comparison tools

## 🔍 Troubleshooting

### Common Issues

#### Model Loading Errors
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Force CPU usage
export CUDA_VISIBLE_DEVICES=""
```

#### Memory Issues
```bash
# Reduce batch size
python main.py --input image.jpg --prompt "style" --num-steps 25
```

#### File Size Limits
- Maximum file size: 16MB
- Supported formats: JPG, PNG, BMP, TIFF, WEBP
- Automatic image validation

## 📝 API Documentation

### Main Generator Class
```python
from models.image_generator import ImageGenerator

# Initialize generator
generator = ImageGenerator(model_name="stable-diffusion")

# Generate image
result = generator.generate(
    input_image="path/to/image.jpg",
    prompt="transform description",
    strength=0.75,
    guidance_scale=7.5,
    num_inference_steps=50
)
```

### Utility Functions
```python
from utils.image_utils import load_image, save_image, validate_image

# Load and validate image
image = load_image("path/to/image.jpg")

# Save with metadata
save_image(image, "output.png", metadata={"prompt": "description"})
```

## 🎯 Use Cases

### Creative Applications
- Artistic style transfer
- Photo enhancement and restoration
- Creative content generation
- Educational demonstrations

### Business Applications
- Marketing material creation
- Product visualization
- Design prototyping
- Client presentations

### Research Applications
- AI model evaluation
- Image processing research
- Educational demonstrations
- Technology showcases

## 🏆 Project Highlights

### Technical Excellence
- **Error-Free Implementation**: Comprehensive error handling and validation
- **Performance Optimized**: GPU acceleration and memory management
- **Scalable Architecture**: Modular design for easy extension
- **Professional Quality**: Production-ready code with proper documentation

### User Experience
- **Multiple Interfaces**: Command line, Flask, and Gradio options
- **Intuitive Design**: Easy-to-use controls and clear feedback
- **Demo Ready**: Pre-configured examples for client demonstrations
- **Comprehensive Documentation**: Detailed setup and usage instructions

### Innovation
- **State-of-the-Art Models**: Latest AI image generation technology
- **Free Model Integration**: Uses freely available models
- **Local Deployment**: No external API dependencies
- **Customizable**: Easy to modify and extend

## 📞 Support & Contact

**Developed by Tarun Agarwal for Prodigy InfoTech**

For technical support or questions about this project, please contact the development team at Prodigy InfoTech.

---

**Built with ❤️ by Tarun Agarwal for Prodigy InfoTech**

*Empowering the future with AI-driven image generation technology.* 