import cv2
import numpy as np
from PIL import Image

def generate_mock_heatmap(image: Image.Image) -> Image.Image:
    """
    Creates a mock augmented image highlighting 'anomalies' using OpenCV heatmaps and bounding boxes.
    """
    # Convert PIL Image to OpenCV format (RGB -> BGR)
    img_cv = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)
    
    height, width, _ = img_cv.shape
    
    # Simulate a heatmap overlay
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    
    # Blend original image with heatmap (mostly original)
    overlay = cv2.addWeighted(img_cv, 0.75, heatmap, 0.25, 0)
    
    # Generate geometric coordinates
    center_x, center_y = width // 2, height // 2
    offset_x = width // 8
    offset_y = height // 8
    
    # Draw mock targeting reticles and bounding boxes
    cv2.rectangle(overlay, (center_x - offset_x, center_y - offset_y), 
                  (center_x + offset_x, center_y + offset_y), (0, 0, 255), 3)
    
    cv2.line(overlay, (center_x - 30, center_y), (center_x + 30, center_y), (0, 255, 0), 2)
    cv2.line(overlay, (center_x, center_y - 30), (center_x, center_y + 30), (0, 255, 0), 2)
    
    # Adding a "SCAN CORTEX ACTIVE" fake HUD element
    cv2.putText(overlay, "EPIDERMIX AI SCAN", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (0, 255, 0), 2)
    
    # Convert back to PIL Image (BGR -> RGB)
    result = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    return result
