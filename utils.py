from PIL import Image
import io

def get_transparent_pixel_png() -> io.BytesIO:
    """
    Generates a 1x1 transparent PNG image in memory.

    Returns:
        io.BytesIO: A bytes buffer containing the PNG data.
    """

    # Create a 1x1 image with 4 channels (RGBA)
    img = Image.new('RGBA', (1, 1), (0, 0, 0, 0)) # R, G, B, Alpha are all 0
    
    # Save the image to a bytes buffer
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    
    # Rewind the buffer to the beginning
    byte_io.seek(0)
    return byte_io