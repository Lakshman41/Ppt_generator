import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
import config

def create_presentation(slides_data: list, topic: str) -> str:
    """
    Creates a professional PowerPoint presentation with visible background
    images on all slides and shadowed text for readability.
    """
    print("-> Creating final presentation with text shadows...")
    prs = Presentation()
    prs.slide_width = Inches(config.PPT_SLIDE_WIDTH_INCHES)
    prs.slide_height = Inches(config.PPT_SLIDE_HEIGHT_INCHES)
    
    blank_slide_layout = prs.slide_layouts[6]
    
    # --- TITLE SLIDE (The First Slide) ---
    if slides_data:
        title_slide_data = slides_data[0]
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # 1. Add background image as a shape
        if title_slide_data.get('image_path'):
            pic = slide.shapes.add_picture(
                title_slide_data.get('image_path'), 0, 0, width=prs.slide_width, height=prs.slide_height
            )
            # 2. Send the picture to the back
            slide.shapes._spTree.remove(pic._element)
            slide.shapes._spTree.insert(2, pic._element)

        # 3. Add text box for title and subtitle
        tx_box = slide.shapes.add_textbox(Inches(1.5), Inches(3), Inches(13), Inches(3))
        tx_frame = tx_box.text_frame
        tx_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        p_title = tx_frame.paragraphs[0]
        p_title.text = topic.title()
        p_title.alignment = PP_ALIGN.CENTER
        p_title.font.name = 'Calibri Light'
        p_title.font.size = Pt(54)
        p_title.font.bold = True
        p_title.font.color.rgb = RGBColor(255, 255, 255)
        p_title.font.shadow = True # ADD TEXT SHADOW

        p_subtitle = tx_frame.add_paragraph()
        p_subtitle.text = "An AI-Generated Presentation"
        p_subtitle.alignment = PP_ALIGN.CENTER
        p_subtitle.font.name = 'Calibri'
        p_subtitle.font.size = Pt(20)
        p_subtitle.font.color.rgb = RGBColor(220, 220, 220)
        p_subtitle.font.shadow = True # ADD TEXT SHADOW

        # Add speaker notes
        if title_slide_data.get('speaker_notes'):
            notes_slide = slide.notes_slide
            notes_slide.notes_text_frame.text = title_slide_data['speaker_notes']

    # --- CONTENT SLIDES (The Rest of the Slides) ---
    for slide_info in slides_data[1:]:
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # 1. Add background image
        if slide_info.get('image_path'):
            pic = slide.shapes.add_picture(
                slide_info.get('image_path'), 0, 0, width=prs.slide_width, height=prs.slide_height
            )
            # 2. Send the picture to the back
            slide.shapes._spTree.remove(pic._element)
            slide.shapes._spTree.insert(2, pic._element)
        
        # <<< --- FIX: REMOVED THE GRADIENT OVERLAY ENTIRELY --- >>>

        # 3. Add the text box
        tx_box = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(14), Inches(2.0))
        tx_frame = tx_box.text_frame
        tx_frame.word_wrap = True
        
        p_title = tx_frame.paragraphs[0]
        p_title.text = slide_info.get('slide_title', '')
        p_title.font.name = 'Calibri Light'
        p_title.font.size = Pt(36)
        p_title.font.bold = True
        p_title.font.color.rgb = RGBColor(255, 255, 255)
        p_title.font.shadow = True # ADD TEXT SHADOW
        
        p_body = tx_frame.add_paragraph()
        p_body.text = slide_info.get('slide_body', '')
        p_body.font.name = 'Calibri'
        p_body.font.size = Pt(20)
        p_body.font.color.rgb = RGBColor(230, 230, 230)
        p_body.line_spacing = 1.2
        p_body.font.shadow = True # ADD TEXT SHADOW

        # Add speaker notes
        if slide_info.get('speaker_notes'):
            notes_slide = slide.notes_slide
            # ... (rest of notes logic is fine)
            text_frame = notes_slide.notes_text_frame
            p = text_frame.paragraphs[0]
            p.text = f"Notes for: {slide_info.get('slide_title', '')}"
            p.font.bold = True
            p_notes = text_frame.add_paragraph()
            p_notes.text = slide_info['speaker_notes']

    # --- SAVE PRESENTATION ---
    safe_topic = re.sub(r'[\\/*?:"<>|]', "", topic).replace(" ", "_")
    output_filename = config.OUTPUT_DIR / f"{safe_topic}_presentation.pptx"
    
    prs.save(output_filename)
    print("-> Presentation created successfully.")
    return str(output_filename)