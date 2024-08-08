from PIL import Image, ImageDraw, ImageFont
import random
import string



def generate_captcha_text(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_captcha_image(text):
    width, height = 200, 100
    image = Image.new('RGB', (width, height), color='white')

    draw = ImageDraw.Draw(image)
    
    # Use a default PIL font
    font = ImageFont.load_default()
    
    # Calculate text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    
    draw.text((text_x, text_y), text, fill='black', font=font)
    
    return image
