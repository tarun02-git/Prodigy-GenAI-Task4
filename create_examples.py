#!/usr/bin/env python3
"""
Create sample images for demo examples
Developed by Tarun Agarwal for Prodigy InfoTech
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_sample_images():
    """Create sample images for the demo examples."""
    
    # Create examples directory
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Sample 1: Landscape
    print("Creating sample landscape image...")
    landscape = Image.new('RGB', (512, 384), (135, 206, 235))  # Sky blue
    draw = ImageDraw.Draw(landscape)
    
    # Draw mountains
    draw.polygon([(0, 200), (100, 150), (200, 180), (300, 120), (400, 160), (512, 140), (512, 384), (0, 384)], fill=(139, 69, 19))
    
    # Draw grass
    draw.rectangle([(0, 250), (512, 384)], fill=(34, 139, 34))
    
    # Draw sun
    draw.ellipse([(400, 50), (450, 100)], fill=(255, 255, 0))
    
    # Add some trees
    for x in [50, 150, 250, 350, 450]:
        draw.ellipse([(x-15, 200), (x+15, 230)], fill=(0, 100, 0))
        draw.rectangle([(x-5, 230), (x+5, 250)], fill=(139, 69, 19))
    
    landscape.save(examples_dir / "sample1.jpg", quality=95)
    print("✅ Created sample1.jpg (Landscape)")
    
    # Sample 2: Portrait
    print("Creating sample portrait image...")
    portrait = Image.new('RGB', (384, 512), (240, 240, 240))  # Light gray
    draw = ImageDraw.Draw(portrait)
    
    # Draw face outline
    draw.ellipse([(142, 100), (242, 200)], fill=(255, 218, 185))  # Skin tone
    
    # Draw eyes
    draw.ellipse([(160, 130), (175, 145)], fill=(255, 255, 255))  # White
    draw.ellipse([(209, 130), (224, 145)], fill=(255, 255, 255))
    draw.ellipse([(165, 135), (170, 140)], fill=(0, 0, 0))  # Pupils
    draw.ellipse([(214, 135), (219, 140)], fill=(0, 0, 0))
    
    # Draw nose
    draw.polygon([(192, 150), (188, 165), (196, 165)], fill=(255, 218, 185))
    
    # Draw mouth
    draw.arc([(175, 170), (209, 185)], 0, 180, fill=(139, 69, 19), width=2)
    
    # Draw hair
    draw.ellipse([(130, 80), (254, 120)], fill=(139, 69, 19))
    
    # Draw body
    draw.rectangle([(160, 200), (224, 400)], fill=(70, 130, 180))  # Blue shirt
    
    portrait.save(examples_dir / "sample2.jpg", quality=95)
    print("✅ Created sample2.jpg (Portrait)")
    
    # Sample 3: Abstract art
    print("Creating sample abstract art image...")
    abstract = Image.new('RGB', (512, 512), (255, 255, 255))  # White
    draw = ImageDraw.Draw(abstract)
    
    # Create colorful geometric shapes
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    
    # Draw circles
    for i in range(6):
        x = 100 + i * 60
        y = 150 + (i % 2) * 100
        color = colors[i]
        draw.ellipse([(x-30, y-30), (x+30, y+30)], fill=color)
    
    # Draw rectangles
    for i in range(4):
        x = 50 + i * 120
        y = 350
        color = colors[(i + 2) % len(colors)]
        draw.rectangle([(x, y), (x+80, y+60)], fill=color)
    
    # Draw lines
    for i in range(8):
        x1 = i * 60
        y1 = 50
        x2 = (i + 1) * 60
        y2 = 450
        color = colors[i % len(colors)]
        draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    
    abstract.save(examples_dir / "sample3.jpg", quality=95)
    print("✅ Created sample3.jpg (Abstract Art)")
    
    print("\n🎉 All sample images created successfully!")
    print("📁 Images saved in the 'examples' directory")
    print("🎨 Ready for demo and testing!")

if __name__ == "__main__":
    create_sample_images() 