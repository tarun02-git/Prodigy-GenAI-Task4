# Image-to-Image Generation for Prodigy InfoTech

**Project by Tarun Agarwal for Prodigy InfoTech**

*Using the capabilities of Gen AI for creating a world with technologies.*

## Overview

This project provides a comprehensive image-to-image generation system using state-of-the-art AI models. It includes multiple interfaces (Flask and Gradio) for easy deployment and demonstration.

## Features

- **Multiple AI Models**: Support for various free image-to-image models
- **Web Interfaces**: Both Flask and Gradio interfaces for easy access
- **Batch Processing**: Process multiple images at once
- **Result Management**: Automatic saving of generated images
- **Demo Examples**: Pre-built examples for client demonstrations
- **Error-Free Implementation**: Robust error handling and validation

## Project Structure

```
image-to-image-generation/
├── models/                 # AI model implementations
├── web_interfaces/         # Flask and Gradio interfaces
├── examples/              # Demo examples and sample images
├── results/               # Generated image outputs
├── utils/                 # Utility functions
├── config/                # Configuration files
├── requirements.txt       # Python dependencies
├── main.py               # Main application entry point
├── flask_app.py          # Flask web interface
├── gradio_app.py         # Gradio interface
└── README.md             # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd image-to-image-generation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download models** (first run will download automatically):
   ```bash
   python main.py --download-models
   ```

## Usage

### Command Line Interface

```bash
# Basic image-to-image generation
python main.py --input examples/sample.jpg --prompt "a beautiful landscape"

# Batch processing
python main.py --input-dir examples/ --prompt "artistic style"

# With specific model
python main.py --input examples/sample.jpg --model stable-diffusion --prompt "oil painting"
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

## Available Models

1. **Stable Diffusion**: High-quality image generation
2. **ControlNet**: Precise control over image generation
3. **InstructPix2Pix**: Instruction-based image editing
4. **Stable Diffusion XL**: Enhanced resolution and quality

## Examples

The `examples/` directory contains sample images for testing:
- `sample1.jpg`: Landscape image
- `sample2.jpg`: Portrait image
- `sample3.jpg`: Abstract art

## Results

All generated images are automatically saved in the `results/` directory with timestamps and metadata.

## Configuration

Edit `config/settings.py` to customize:
- Model parameters
- Output settings
- Web interface configurations

## Error Handling

The project includes comprehensive error handling for:
- Invalid input images
- Model loading failures
- Memory management
- Network connectivity issues

## Performance Optimization

- GPU acceleration (when available)
- Memory-efficient processing
- Batch processing capabilities
- Caching for repeated operations

## License

This project is developed by Tarun Agarwal for Prodigy InfoTech.

## Support

For technical support or questions, please contact the development team at Prodigy InfoTech.

---

**Built with ❤️ by Tarun Agarwal for Prodigy InfoTech**
*Empowering the future with AI-driven image generation technology.* 