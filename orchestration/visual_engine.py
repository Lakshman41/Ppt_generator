import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
import config # It now imports the class-based config

def create_presentation(enriched_slides: list, topic: str, style: str = 'dark') -> str:
    print("-> Drawing presentation from scratch...")
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_layout = prs.slide_layouts[6]
    themes = {
        'dark': {'font': 'Calibri', 'text': RGBColor(255, 255, 255), 'subtext': RGBColor(200, 200, 200), 'bg': RGBColor(45, 52, 54)},
        'light': {'font': 'Calibri', 'text': RGBColor(30, 30, 30), 'subtext': RGBColor(80, 80, 80), 'bg': RGBColor(248, 249, 250)},
    }
    theme = themes.get(style, themes['dark'])

    for i, slide_data in enumerate(enriched_slides):
        slide = prs.slides.add_slide(blank_layout)
        layout = slide_data.get('layout', 'Photo Layout')
        if i == 0:
            _draw_title_slide(slide, prs, slide_data, theme, topic)
        elif "Diagram" in layout and slide_data.get('image_path'):
            _draw_diagram_slide(slide, prs, slide_data, theme)
        else:
            _draw_photo_slide(slide, prs, slide_data, theme)

    safe_topic = re.sub(r'[\\/*?:"<>|]', "", topic).replace(" ", "_")
    output_filename = config.PPTConfig.PATHS['output'] / f"{safe_topic}_{style}_presentation.pptx" # Use new config
    prs.save(output_filename)
    print(f"-> Majestic presentation saved: {output_filename}")
    return str(output_filename)

def _add_image_as_background(slide, prs, image_path):
    if image_path:
        pic = slide.shapes.add_picture(image_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
        slide.shapes._spTree.remove(pic._element)
        slide.shapes._spTree.insert(2, pic._element)

def _draw_title_slide(slide, prs, slide_data, theme, topic):
    # ... (code is correct) ...
    _add_image_as_background(slide, prs, slide_data.get('image_path'))
    tx_box = slide.shapes.add_textbox(Inches(2), Inches(3), Inches(12), Inches(3))
    p = tx_box.text_frame.paragraphs[0]
    p.text = topic
    p.font.name, p.font.size, p.font.bold, p.font.color.rgb = theme['font'], Pt(60), True, theme['text']
    p.alignment = PP_ALIGN.CENTER
    scrim = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    fill = scrim.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0,0,0)
    fill.fore_color.brightness = 0.4
    scrim.line.fill.background()

def _draw_photo_slide(slide, prs, slide_data, theme):
    # ... (code is correct) ...
    _add_image_as_background(slide, prs, slide_data.get('image_path'))
    tx_box = slide.shapes.add_textbox(Inches(1), Inches(6), Inches(14), Inches(2.5))
    tx_frame = tx_box.text_frame
    p = tx_frame.paragraphs[0]
    p.text = slide_data.get('slide_title', '')
    p.font.name, p.font.size, p.font.bold, p.font.color.rgb = theme['font'], Pt(40), True, theme['text']
    p2 = tx_frame.add_paragraph()
    p2.text = slide_data.get('slide_body', '')
    p2.font.name, p2.font.size, p2.font.color.rgb = theme['font'], Pt(24), theme['subtext']

def _draw_diagram_slide(slide, prs, slide_data, theme):
    # ... (code is correct) ...
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = theme['bg']
    tx_box = slide.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(7), Inches(6))
    tx_frame = tx_box.text_frame
    p = tx_frame.paragraphs[0]
    p.text = slide_data.get('slide_title', '')
    p.font.name, p.font.size, p.font.bold, p.font.color.rgb = theme['font'], Pt(40), True, theme['text']
    p.line_spacing = 1.2
    p2 = tx_frame.add_paragraph()
    p2.text = "\n" + slide_data.get('slide_body', '')
    p2.font.name, p2.font.size, p2.font.color.rgb = theme['font'], Pt(22), theme['subtext']
    p2.line_spacing = 1.3
    if slide_data.get('image_path'):
        img_height = Inches(6)
        img_top = Inches((9.0 - 6) / 2)
        slide.shapes.add_picture(slide_data['image_path'], Inches(8.25), img_top, height=img_height)