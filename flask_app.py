#!/usr/bin/env python3
"""
Flask Web Interface for Image-to-Image Generation Project
Developed by Tarun Agarwal for Prodigy InfoTech
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import json
from typing import Optional

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from flask import Flask, request, render_template, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64

from config.settings import MODEL_CONFIGS, WEB_SETTINGS, SUPPORTED_FORMATS, ERROR_MESSAGES
from models.image_generator import ImageGenerator
from utils.image_utils import validate_image, load_image, save_image, generate_output_filename

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = WEB_SETTINGS['flask']['max_file_size']
app.config['SECRET_KEY'] = 'prodigy_infotech_image_generation_2024'

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

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html', models=MODEL_CONFIGS)

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """API endpoint for image generation."""
    try:
        # Get form data
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'}), 400
            
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No image file selected'}), 400
            
        # Validate file
        if not file.filename.lower().endswith(tuple(SUPPORTED_FORMATS)):
            return jsonify({'success': False, 'error': ERROR_MESSAGES['invalid_image']}), 400
            
        # Get parameters
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400
            
        model_name = request.form.get('model', 'stable-diffusion')
        if model_name not in MODEL_CONFIGS:
            return jsonify({'success': False, 'error': ERROR_MESSAGES['model_not_found']}), 400
            
        strength = float(request.form.get('strength', MODEL_CONFIGS[model_name]['default_strength']))
        guidance_scale = float(request.form.get('guidance_scale', MODEL_CONFIGS[model_name]['default_guidance_scale']))
        num_steps = int(request.form.get('num_steps', 50))
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"upload_{timestamp}_{filename}"
        temp_path = Path("results") / temp_filename
        
        temp_path.parent.mkdir(exist_ok=True)
        file.save(str(temp_path))
        
        try:
            # Validate the uploaded image
            if not validate_image(temp_path):
                return jsonify({'success': False, 'error': 'Invalid image file'}), 400
                
            # Initialize generator
            generator = get_generator(model_name)
            
            # Generate image
            result = generator.generate(
                input_image=str(temp_path),
                prompt=prompt,
                strength=strength,
                guidance_scale=guidance_scale,
                num_inference_steps=num_steps
            )
            
            if result['success']:
                # Convert generated image to base64 for display
                img_buffer = io.BytesIO()
                result['generated_image'].save(img_buffer, format='PNG')
                img_str = base64.b64encode(img_buffer.getvalue()).decode()
                
                response_data = {
                    'success': True,
                    'image_data': f"data:image/png;base64,{img_str}",
                    'output_path': result['output_path'],
                    'metadata': result['metadata']
                }
                
                # Clean up temp file
                temp_path.unlink(missing_ok=True)
                
                return jsonify(response_data)
            else:
                return jsonify({'success': False, 'error': result['error']}), 500
                
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            return jsonify({'success': False, 'error': ERROR_MESSAGES['processing_error']}), 500
            
        finally:
            # Clean up temp file
            temp_path.unlink(missing_ok=True)
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/models')
def get_models():
    """Get available models."""
    return jsonify({
        'success': True,
        'models': MODEL_CONFIGS
    })

@app.route('/api/status')
def get_status():
    """Get system status."""
    try:
        generator = get_generator()
        model_info = generator.get_model_info()
        
        return jsonify({
            'success': True,
            'status': 'ready',
            'model_info': model_info,
            'device': generator.device
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e)
        })

@app.route('/results/<filename>')
def download_result(filename):
    """Download generated result."""
    result_path = Path("results") / filename
    if result_path.exists():
        return send_file(str(result_path), as_attachment=True)
    else:
        return jsonify({'success': False, 'error': 'File not found'}), 404

@app.route('/demo')
def demo():
    """Demo page with examples."""
    return render_template('demo.html', models=MODEL_CONFIGS)

@app.route('/api/demo-examples')
def get_demo_examples():
    """Get demo examples."""
    from config.settings import DEMO_EXAMPLES
    return jsonify({
        'success': True,
        'examples': DEMO_EXAMPLES
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'success': False, 'error': ERROR_MESSAGES['file_too_large']}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'success': False, 'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create templates directory and HTML files
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Create index.html template
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image-to-Image Generation - Prodigy InfoTech</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .main-content {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }
        
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .file-upload {
            border: 2px dashed #667eea;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .file-upload:hover {
            border-color: #764ba2;
            background-color: #f8f9ff;
        }
        
        .file-upload.dragover {
            border-color: #764ba2;
            background-color: #f0f2ff;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .result-section {
            margin-top: 30px;
            text-align: center;
        }
        
        .result-image {
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            color: #e74c3c;
            background: #fdf2f2;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .success {
            color: #27ae60;
            background: #f0f9ff;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: white;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Image-to-Image Generation</h1>
            <p>Developed by Tarun Agarwal for Prodigy InfoTech</p>
            <p>Using the capabilities of Gen AI for creating a world with technologies</p>
        </div>
        
        <div class="main-content">
            <form id="generationForm">
                <div class="form-group">
                    <label for="image">Upload Image:</label>
                    <div class="file-upload" id="fileUpload">
                        <input type="file" id="image" name="image" accept="image/*" style="display: none;">
                        <p>📁 Click to upload or drag and drop</p>
                        <p style="font-size: 0.9rem; color: #666;">Supported formats: JPG, PNG, BMP, TIFF, WEBP</p>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="prompt">Prompt:</label>
                    <textarea id="prompt" name="prompt" rows="3" placeholder="Describe how you want to transform the image..." required></textarea>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="model">Model:</label>
                        <select id="model" name="model">
                            <option value="stable-diffusion">Stable Diffusion</option>
                            <option value="stable-diffusion-xl">Stable Diffusion XL</option>
                            <option value="instructpix2pix">InstructPix2Pix</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="strength">Strength (0.0-1.0):</label>
                        <input type="range" id="strength" name="strength" min="0.0" max="1.0" step="0.05" value="0.75">
                        <span id="strengthValue">0.75</span>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="guidance_scale">Guidance Scale:</label>
                        <input type="range" id="guidance_scale" name="guidance_scale" min="1.0" max="20.0" step="0.5" value="7.5">
                        <span id="guidanceValue">7.5</span>
                    </div>
                    
                    <div class="form-group">
                        <label for="num_steps">Steps:</label>
                        <input type="range" id="num_steps" name="num_steps" min="10" max="100" step="5" value="50">
                        <span id="stepsValue">50</span>
                    </div>
                </div>
                
                <button type="submit" class="btn" id="generateBtn">🎨 Generate Image</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Generating your image... This may take a few moments.</p>
            </div>
            
            <div class="result-section" id="resultSection" style="display: none;">
                <h3>Generated Image</h3>
                <img id="resultImage" class="result-image">
                <div id="resultInfo"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>&copy; 2024 Prodigy InfoTech. Developed by Tarun Agarwal.</p>
        </div>
    </div>
    
    <script>
        // File upload handling
        const fileUpload = document.getElementById('fileUpload');
        const fileInput = document.getElementById('image');
        
        fileUpload.addEventListener('click', () => fileInput.click());
        
        fileUpload.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUpload.classList.add('dragover');
        });
        
        fileUpload.addEventListener('dragleave', () => {
            fileUpload.classList.remove('dragover');
        });
        
        fileUpload.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUpload.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                updateFileDisplay();
            }
        });
        
        fileInput.addEventListener('change', updateFileDisplay);
        
        function updateFileDisplay() {
            const file = fileInput.files[0];
            if (file) {
                fileUpload.innerHTML = `<p>✅ ${file.name}</p><p style="font-size: 0.9rem; color: #666;">Click to change</p>`;
            }
        }
        
        // Range input value display
        document.getElementById('strength').addEventListener('input', (e) => {
            document.getElementById('strengthValue').textContent = e.target.value;
        });
        
        document.getElementById('guidance_scale').addEventListener('input', (e) => {
            document.getElementById('guidanceValue').textContent = e.target.value;
        });
        
        document.getElementById('num_steps').addEventListener('input', (e) => {
            document.getElementById('stepsValue').textContent = e.target.value;
        });
        
        // Form submission
        document.getElementById('generationForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData();
            const imageFile = document.getElementById('image').files[0];
            const prompt = document.getElementById('prompt').value;
            
            if (!imageFile) {
                alert('Please select an image file.');
                return;
            }
            
            if (!prompt.trim()) {
                alert('Please enter a prompt.');
                return;
            }
            
            formData.append('image', imageFile);
            formData.append('prompt', prompt);
            formData.append('model', document.getElementById('model').value);
            formData.append('strength', document.getElementById('strength').value);
            formData.append('guidance_scale', document.getElementById('guidance_scale').value);
            formData.append('num_steps', document.getElementById('num_steps').value);
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('resultSection').style.display = 'none';
            document.getElementById('generateBtn').disabled = true;
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('resultImage').src = result.image_data;
                    document.getElementById('resultInfo').innerHTML = `
                        <p><strong>Generation Time:</strong> ${result.metadata.generation_time.toFixed(2)}s</p>
                        <p><strong>Model:</strong> ${result.metadata.model}</p>
                        <p><strong>Parameters:</strong> Strength: ${result.metadata.strength}, Guidance: ${result.metadata.guidance_scale}, Steps: ${result.metadata.num_inference_steps}</p>
                    `;
                    document.getElementById('resultSection').style.display = 'block';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('generateBtn').disabled = false;
            }
        });
    </script>
</body>
</html>'''
    
    with open(templates_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    
    # Create demo.html template
    demo_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo - Image-to-Image Generation</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .demo-examples {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .example-card {
            border: 1px solid #e1e5e9;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        
        .example-card h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        
        .btn:hover {
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Demo Examples</h1>
            <p>Try these pre-configured examples to see the power of image-to-image generation</p>
        </div>
        
        <div class="demo-examples" id="demoExamples">
            <!-- Demo examples will be loaded here -->
        </div>
    </div>
    
    <script>
        // Load demo examples
        fetch('/api/demo-examples')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const container = document.getElementById('demoExamples');
                    data.examples.forEach(example => {
                        const card = document.createElement('div');
                        card.className = 'example-card';
                        card.innerHTML = `
                            <h3>${example.name}</h3>
                            <p><strong>Prompt:</strong> ${example.prompt}</p>
                            <p><strong>Model:</strong> ${example.model}</p>
                            <p><strong>Strength:</strong> ${example.strength}</p>
                            <button class="btn" onclick="runDemo('${example.name}')">Run Demo</button>
                        `;
                        container.appendChild(card);
                    });
                }
            });
            
        function runDemo(exampleName) {
            alert('Demo functionality would run: ' + exampleName);
            // In a real implementation, this would trigger the generation
        }
    </script>
</body>
</html>'''
    
    with open(templates_dir / "demo.html", "w", encoding="utf-8") as f:
        f.write(demo_html)
    
    print("🚀 Starting Flask Web Interface...")
    print("📱 Access the application at: http://localhost:5000")
    print("🎨 Developed by Tarun Agarwal for Prodigy InfoTech")
    
    app.run(
        host=WEB_SETTINGS['flask']['host'],
        port=WEB_SETTINGS['flask']['port'],
        debug=WEB_SETTINGS['flask']['debug']
    ) 