import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE_TYPE
import config
import os

def create_presentation(enriched_slides: list, topic: str, style: str = 'dark') -> str:
    print("-> Drawing presentation from scratch...")
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_layout = prs.slide_layouts[6]
    
    # Enhanced theme configuration
    themes = {
        'dark': {
            'font': 'Calibri',
            'text': RGBColor(255, 255, 255),
            'subtext': RGBColor(200, 200, 200),
            'bg': RGBColor(45, 52, 54),
            'accent': RGBColor(52, 152, 219),
            'secondary': RGBColor(44, 62, 80)
        },
        'light': {
            'font': 'Calibri',
            'text': RGBColor(30, 30, 30),
            'subtext': RGBColor(80, 80, 80),
            'bg': RGBColor(248, 249, 250),
            'accent': RGBColor(41, 128, 185),
            'secondary': RGBColor(52, 73, 94)
        }
    }
    theme = themes.get(style, themes['dark'])

    # Add title slide
    slide = prs.slides.add_slide(blank_layout)
    _draw_title_slide(slide, prs, {'slide_title': topic}, theme, topic)

    # Add table of contents
    slide = prs.slides.add_slide(blank_layout)
    _draw_toc_slide(slide, prs, enriched_slides, theme)

    # Add content slides
    for i, slide_data in enumerate(enriched_slides):
        slide = prs.slides.add_slide(blank_layout)
        layout = slide_data.get('layout', 'Photo Layout')
        
        if "Diagram" in layout and slide_data.get('image_path'):
            _draw_diagram_slide(slide, prs, slide_data, theme)
        else:
            _draw_photo_slide(slide, prs, slide_data, theme)

    safe_topic = re.sub(r'[\\/*?:"<>|]', "", topic).replace(" ", "_")
    output_filename = config.PPTConfig.PATHS['output'] / f"{safe_topic}_{style}_presentation.pptx"
    prs.save(output_filename)
    print(f"-> Majestic presentation saved: {output_filename}")
    return str(output_filename)

def _add_image_as_background(slide, prs, image_path):
    if image_path:
        print(f"DEBUG: Adding background image: {image_path}")
        if not os.path.exists(image_path):
            print(f"WARNING: Background image file not found: {image_path}")
        else:
            # Add main background image with proper sizing
            pic = slide.shapes.add_picture(image_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
            slide.shapes._spTree.remove(pic._element)
            slide.shapes._spTree.insert(2, pic._element)
            
            # Add gradient overlay for better text readability
            overlay = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
            fill = overlay.fill
            fill.gradient()
            fill.gradient_stops[0].position = 0
            fill.gradient_stops[0].color.rgb = RGBColor(0, 0, 0)
            fill.gradient_stops[0].color.brightness = 0.6
            fill.gradient_stops[1].position = 1
            fill.gradient_stops[1].color.rgb = RGBColor(0, 0, 0)
            fill.gradient_stops[1].color.brightness = 0.3
            overlay.line.fill.background()

def _draw_title_slide(slide, prs, slide_data, theme, topic):
    _add_image_as_background(slide, prs, slide_data.get('image_path'))
    
    # Add decorative elements
    accent_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2), Inches(2), Inches(12), Inches(5))
    accent_shape.fill.solid()
    accent_shape.fill.fore_color.rgb = theme['accent']
    accent_shape.fill.fore_color.brightness = 0.2
    accent_shape.line.fill.background()
    
    # Title text
    tx_box = slide.shapes.add_textbox(Inches(2.5), Inches(3), Inches(11), Inches(3))
    p = tx_box.text_frame.paragraphs[0]
    p.text = topic
    p.font.name = theme['font']
    p.font.size = Pt(60)
    p.font.bold = True
    p.font.color.rgb = theme['text']
    p.alignment = PP_ALIGN.CENTER

def _draw_toc_slide(slide, prs, slides, theme):
    # Add a relevant background image
    if slides and slides[0].get('image_path'):
        _add_image_as_background(slide, prs, slides[0]['image_path'])
    
    # Add semi-transparent overlay for better readability
    overlay = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = theme['bg']
    overlay.fill.fore_color.brightness = 0.8
    overlay.line.fill.background()
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(14), Inches(1))
    title_frame = title_box.text_frame
    p = title_frame.paragraphs[0]
    p.text = "Table of Contents"
    p.font.name = theme['font']
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = theme['text']
    
    # Content
    content_box = slide.shapes.add_textbox(Inches(2), Inches(2.5), Inches(12), Inches(5))
    content_frame = content_box.text_frame
    
    for i, slide_data in enumerate(slides, 1):
        p = content_frame.add_paragraph()
        p.text = f"{i}. {slide_data['slide_title']}"
        p.font.name = theme['font']
        p.font.size = Pt(24)
        p.font.color.rgb = theme['text']
        p.space_after = Pt(12)

def _draw_photo_slide(slide, prs, slide_data, theme):
    _add_image_as_background(slide, prs, slide_data.get('image_path'))
    
    # Add content box with semi-transparent background
    content_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(5.5), Inches(14), Inches(3))
    content_box.fill.solid()
    content_box.fill.fore_color.rgb = theme['secondary']
    content_box.fill.fore_color.brightness = 0.2
    content_box.line.fill.background()
    
    # Title and body text
    tx_box = slide.shapes.add_textbox(Inches(1.5), Inches(5.75), Inches(13), Inches(2.5))
    tx_frame = tx_box.text_frame
    
    p = tx_frame.paragraphs[0]
    p.text = slide_data.get('slide_title', '')
    p.font.name = theme['font']
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = theme['text']
    p.space_after = Pt(12)
    
    p2 = tx_frame.add_paragraph()
    p2.text = slide_data.get('slide_body', '')
    p2.font.name = theme['font']
    p2.font.size = Pt(24)
    p2.font.color.rgb = theme['subtext']
    p2.line_spacing = 1.3
    
    # Add supporting images if available
    supporting_images = slide_data.get('supporting_images', [])
    if supporting_images:
        print(f"DEBUG: Adding supporting images: {supporting_images}")
        
        # Calculate grid layout for supporting images
        num_images = len(supporting_images)
        if num_images == 1:
            # Single image layout
            img_height = Inches(4)
            img_width = Inches(6)
            img_left = Inches(9)
            img_top = Inches(1)
            slide.shapes.add_picture(supporting_images[0], img_left, img_top, width=img_width, height=img_height)
        elif num_images == 2:
            # Two images side by side
            img_height = Inches(3)
            img_width = Inches(5)
            img_gap = Inches(0.5)
            img_top = Inches(1)
            
            # First image
            slide.shapes.add_picture(supporting_images[0], Inches(9), img_top, width=img_width, height=img_height)
            # Second image
            slide.shapes.add_picture(supporting_images[1], Inches(9), img_top + img_height + img_gap, width=img_width, height=img_height)
        else:
            # Three or more images in a grid
            img_height = Inches(2.5)
            img_width = Inches(4)
            img_gap = Inches(0.3)
            img_top = Inches(1)
            img_left = Inches(9)
            
            for idx, img_path in enumerate(supporting_images[:3]):  # Limit to 3 images
                if not os.path.exists(img_path):
                    print(f"WARNING: Supporting image file not found: {img_path}")
                    continue
                row = idx // 2
                col = idx % 2
                left = img_left + (img_width + img_gap) * col
                top = img_top + (img_height + img_gap) * row
                slide.shapes.add_picture(img_path, left, top, width=img_width, height=img_height)

def _draw_diagram_slide(slide, prs, slide_data, theme):
    # Add a relevant background image
    if slide_data.get('background_image'):
        _add_image_as_background(slide, prs, slide_data['background_image'])
    else:
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = theme['bg']
    
    # Add decorative header
    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.5))
    header.fill.solid()
    header.fill.fore_color.rgb = theme['accent']
    header.line.fill.background()
    
    # Title
    tx_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.25), Inches(7), Inches(1))
    tx_frame = tx_box.text_frame
    p = tx_frame.paragraphs[0]
    p.text = slide_data.get('slide_title', '')
    p.font.name = theme['font']
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = theme['text']
    
    # Content
    content_box = slide.shapes.add_textbox(Inches(0.75), Inches(2), Inches(7), Inches(6))
    content_frame = content_box.text_frame
    p2 = content_frame.paragraphs[0]
    p2.text = slide_data.get('slide_body', '')
    p2.font.name = theme['font']
    p2.font.size = Pt(22)
    p2.font.color.rgb = theme['subtext']
    p2.line_spacing = 1.3
    
    # Diagram
    if slide_data.get('image_path'):
        img_height = Inches(6)
        img_top = Inches(2)
        if not os.path.exists(slide_data['image_path']):
            print(f"WARNING: Diagram image file not found: {slide_data['image_path']}")
        else:
            slide.shapes.add_picture(slide_data['image_path'], Inches(8.25), img_top, height=img_height)