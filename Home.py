import streamlit as st
import base64
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="Graphity - Home",
    layout="wide",
    # Set initial_sidebar_state to "collapsed" to start with sidebar hidden
    initial_sidebar_state="collapsed",
)

# Apply custom CSS to completely hide the sidebar
st.markdown("""
<style>
    /* Hide the sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Hide the sidebar toggle button */
    .css-1rs6os {
        display: none;
    }
    
    /* Hide the hamburger menu button */
    .css-fblp2m {
        display: none;
    }
    
    /* Make the main content take full width */
    .main .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

    .main-header {
        font-family: 'Poppins', 'Aileron', sans-serif !important;
        font-size: 5rem !important;
        text-align: center;
        color: black;
        margin: 50px 0 0 0;
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        color: #4776E6;
    }

    .feature-title {
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 10px;
        color: #1e3c72;
    }

    .feature-description {
        color: #666;
        margin-bottom: 15px;
    }

    .nav-button {
        background: linear-gradient(to right, #1e3c72, #4776E6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        cursor: pointer;
        transition: all 0.3s;
    }

    .nav-button:hover {
        background: linear-gradient(to right, #0c2b5e, #3060c9);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .welcome-section {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
    }

    .gallery-image {
        border-radius: 8px;
        margin-bottom: 10px;
        transition: transform 0.3s;
    }

    .gallery-image:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Background gradient
st.markdown('''
<style>
    .stApp {
        background: linear-gradient(to bottom, #ffffff, #f5f8fe);
    }
</style>''', unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>Graphity</h1>", unsafe_allow_html=True)

# Navigation buttons (optional) - Add these since sidebar is removed
#col1, col2, col3, col4 = st.columns(4)
#with col1:
 #   if st.button("Home", use_container_width=True):
#        st.switch_page("Home.py")
#with col2:
#    if st.button("Explorer", use_container_width=True):
#        st.switch_page("pages/explorer.py")
#with col3:
#    if st.button("Gallery", use_container_width=True):
 #       st.switch_page("pages/gallery.py")
#with col4:
#    if st.button("Tutorial", use_container_width=True):
#        st.switch_page("pages/tutorial.py")

st.markdown("<div class='welcome-section'>", unsafe_allow_html=True)
# Create a two-column layout
col1, col2 = st.columns([2, 1])  # Adjust the ratio as needed

# First column with welcome content
with col1:
    st.markdown("<h3 class='welcome-title'>Welcome to Graphity</h3>", unsafe_allow_html=True)
    st.markdown("""
    Discover the beauty of mathematical surfaces and functions in an interactive 3D environment.
    This tool allows you to visualize classic mathematical surfaces, create custom parametric surfaces,
    and explore the fascinating world of 3D geometry.
    """)
    
    # Why Graphity section
    st.markdown("<h4>Why Graphity?</h4>", unsafe_allow_html=True)
    st.markdown("""
    Graphity stands apart from conventional graphing tools with its intuitive interface and powerful capabilities:
    - **Real-time manipulation** of mathematical functions and parameters
    - **High-performance rendering** that handles complex surfaces smoothly
    - **Accessible mathematics** for students, educators, and enthusiasts alike
    - **No installation required** - runs directly in your browser
    """)
    
    # Applications section
    st.markdown("<h4>Applications</h4>", unsafe_allow_html=True)
    st.markdown("""
    Whether you're a student, educator, researcher, or simply curious about mathematics:

    - **Education**: Bring abstract concepts to life in classrooms and study sessions
    - **Research**: Visualize complex mathematical relationships for deeper understanding
    - **Art & Design**: Create stunning mathematical art based on elegant equations
    - **Engineering**: Model and understand 3D forms before applying them to real-world problems
    """)
    
    # Call to action
    st.markdown("**Ready to start exploring?**")
    st.markdown("[Launch Explorer](./explorer) 🚀")  # Link to explorer page

# Second column can be used for an image or additional content
with col2:
    # Placeholder for a logo or representative image
    st.image("gauss.png", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Featured graphs section
st.markdown("## Featured Surfaces")
st.markdown("Explore these classic mathematical surfaces with a single click.")

# Featured graphs in a grid
col1, col2, col3 = st.columns(3)

with col1:
    st.image("mobius.png", use_container_width=True, 
             caption="Möbius Strip")
    st.markdown("A non-orientable surface with only one side.")
    if st.button("Explore Möbius Strip", key="mobius"):
        st.switch_page("pages/explorer.py")  # This will pass parameters
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.image("klein.png", use_container_width=True,
             caption="Klein Bottle")
    st.markdown("A non-orientable surface with no boundary.")
    if st.button("Explore Klein Bottle", key="klein"):
        st.switch_page("pages/explorer.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.image("torus.png", use_container_width=True,
             caption="Torus")
    st.markdown("A surface of revolution generated by revolving a circle.")
    if st.button("Explore Torus", key="torus"):
        st.switch_page("pages/explorer.py")
    st.markdown("</div>", unsafe_allow_html=True)

# Features section
st.markdown("## Features")
st.markdown("Discover what you can do with the Graphity")

# Features in a grid
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='feature-icon'>📊</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-title'>Interactive 3D Visualization</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='feature-description'>
    Rotate, zoom, and pan to explore surfaces from any angle.
    Choose from various rendering styles and color schemes.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Try Visualization", key="viz"):
        st.switch_page("pages/explorer.py")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='feature-icon'>🧮</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-title'>Mathematical Function Builder</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='feature-description'>
    Create surfaces from custom mathematical functions.
    Support for both parametric equations and explicit functions.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Build Custom Functions", key="func"):
        st.switch_page("pages/explorer.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='feature-icon'>🎨</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-title'>Custom Appearance</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='feature-description'>
    Choose from various colormaps including vibrant custom themes.
    Adjust transparency, wireframe visibility, and other visual properties.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Customize Appearance", key="appear"):
        st.switch_page("pages/explorer.py")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='feature-icon'>📚</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-title'>Mathematical Insights</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='feature-description'>
    Learn about each surface's mathematical properties and equations.
    Explore the relationship between equations and geometric shapes.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Learn More", key="learn"):
        st.switch_page("pages/explorer.py")
    st.markdown("</div>", unsafe_allow_html=True)

# Getting started section
with st.expander("Getting Started Guide"):
    st.markdown("""
    ### Quick Start Guide
    
    1. **Choose a surface**: Select from predefined surfaces or create your own
    2. **Customize appearance**: Choose colors, transparency, and rendering style
    3. **Interact**: Explore the 3D visualization with mouse controls
    4. **Learn**: Expand the information panel to understand the mathematics
    
    ### Tips for Beginners
    
    - Start with predefined surfaces to get familiar with the controls
    - Try different color maps to highlight different features of the surfaces
    - Use the "Surface + Wireframe" rendering style for better spatial understanding
    - Experiment with different parameter ranges for custom surfaces
    """)

# Footer
st.markdown("""
<div class='footer'>
    <p>Graphity - Created by Aaryan Singh, Navreh Koul, Kumar Varchasva, Sagar Qazi and Shruti Malik</p>
    <p>© 2025 - Version 3.1415926</p>
</div>
""", unsafe_allow_html=True)