import streamlit as st
import os
from dotenv import load_dotenv
from orchestration.content_engine import generate_slide_outline, decide_slide_layout, generate_visual_keyword
from orchestration.visual_engine import create_presentation
from orchestration.image_engine import search_and_download_photo, get_supporting_images

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🎨 Presentation Generator",
    page_icon="🎨",
    layout="centered"
)

# Simple header
st.title("🎨 Majestic Presentation Generator")
st.markdown("**✨ Created by LAKSHMAN SINGH**")
st.markdown("Transform your ideas into stunning PowerPoint presentations with AI")

# Check API keys
def check_api_keys():
    gemini_key = os.getenv('GEMINI_API_KEY')
    pexels_key = os.getenv('PEXELS_API_KEY')
    return bool(gemini_key) and bool(pexels_key)

if not check_api_keys():
    st.error("⚠️ Missing API Keys! Please add GEMINI_API_KEY and PEXELS_API_KEY to your .env file")
    st.stop()

# Input form
st.header("🚀 Create Your Presentation")

with st.form("presentation_form"):
    topic = st.text_input(
        "📋 Presentation Topic",
        placeholder="e.g., Artificial Intelligence in Healthcare"
    )
    
    num_slides = st.slider("📊 Number of Slides", 3, 15, 6)
    
    style = st.selectbox("🎨 Style", ["dark", "light"])
    
    submitted = st.form_submit_button("🎯 Generate Presentation")

if submitted:
    if not topic.strip():
        st.error("❌ Please enter a presentation topic")
    else:
        with st.spinner("🔄 Generating your presentation... This may take a few minutes."):
            try:
                # Generate slide outline
                st.info("🧠 Generating content outline...")
                slides = generate_slide_outline(topic, num_slides)
                
                if not slides:
                    st.error("❌ Failed to generate slide outline")
                    st.stop()
                
                # Process slides
                st.info("🎨 Processing slides and adding images...")
                enriched_slides = []
                
                for i, slide_data in enumerate(slides):
                    # Set layout
                    if i == 0:
                        slide_data['layout'] = "Title Layout"
                    else:
                        slide_data['layout'] = decide_slide_layout(slide_data)
                    
                    # Generate and download background image
                    visual_keyword = generate_visual_keyword(slide_data['slide_title'], slide_data['slide_body'])
                    if visual_keyword:
                        image_path = search_and_download_photo(visual_keyword, is_background=True)
                        if image_path:
                            slide_data['image_path'] = image_path
                    
                    # Get supporting images for non-title slides
                    if i > 0:
                        supporting_images = get_supporting_images(slide_data)
                        if supporting_images:
                            slide_data['supporting_images'] = supporting_images
                    
                    enriched_slides.append(slide_data)
                
                # Create presentation
                st.info("📊 Creating PowerPoint presentation...")
                output_file = create_presentation(enriched_slides, topic, style, num_slides)
                
                # Success message
                st.success("🎉 Presentation generated successfully!")
                st.success(f"📁 File saved as: {output_file}")
                
                # Download button
                if os.path.exists(output_file):
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Presentation",
                            data=file.read(),
                            file_name=os.path.basename(output_file),
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("💡 **Tip**: Be specific with your topic for better results!")

# Sample topics
with st.expander("🎯 Sample Topics"):
    st.write("Click to copy:")
    sample_topics = [
        "Digital Marketing Strategies 2024",
        "Climate Change Solutions", 
        "Machine Learning Fundamentals",
        "Project Management Best Practices"
    ]
    for topic in sample_topics:
        st.code(topic)