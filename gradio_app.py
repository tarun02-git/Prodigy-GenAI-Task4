#!/usr/bin/env python3
"""
Gradio Web Interface for Image-to-Image Generation Project
Developed by Tarun Agarwal for Prodigy InfoTech
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import gradio as gr
from PIL import Image
import numpy as np

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from config.settings import MODEL_CONFIGS, WEB_SETTINGS, DEMO_EXAMPLES
from models.image_generator import ImageGenerator
from utils.image_utils import validate_image, load_image, save_image, generate_output_filename

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global generator instance
generator = None

def get_generator(model_name: str = "stable-diffusion") -> ImageGenerator:
    """Get or create generator instance."""
    global generator
    if generator is None or generator.model_name != model_name:
        try:
            generator = ImageGenerator(model_name=model_name)
        except Exception as e:
            logger.error(f"Error initializing generator: {str(e)}")
            raise
    return generator

def generate_image_gradio(input_image, prompt, model_name, strength, guidance_scale, num_steps):
    """
    Generate image using Gradio interface.
    
    Args:
        input_image: Input image (PIL Image or numpy array)
        prompt: Text prompt for generation
        model_name: Model to use
        strength: Denoising strength
        guidance_scale: Guidance scale
        num_steps: Number of inference steps
        
    Returns:
        tuple: (generated_image, metadata_text)
    """
    try:
        if input_image is None:
            return None, "❌ Please upload an input image."
            
        if not prompt or not prompt.strip():
            return None, "❌ Please enter a prompt."
            
        # Convert numpy array to PIL Image if needed
        if isinstance(input_image, np.ndarray):
            input_image = Image.fromarray(input_image)
            
        # Initialize generator
        generator = get_generator(model_name)
        
        # Generate image
        result = generator.generate(
            input_image=input_image,
            prompt=prompt,
            strength=strength,
            guidance_scale=guidance_scale,
            num_inference_steps=num_steps
        )
        
        if result['success']:
            # Create metadata text
            metadata = result['metadata']
            metadata_text = f"""
✅ Generation Successful!

📊 Generation Details:
• Model: {metadata['model']}
• Generation Time: {metadata['generation_time']:.2f}s
• Strength: {metadata['strength']}
• Guidance Scale: {metadata['guidance_scale']}
• Steps: {metadata['num_inference_steps']}
• Device: {metadata['device']}
• Input Size: {metadata['input_size']}
• Output Size: {metadata['output_size']}

💾 Saved to: {result['output_path']}
            """
            
            return result['generated_image'], metadata_text
        else:
            return None, f"❌ Generation failed: {result['error']}"
            
    except Exception as e:
        logger.error(f"Error in Gradio generation: {str(e)}")
        return None, f"❌ Error: {str(e)}"

def run_demo_example(example_index):
    """Run a demo example."""
    try:
        if example_index >= len(DEMO_EXAMPLES):
            return None, "❌ Invalid example index."
            
        example = DEMO_EXAMPLES[example_index]
        
        # Check if example image exists
        if not Path(example['input']).exists():
            return None, f"❌ Example image not found: {example['input']}"
            
        # Load example image
        input_image = load_image(example['input'])
        
        # Generate using the example parameters
        result = generate_image_gradio(
            input_image=input_image,
            prompt=example['prompt'],
            model_name=example['model'],
            strength=example['strength'],
            guidance_scale=7.5,
            num_steps=50
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error running demo example: {str(e)}")
        return None, f"❌ Error running demo: {str(e)}"

def get_model_info(model_name):
    """Get information about the selected model."""
    if model_name in MODEL_CONFIGS:
        config = MODEL_CONFIGS[model_name]
        return f"""
📋 Model Information:
• Name: {model_name}
• Description: {config['description']}
• Max Resolution: {config['max_resolution']}px
• Default Strength: {config['default_strength']}
• Default Guidance Scale: {config['default_guidance_scale']}
        """
    else:
        return "❌ Model not found."

def create_gradio_interface():
    """Create the Gradio interface."""
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header {
        text-align: center;
        margin-bottom: 20px;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
    .header h1 {
        margin: 0;
        font-size: 2rem;
    }
    .header p {
        margin: 5px 0 0 0;
        opacity: 0.9;
    }
    """
    
    with gr.Blocks(css=custom_css, title="Image-to-Image Generation - Prodigy InfoTech") as interface:
        
        # Header
        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div class="header">
                    <h1>🎨 Image-to-Image Generation</h1>
                    <p>Developed by Tarun Agarwal for Prodigy InfoTech</p>
                    <p>Using the capabilities of Gen AI for creating a world with technologies</p>
                </div>
                """)
        
        # Main interface
        with gr.Tabs():
            
            # Generation Tab
            with gr.TabItem("🎨 Generate Image"):
                with gr.Row():
                    with gr.Column(scale=1):
                        # Input section
                        gr.Markdown("### 📸 Upload Input Image")
                        input_image = gr.Image(
                            label="Input Image",
                            type="pil",
                            height=300
                        )
                        
                        gr.Markdown("### 📝 Generation Parameters")
                        prompt = gr.Textbox(
                            label="Prompt",
                            placeholder="Describe how you want to transform the image...",
                            lines=3
                        )
                        
                        model_name = gr.Dropdown(
                            choices=list(MODEL_CONFIGS.keys()),
                            value="stable-diffusion",
                            label="Model",
                            info="Select the AI model to use"
                        )
                        
                        with gr.Row():
                            strength = gr.Slider(
                                minimum=0.0,
                                maximum=1.0,
                                value=0.75,
                                step=0.05,
                                label="Strength",
                                info="Denoising strength (0.0-1.0)"
                            )
                            
                            guidance_scale = gr.Slider(
                                minimum=1.0,
                                maximum=20.0,
                                value=7.5,
                                step=0.5,
                                label="Guidance Scale",
                                info="Guidance scale for generation"
                            )
                        
                        num_steps = gr.Slider(
                            minimum=10,
                            maximum=100,
                            value=50,
                            step=5,
                            label="Steps",
                            info="Number of inference steps"
                        )
                        
                        generate_btn = gr.Button(
                            "🎨 Generate Image",
                            variant="primary",
                            size="lg"
                        )
                        
                        # Model info
                        model_info = gr.Textbox(
                            label="Model Information",
                            value=get_model_info("stable-diffusion"),
                            lines=6,
                            interactive=False
                        )
                    
                    with gr.Column(scale=1):
                        # Output section
                        gr.Markdown("### 🎨 Generated Image")
                        output_image = gr.Image(
                            label="Generated Image",
                            height=300
                        )
                        
                        output_info = gr.Textbox(
                            label="Generation Information",
                            lines=10,
                            interactive=False
                        )
                
                # Connect components
                generate_btn.click(
                    fn=generate_image_gradio,
                    inputs=[input_image, prompt, model_name, strength, guidance_scale, num_steps],
                    outputs=[output_image, output_info]
                )
                
                # Update model info when model changes
                model_name.change(
                    fn=get_model_info,
                    inputs=[model_name],
                    outputs=[model_info]
                )
            
            # Demo Tab
            with gr.TabItem("🚀 Demo Examples"):
                gr.Markdown("### 🎯 Try these pre-configured examples")
                
                with gr.Row():
                    with gr.Column():
                        demo_examples = gr.Dropdown(
                            choices=[f"{i+1}. {ex['name']}" for i, ex in enumerate(DEMO_EXAMPLES)],
                            label="Select Demo Example",
                            value="1. Landscape to Oil Painting"
                        )
                        
                        run_demo_btn = gr.Button(
                            "🚀 Run Demo",
                            variant="primary"
                        )
                    
                    with gr.Column():
                        demo_output_image = gr.Image(
                            label="Demo Result",
                            height=300
                        )
                        
                        demo_output_info = gr.Textbox(
                            label="Demo Information",
                            lines=8,
                            interactive=False
                        )
                
                # Connect demo components
                run_demo_btn.click(
                    fn=lambda x: run_demo_example(int(x.split('.')[0]) - 1),
                    inputs=[demo_examples],
                    outputs=[demo_output_image, demo_output_info]
                )
            
            # About Tab
            with gr.TabItem("ℹ️ About"):
                gr.Markdown("""
                # 🎨 Image-to-Image Generation for Prodigy InfoTech
                
                ## About This Project
                
                This project demonstrates the power of AI-driven image-to-image generation using state-of-the-art models. 
                It provides multiple interfaces for easy access and experimentation.
                
                ## Features
                
                - **Multiple AI Models**: Support for various free image-to-image models
                - **Web Interfaces**: Both Flask and Gradio interfaces for easy access
                - **Batch Processing**: Process multiple images at once
                - **Result Management**: Automatic saving of generated images
                - **Demo Examples**: Pre-built examples for client demonstrations
                - **Error-Free Implementation**: Robust error handling and validation
                
                ## Available Models
                
                1. **Stable Diffusion**: High-quality image generation
                2. **ControlNet**: Precise control over image generation
                3. **InstructPix2Pix**: Instruction-based image editing
                4. **Stable Diffusion XL**: Enhanced resolution and quality
                
                ## Usage
                
                1. Upload an input image
                2. Enter a descriptive prompt
                3. Select your preferred model and parameters
                4. Click "Generate Image" to create your transformation
                
                ## Technical Details
                
                - Built with Python, PyTorch, and Diffusers
                - GPU acceleration support
                - Memory-efficient processing
                - Comprehensive error handling
                
                ## Developer
                
                **Developed by Tarun Agarwal for Prodigy InfoTech**
                
                Using the capabilities of Gen AI for creating a world with technologies.
                
                ---
                
                *This project showcases the cutting-edge capabilities of generative AI in image transformation and creation.*
                """)
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 20px; padding: 10px; color: #666;">
            <p>&copy; 2024 Prodigy InfoTech. Developed by Tarun Agarwal.</p>
        </div>
        """)
    
    return interface

def main():
    """Main function to run the Gradio interface."""
    print("🎨 Starting Gradio Web Interface...")
    print("📱 Access the application at: http://localhost:7860")
    print("🎨 Developed by Tarun Agarwal for Prodigy InfoTech")
    
    # Create the interface
    interface = create_gradio_interface()
    
    # Launch the interface
    interface.launch(
        server_name=WEB_SETTINGS['gradio']['server_name'],
        server_port=WEB_SETTINGS['gradio']['server_port'],
        share=WEB_SETTINGS['gradio']['share'],
        debug=WEB_SETTINGS['gradio']['debug']
    )

if __name__ == "__main__":
    main() 