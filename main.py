#!/usr/bin/env python3
"""
Main application for Image-to-Image Generation Project
Developed by Tarun Agarwal for Prodigy InfoTech

Using the capabilities of Gen AI for creating a world with technologies.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional
import json

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from config.settings import MODEL_CONFIGS, DEMO_EXAMPLES, LOGGING_CONFIG
from models.image_generator import ImageGenerator
from utils.image_utils import validate_image, load_image, create_image_grid, cleanup_old_results
from utils.image_utils import get_image_info

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG["file"]),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def setup_logging():
    """Setup logging configuration."""
    LOGGING_CONFIG["file"].parent.mkdir(exist_ok=True)

def print_banner():
    """Print project banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Image-to-Image Generation for Prodigy InfoTech            ║
║                                                                              ║
║                    Developed by Tarun Agarwal                               ║
║                                                                              ║
║         Using the capabilities of Gen AI for creating a world with          ║
║                           technologies.                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_demo_examples():
    """Run demo examples to showcase the system."""
    print("\n🎨 Running Demo Examples...")
    print("=" * 50)
    
    generator = ImageGenerator(model_name="stable-diffusion")
    
    for i, example in enumerate(DEMO_EXAMPLES, 1):
        print(f"\n📸 Demo {i}: {example['name']}")
        print(f"   Input: {example['input']}")
        print(f"   Prompt: '{example['prompt']}'")
        print(f"   Model: {example['model']}")
        
        try:
            # Check if example image exists
            if not Path(example['input']).exists():
                print(f"   ⚠️  Example image not found: {example['input']}")
                continue
                
            result = generator.generate(
                input_image=example['input'],
                prompt=example['prompt'],
                strength=example['strength']
            )
            
            if result['success']:
                print(f"   ✅ Generated successfully!")
                print(f"   📁 Saved to: {result['output_path']}")
                print(f"   ⏱️  Time: {result['metadata']['generation_time']:.2f}s")
            else:
                print(f"   ❌ Failed: {result['error']}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            
    print("\n🎉 Demo completed!")

def process_single_image(input_path: str, prompt: str, model: str, 
                       strength: float, guidance_scale: float, 
                       num_steps: int) -> dict:
    """Process a single image."""
    try:
        # Validate input image
        if not validate_image(input_path):
            return {"success": False, "error": "Invalid input image"}
            
        # Initialize generator
        generator = ImageGenerator(model_name=model)
        
        # Generate image
        result = generator.generate(
            input_image=input_path,
            prompt=prompt,
            strength=strength,
            guidance_scale=guidance_scale,
            num_inference_steps=num_steps
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return {"success": False, "error": str(e)}

def process_batch_images(input_dir: str, prompt: str, model: str,
                       strength: float, guidance_scale: float,
                       num_steps: int) -> List[dict]:
    """Process multiple images in a directory."""
    try:
        input_path = Path(input_dir)
        if not input_path.exists():
            return [{"success": False, "error": f"Directory not found: {input_dir}"}]
            
        # Find all image files
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']:
            image_files.extend(input_path.glob(f"*{ext}"))
            image_files.extend(input_path.glob(f"*{ext.upper()}"))
            
        if not image_files:
            return [{"success": False, "error": f"No image files found in {input_dir}"}]
            
        print(f"Found {len(image_files)} images to process")
        
        # Initialize generator
        generator = ImageGenerator(model_name=model)
        
        # Process each image
        results = []
        for i, image_file in enumerate(image_files, 1):
            print(f"Processing {i}/{len(image_files)}: {image_file.name}")
            
            result = generator.generate(
                input_image=str(image_file),
                prompt=prompt,
                strength=strength,
                guidance_scale=guidance_scale,
                num_inference_steps=num_steps
            )
            
            results.append(result)
            
        return results
        
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        return [{"success": False, "error": str(e)}]

def list_models():
    """List available models."""
    print("\n🤖 Available Models:")
    print("=" * 30)
    for model_name, config in MODEL_CONFIGS.items():
        print(f"📋 {model_name}")
        print(f"   Description: {config['description']}")
        print(f"   Max Resolution: {config['max_resolution']}px")
        print(f"   Default Strength: {config['default_strength']}")
        print(f"   Default Guidance Scale: {config['default_guidance_scale']}")
        print()

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Image-to-Image Generation for Prodigy InfoTech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo
  python main.py --input image.jpg --prompt "oil painting style"
  python main.py --input-dir images/ --prompt "anime style"
  python main.py --list-models
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument("--input", type=str, help="Input image file")
    input_group.add_argument("--input-dir", type=str, help="Input directory for batch processing")
    
    # Generation parameters
    parser.add_argument("--prompt", type=str, help="Text prompt for generation")
    parser.add_argument("--model", type=str, default="stable-diffusion", 
                       choices=list(MODEL_CONFIGS.keys()), help="Model to use")
    parser.add_argument("--strength", type=float, default=0.75, 
                       help="Denoising strength (0.0-1.0)")
    parser.add_argument("--guidance-scale", type=float, default=7.5,
                       help="Guidance scale for generation")
    parser.add_argument("--num-steps", type=int, default=50,
                       help="Number of inference steps")
    
    # Special commands
    parser.add_argument("--demo", action="store_true", help="Run demo examples")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--download-models", action="store_true", help="Download models")
    parser.add_argument("--cleanup", action="store_true", help="Clean up old results")
    
    args = parser.parse_args()
    
    # Setup
    setup_logging()
    print_banner()
    
    # Handle special commands
    if args.list_models:
        list_models()
        return
        
    if args.cleanup:
        deleted_count = cleanup_old_results()
        print(f"🧹 Cleaned up {deleted_count} old result files")
        return
        
    if args.download_models:
        print("📥 Downloading models...")
        for model_name in MODEL_CONFIGS.keys():
            try:
                print(f"Downloading {model_name}...")
                generator = ImageGenerator(model_name=model_name)
                print(f"✅ {model_name} downloaded successfully")
            except Exception as e:
                print(f"❌ Error downloading {model_name}: {str(e)}")
        return
        
    if args.demo:
        run_demo_examples()
        return
        
    # Validate required arguments
    if not args.input and not args.input_dir:
        parser.error("Either --input or --input-dir is required")
        
    if not args.prompt:
        parser.error("--prompt is required")
        
    # Process images
    if args.input:
        print(f"🎨 Processing single image: {args.input}")
        result = process_single_image(
            input_path=args.input,
            prompt=args.prompt,
            model=args.model,
            strength=args.strength,
            guidance_scale=args.guidance_scale,
            num_steps=args.num_steps
        )
        
        if result['success']:
            print(f"✅ Generation successful!")
            print(f"📁 Output: {result['output_path']}")
            print(f"⏱️  Time: {result['metadata']['generation_time']:.2f}s")
        else:
            print(f"❌ Generation failed: {result['error']}")
            sys.exit(1)
            
    elif args.input_dir:
        print(f"🎨 Processing batch images from: {args.input_dir}")
        results = process_batch_images(
            input_dir=args.input_dir,
            prompt=args.prompt,
            model=args.model,
            strength=args.strength,
            guidance_scale=args.guidance_scale,
            num_steps=args.num_steps
        )
        
        successful = sum(1 for r in results if r['success'])
        total = len(results)
        
        print(f"\n📊 Batch processing completed:")
        print(f"✅ Successful: {successful}/{total}")
        print(f"❌ Failed: {total - successful}/{total}")
        
        if successful < total:
            print("\nFailed generations:")
            for result in results:
                if not result['success']:
                    print(f"  - {result['error']}")

if __name__ == "__main__":
    main() 