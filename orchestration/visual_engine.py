from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import config
import re

def create_presentation(slides_data: list, topic: str) -> str:
    """
    Creates a PowerPoint presentation from the slide data.

    Args:
        slides_data (list): A list of slide dictionaries. Each must have
                            'slide_title' and 'image_path'.
        topic (str): The main topic, used for the filename.

    Returns:
        str: The path to the generated .pptx file.
    """
    print("-> Creating PowerPoint presentation...")
    prs = Presentation()
    prs.slide_width = Inches(config.PPT_SLIDE_WIDTH_INCHES)
    prs.slide_height = Inches(config.PPT_SLIDE_HEIGHT_INCHES)
    
    # Use a blank slide layout (layout index 6 is typically blank)
    blank_slide_layout = prs.slide_layouts[6]

    for slide_info in slides_data:
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # 1. Add background image
        if slide_info.get('image_path'):
            img_path = slide_info['image_path']
            # Add the picture to fill the slide
            slide.shapes.add_picture(
                img_path, 0, 0, width=prs.slide_width, height=prs.slide_height
            )
        
        # 2. Add title text
        title_text = slide_info.get('slide_title', ' ')
        
        # Add a semi-transparent box behind the text for readability
        # Left, Top, Width, Height
        tx_box_shape = slide.shapes.add_textbox(
            Inches(1), Inches(7.5), Inches(14), Inches(1.2)
        )
        fill = tx_box_shape.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(0, 0, 0) # Black
        # This requires a development version of python-pptx or a workaround.
        # For simplicity, we'll set transparency on the shape's line, which is not ideal.
        # A true overlay is more complex, so we'll just use a solid box for now.
        # We will improve this in the polish phase.

        # Add text to the box
        p = tx_box_shape.text_frame.paragraphs[0]
        p.text = title_text
        p.font.name = 'Calibri'
        p.font.size = Pt(40)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255) # White

    # Sanitize topic for filename
    safe_topic = re.sub(r'[\\/*?:"<>|]', "", topic).replace(" ", "_")
    output_filename = config.OUTPUT_DIR / f"{safe_topic}_presentation.pptx"
    
    prs.save(output_filename)
    print("-> Presentation created successfully.")
    return str(output_filename)