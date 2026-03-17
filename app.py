import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw
import io
from PIL import Image


# --- Load Logo ---
logo = Image.open("logo.png")

# --- Top Layout with Columns ---
col1, col2 = st.columns([1.5, 4])   # Adjust ratio for spacing

with col1:
    st.image(logo, width=250)  

with col2:
    st.markdown(
        "<h1 style='margin-bottom:0; color:#333; line-height:1;'>Image Editing Application</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='margin-top:0; color:#666; font-size:18px; line-height:1;'>Advanced Image Processing Tool</p>",
        unsafe_allow_html=True
    )

# --- INPUT SOURCE ---
st.sidebar.title("Input Source")
input_option = st.sidebar.radio("Select Input", ["Upload Image", "Use Webcam"])

image = None

if input_option == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)

else:
    camera_image = st.camera_input("Capture Image")
    if camera_image:
        image = Image.open(camera_image)

# --- IF IMAGE EXISTS ---
if image:

    original_img = image
    img = original_img.copy()

    # --- CONTROLS ---
    st.sidebar.title("Controls")

    # Basic
    st.sidebar.subheader("Basic")
    grayscale = st.sidebar.checkbox("Grayscale")
    invert = st.sidebar.checkbox("Invert Colors")

    # Resize
    st.sidebar.subheader("Resize")
    width = st.sidebar.slider("Width", 50, 1000, original_img.width)
    height = st.sidebar.slider("Height", 50, 1000, original_img.height)

    # Transform
    st.sidebar.subheader("Transform")
    angle = st.sidebar.slider("Rotate", 0, 360, 0)
    flip_h = st.sidebar.checkbox("Flip Horizontal")
    flip_v = st.sidebar.checkbox("Flip Vertical")

    # Adjust
    st.sidebar.subheader("Adjustments")
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)

    # Filters
    st.sidebar.subheader("Filters")
    filter_option = st.sidebar.selectbox(
        "Filter",
        ["None", "Blur", "Sharpen", "Edge Detection"]
    )

    # Text
    st.sidebar.subheader("Text")
    add_text = st.sidebar.checkbox("Add Text")
    text = st.sidebar.text_input("Enter Text")

    # --- PROCESSING ---
    if grayscale:
        img = ImageOps.grayscale(img)

    if invert:
        img = ImageOps.invert(img.convert("RGB"))

    img = img.rotate(angle, expand=True)

    if flip_h:
        img = ImageOps.mirror(img)
    if flip_v:
        img = ImageOps.flip(img)

    img = img.resize((width, height))

    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)

    if filter_option == "Blur":
        img = img.filter(ImageFilter.BLUR)
    elif filter_option == "Sharpen":
        img = img.filter(ImageFilter.SHARPEN)
    elif filter_option == "Edge Detection":
        img = img.filter(ImageFilter.FIND_EDGES)

    if add_text and text:
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), text, fill="white")

    # --- BEFORE/AFTER COMPARISON ---
    st.subheader("Comparison View")

    col1, col2 = st.columns(2)

    with col1:
        st.caption("Original")
        st.image(original_img, use_container_width=True)

    with col2:
        st.caption("Edited")
        st.image(img, use_container_width=True)

    # --- DOWNLOAD ---
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    st.download_button(
        "Download Edited Image",
        buf.getvalue(),
        "edited_image.png",
        "image/png"
    )

else:
    st.info("Upload or capture an image to begin.")
