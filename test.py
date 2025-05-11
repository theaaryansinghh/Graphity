import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy.utilities.lambdify import lambdify
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from io import BytesIO

DEFAULT_U_RES = 100
DEFAULT_V_RES = 50



# Add this after your imports and page config but before the main code

# Configure page
st.set_page_config(
    page_title="3D Graph Explorer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Set default values for u_res and v_res in session state
if 'u_res' not in st.session_state:
    st.session_state.u_res = 100  # Default U resolution
if 'v_res' not in st.session_state:
    st.session_state.v_res = 50   # Default V resolution

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        background: linear-gradient(135deg, #1e3c72, #2a5298, #4776E6);
        color: white !important;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    # Rest of your CSS...
    .stExpander {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .sidebar-header {
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 12px;
        color: #1e3c72;
        border-bottom: 2px solid #e6eef8;
        padding-bottom: 5px;
    }
    .graph-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #e0e0e0;
        font-size: 0.85em;
        color: #666;
    }
    .stButton>button {
        background: linear-gradient(to right, #1e3c72, #4776E6);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #0c2b5e, #3060c9);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    .stSlider>div>div>div {
        background-color: #4776E6;
    }
    .info-box {
        background-color: #f8f9fa;
        border-left: 4px solid #1e3c72;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    .css-6qob1r.e1fqkh3o3 {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
    }
    .css-1outpf7.e16nr0p31 label {
        font-weight: 500;
        color: #1e3c72;
    }
</style>
""", unsafe_allow_html=True)

# Background gradient for app
st.markdown('''
<style>
    .stApp {
        background: linear-gradient(to bottom, #ffffff, #f5f8fe);
    }
</style>''', unsafe_allow_html=True)

# Header with gradient background
st.markdown("<h1 class='main-header'>Interactive 3D Graph Explorer</h1>", unsafe_allow_html=True)

# Function to create predefined graphs
def create_mobius_strip(u_res, v_res):
    u = np.linspace(0, 2 * np.pi, u_res)
    v = np.linspace(-1, 1, v_res)
    u, v = np.meshgrid(u, v)
    
    x = (1 + 0.5 * v * np.cos(u / 2)) * np.cos(u)
    y = (1 + 0.5 * v * np.cos(u / 2)) * np.sin(u)
    z = 0.5 * v * np.sin(u / 2)
    
    return x, y, z, "Möbius Strip"

def create_klein_bottle(u_res, v_res):
    u = np.linspace(0, 2 * np.pi, u_res)
    v = np.linspace(0, 2 * np.pi, v_res)
    u, v = np.meshgrid(u, v)
    
    r = 4 * (1 - np.cos(u) / 2)
    
    x = 6 * np.cos(u) * (1 + np.sin(u)) + r * np.cos(v + np.pi)
    y = 16 * np.sin(u)
    z = 6 * np.cos(u) * (1 + np.sin(u)) + r * np.sin(v)
    
    return x, y, z, "Klein Bottle"

def create_torus(u_res, v_res, R=2, r=0.5):
    u = np.linspace(0, 2 * np.pi, u_res)
    v = np.linspace(0, 2 * np.pi, v_res)
    u, v = np.meshgrid(u, v)
    
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    
    return x, y, z, "Torus"

def create_sphere(u_res, v_res, r=1):
    u = np.linspace(0, 2 * np.pi, u_res)
    v = np.linspace(0, np.pi, v_res)
    u, v = np.meshgrid(u, v)
    
    x = r * np.sin(v) * np.cos(u)
    y = r * np.sin(v) * np.sin(u)
    z = r * np.cos(v)
    
    return x, y, z, "Sphere"

def create_custom_function(u_res, v_res, x_expr, y_expr, z_expr, u_min, u_max, v_min, v_max):
    # Parse expressions
    try:
        u_sym, v_sym = sp.symbols('u v')
        
        x_func = lambdify((u_sym, v_sym), parse_expr(x_expr), 'numpy')
        y_func = lambdify((u_sym, v_sym), parse_expr(y_expr), 'numpy')
        z_func = lambdify((u_sym, v_sym), parse_expr(z_expr), 'numpy')
        
        u = np.linspace(u_min, u_max, u_res)
        v = np.linspace(v_min, v_max, v_res)
        u, v = np.meshgrid(u, v)
        
        x = x_func(u, v)
        y = y_func(u, v)
        z = z_func(u, v)
        
        return x, y, z, "Custom Parametric Surface"
    except Exception as e:
        st.error(f"Error evaluating expressions: {str(e)}")
        return None, None, None, None

def create_custom_explicit(u_res, v_res, z_expr, x_min, x_max, y_min, y_max):
    try:
        x_sym, y_sym = sp.symbols('x y')
        
        z_func = lambdify((x_sym, y_sym), parse_expr(z_expr), 'numpy')
        
        x = np.linspace(x_min, x_max, u_res)
        y = np.linspace(y_min, y_max, v_res)
        x, y = np.meshgrid(x, y)
        
        z = z_func(x, y)
        
        return x, y, z, "Custom Explicit Surface z=f(x,y)"
    except Exception as e:
        st.error(f"Error evaluating expression: {str(e)}")
        return None, None, None, None

# Create color maps
def get_color_maps():
    # Standard colormaps
    standard_maps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis',
                    'Spectral', 'coolwarm', 'rainbow', 'jet']
    
    # Create custom colormaps
    custom_maps = {}
    
    # Ocean theme
    ocean_colors = [(0, '#03045e'), (0.25, '#0077b6'), 
                    (0.5, '#00b4d8'), (0.75, '#90e0ef'), (1, '#caf0f8')]
    custom_maps['ocean'] = LinearSegmentedColormap.from_list('ocean', ocean_colors)
    
    # Sunset theme
    sunset_colors = [(0, '#4a0a77'), (0.25, '#b5179e'), 
                     (0.5, '#f72585'), (0.75, '#fb8500'), (1, '#ffcf55')]
    custom_maps['sunset'] = LinearSegmentedColormap.from_list('sunset', sunset_colors)
    
    # Forest theme
    forest_colors = [(0, '#081c15'), (0.25, '#1b4332'), 
                     (0.5, '#2d6a4f'), (0.75, '#52b788'), (1, '#d8f3dc')]
    custom_maps['forest'] = LinearSegmentedColormap.from_list('forest', forest_colors)
    
    # Galaxy theme
    galaxy_colors = [(0, '#0d1b2a'), (0.25, '#1b263b'), 
                     (0.5, '#415a77'), (0.75, '#778da9'), (1, '#e0e1dd')]
    custom_maps['galaxy'] = LinearSegmentedColormap.from_list('galaxy', galaxy_colors)
    
    # Fire theme
    fire_colors = [(0, '#370617'), (0.25, '#9d0208'), 
                   (0.5, '#dc2f02'), (0.75, '#f48c06'), (1, '#ffba08')]
    custom_maps['fire'] = LinearSegmentedColormap.from_list('fire', fire_colors)
    
    return standard_maps, custom_maps

# Convert matplotlib colormap to plotly colorscale
def convert_colormap_to_colorscale(colormap_name, custom_maps):
    if colormap_name in custom_maps:
        cmap = custom_maps[colormap_name]
        # Sample the colormap at 11 points
        colors = cmap(np.linspace(0, 1, 11))
        return [(i/10, f'rgb({int(r*255)},{int(g*255)},{int(b*255)})') 
                for i, (r, g, b, _) in enumerate(colors)]
    else:
        # For standard colormaps, use the name directly in plotly
        return colormap_name

# Sidebar for controls
# Sidebar for controls
with st.sidebar:
    st.markdown("<div class='sidebar-header'>Graph Selection</div>", unsafe_allow_html=True)
    graph_type = st.selectbox(
        "Select Graph Type", 
        ["Möbius Strip", "Klein Bottle", "Torus", "Sphere", 
         "Custom Parametric Surface", "Custom Explicit Surface z=f(x,y)"]
    )
    
    # Parameters specific to each graph type
    if graph_type == "Torus":
        col1, col2 = st.columns(2)
        with col1:
            torus_R = st.slider("Major Radius (R)", 0.5, 5.0, 2.0, 0.1)
        with col2:
            torus_r = st.slider("Minor Radius (r)", 0.1, 3.0, 0.5, 0.1)
    
    elif graph_type == "Sphere":
        sphere_r = st.slider("Radius", 0.1, 5.0, 1.0, 0.1)
    
    elif graph_type == "Custom Parametric Surface":
        st.markdown("### Define Parametric Equations")
        st.markdown("<div class='info-box'>Use `u` and `v` as parameters</div>", unsafe_allow_html=True)
        
        x_expr = st.text_input("x(u,v) = ", "(1 + 0.5*cos(v))*cos(u)")
        y_expr = st.text_input("y(u,v) = ", "(1 + 0.5*cos(v))*sin(u)")
        z_expr = st.text_input("z(u,v) = ", "0.5*sin(v)")
        
        col1, col2 = st.columns(2)
        with col1:
            u_min = st.number_input("u min", value=0.0)
            v_min = st.number_input("v min", value=0.0)
        with col2:
            u_max = st.number_input("u max", value=2*np.pi)
            v_max = st.number_input("v max", value=2*np.pi)
    
    elif graph_type == "Custom Explicit Surface z=f(x,y)":
        st.markdown("### Define Function")
        st.markdown("<div class='info-box'>Use `x` and `y` as variables</div>", unsafe_allow_html=True)
        
        z_expr = st.text_input("z(x,y) = ", "sin(sqrt(x**2 + y**2))")
        
        col1, col2 = st.columns(2)
        with col1:
            x_min = st.number_input("x min", value=-5.0)
            y_min = st.number_input("y min", value=-5.0)
        with col2:
            x_max = st.number_input("x max", value=5.0)
            y_max = st.number_input("y max", value=5.0)
    
    # Create an expander for all visualization options
    with st.expander("Visualization Options"):
        # Color settings     
        standard_maps, custom_maps = get_color_maps()     
        all_colormaps = standard_maps + list(custom_maps.keys())     
        colormap = st.selectbox("Color Map", all_colormaps, index=0)          
        
        # Plot settings     
        plot_style = st.radio("Rendering Style", ["Surface", "Wireframe", "Surface + Wireframe"])     
        alpha = st.slider("Transparency", 0.0, 1.0, 0.8, 0.05)          
        
        # Additional options     
        show_grid = st.checkbox("Show Grid", value=True)     
        show_axes = st.checkbox("Show Axes", value=True)     
        show_colorbar = st.checkbox("Show Color Bar", value=True)     
        # Add this after the show_colorbar checkbox     
        auto_rotate = st.checkbox("Auto-Rotate Graph", value=False)     
        rotation_speed = st.slider("Rotation Speed", 0.001, 0.1, 0.01, 0.001, disabled=not auto_rotate)

    # Keep the actions section outside the expander
    st.markdown("<h3>Actions</h3>", unsafe_allow_html=True)     
    apply_button = st.button("Generate Graph", use_container_width=True)      

    
# Main area for visualization
if 'last_graph_params' not in st.session_state:
    st.session_state.last_graph_params = None

current_params = {
    'graph_type': graph_type,
    'u_res': st.session_state.u_res,  # Use session state value instead of slider
    'v_res': st.session_state.v_res,  # Use session state value instead of slider
    'colormap': colormap,
    'plot_style': plot_style,
    'alpha': alpha,
    'show_grid': show_grid,
    'show_axes': show_axes,
    'show_colorbar': show_colorbar
}

# Add specific parameters based on graph type
if graph_type == "Torus":
    current_params['torus_R'] = torus_R
    current_params['torus_r'] = torus_r
elif graph_type == "Sphere":
    current_params['sphere_r'] = sphere_r
elif graph_type == "Custom Parametric Surface":
    current_params.update({
        'x_expr': x_expr,
        'y_expr': y_expr,
        'z_expr': z_expr,
        'u_min': u_min,
        'u_max': u_max,
        'v_min': v_min,
        'v_max': v_max
    })
elif graph_type == "Custom Explicit Surface z=f(x,y)":
    current_params.update({
        'z_expr': z_expr,
        'x_min': x_min,
        'x_max': x_max,
        'y_min': y_min,
        'y_max': y_max
    })

# Check if we should update the graph
should_update = apply_button or (st.session_state.last_graph_params is None)

if should_update:
    st.session_state.last_graph_params = current_params
    
    # Generate the surface data based on graph type
    if graph_type == "Möbius Strip":
        x, y, z, title = create_mobius_strip(st.session_state.u_res, st.session_state.v_res)
    elif graph_type == "Klein Bottle":
        x, y, z, title = create_klein_bottle(st.session_state.u_res, st.session_state.v_res)
    elif graph_type == "Torus":
        x, y, z, title = create_torus(st.session_state.u_res, st.session_state.v_res, torus_R, torus_r)
    elif graph_type == "Sphere":
        x, y, z, title = create_sphere(st.session_state.u_res, st.session_state.v_res, sphere_r)
    elif graph_type == "Custom Parametric Surface":
        x, y, z, title = create_custom_function(st.session_state.u_res, st.session_state.v_res, x_expr, y_expr, z_expr, u_min, u_max, v_min, v_max)
    elif graph_type == "Custom Explicit Surface z=f(x,y)":
        x, y, z, title = create_custom_explicit(st.session_state.u_res, st.session_state.v_res, z_expr, x_min, x_max, y_min, y_max)
    
    if x is not None:
        st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
        
        # Convert matplotlib colormap to plotly colorscale
        colorscale = convert_colormap_to_colorscale(colormap, custom_maps)
        
        # Create interactive Plotly figure
        fig = go.Figure()
        
        # Add surface based on style
        if plot_style == "Surface" or plot_style == "Surface + Wireframe":
            surface_opacity = alpha
            showscale = show_colorbar
            
            fig.add_trace(
                go.Surface(
                    x=x, y=y, z=z,
                    colorscale=colorscale,
                    opacity=surface_opacity,
                    showscale=showscale,
                    contours={
                        "x": {"show": plot_style == "Surface + Wireframe", "width": 1, "color": "black"},
                        "y": {"show": plot_style == "Surface + Wireframe", "width": 1, "color": "black"},
                        "z": {"show": plot_style == "Surface + Wireframe", "width": 1, "color": "black"}
                    }
                )
            )
        
        if plot_style == "Wireframe":
            # For wireframe only, need to use mesh3d or add multiple line traces
            for i in range(x.shape[0]):
                fig.add_trace(
                    go.Scatter3d(
                        x=x[i,:], y=y[i,:], z=z[i,:],
                        mode='lines',
                        line=dict(color='black', width=1.5),
                        opacity=alpha,
                        showlegend=False
                    )
                )
            
            for j in range(x.shape[1]):
                fig.add_trace(
                    go.Scatter3d(
                        x=x[:,j], y=y[:,j], z=z[:,j],
                        mode='lines',
                        line=dict(color='black', width=1.5),
                        opacity=alpha,
                        showlegend=False
                    )
                )
        
        # Set layout for the figure
        camera = dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
        
        # Calculate ranges for axes
        max_range = np.array([
            x.max() - x.min(),
            y.max() - y.min(),
            z.max() - z.min()
        ]).max() / 2.0
        
        mid_x = (x.max() + x.min()) / 2
        mid_y = (y.max() + y.min()) / 2
        mid_z = (z.max() + z.min()) / 2
        
        # Set layout with improved styling
        fig.update_layout(
            title={
                'text': f"<b>{title}</b>",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=24, color='#1e3c72')
            },
            scene=dict(
                xaxis=dict(
                    title="X-axis",
                    visible=show_axes,
                    showgrid=show_grid,
                    range=[mid_x - max_range, mid_x + max_range]
                ),
                yaxis=dict(
                    title="Y-axis",
                    visible=show_axes,
                    showgrid=show_grid,
                    range=[mid_y - max_range, mid_y + max_range]
                ),
                zaxis=dict(
                    title="Z-axis",
                    visible=show_axes,
                    showgrid=show_grid,
                    range=[mid_z - max_range, mid_z + max_range]
                ),
                aspectmode='cube',
                camera=camera
            ),
            width=900,
            height=750,
            margin=dict(l=0, r=0, b=0, t=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif")
        )
        
        # Add an informational note about interactivity
        st.info("👆 **Interactive Controls**: Click and drag to rotate, scroll to zoom, shift+click to pan.")
        
        # Display the interactive 3D plot
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add information about the current graph
        with st.expander("Graph Information"):
            if graph_type == "Möbius Strip":
                st.markdown("""
                ### Möbius Strip
                
                **Mathematical Definition:**
                A non-orientable surface with only one side and one boundary component.
                
                **Parametric Equations:**
                ```
                x = (1 + (v/2)cos(u/2))cos(u)
                y = (1 + (v/2)cos(u/2))sin(u)
                z = (v/2)sin(u/2)
                ```
                Where:
                - u ∈ [0, 2π) (angular parameter)
                - v ∈ [-1, 1] (width parameter)
                
                **Key Properties:**
                - Single-sided surface
                - Non-orientable
                - Euler characteristic: χ = 0
                - Requires 720° rotation to return to initial state
                """)
            elif graph_type == "Klein Bottle":
                st.markdown("""
                ### Klein Bottle
                
                **Mathematical Definition:**
                A non-orientable surface with no boundary that cannot be embedded in three-dimensional space without intersecting itself.
                
                **Key Properties:**
                - Non-orientable surface
                - Has no inside or outside
                - Cannot be properly embedded in 3D space
                - Self-intersects in this 3D representation
                - Euler characteristic: χ = 0
                
                The representation shown is a common visualization of the Klein bottle in 3D space, though a true Klein bottle requires 4D space to exist without self-intersection.
                """)
            elif graph_type == "Torus":
                st.markdown(f"""
                ### Torus
                
                **Mathematical Definition:**
                A surface of revolution generated by revolving a circle around an axis coplanar with the circle.
                
                **Parametric Equations:**
                ```
                x = (R + r*cos(v))*cos(u)
                y = (R + r*cos(v))*sin(u)
                z = r*sin(v)
                ```
                Where:
                - R = {torus_R} (major radius)
                - r = {torus_r} (minor radius)
                - u, v ∈ [0, 2π)
                
                **Key Properties:**
                - Orientable surface
                - Genus 1 (it has one "hole")
                - Euler characteristic: χ = 0
                """)
            elif graph_type == "Sphere":
                st.markdown(f"""
                ### Sphere
                
                **Mathematical Definition:**
                The set of all points in 3D space that are equidistant from a fixed point (the center).
                
                **Parametric Equations:**
                ```
                x = r*sin(v)*cos(u)
                y = r*sin(v)*sin(u)
                z = r*cos(v)
                ```
                Where:
                - r = {sphere_r} (radius)
                - u ∈ [0, 2π) (longitude)
                - v ∈ [0, π] (latitude)
                
                **Key Properties:**
                - Orientable surface
                - Surface area = 4πr²
                - Volume = (4/3)πr³
                - Euler characteristic: χ = 2
                """)
            elif graph_type == "Custom Parametric Surface":
                st.markdown(f"""
                ### Custom Parametric Surface
                
                **Equations:**
                ```
                x(u,v) = {x_expr}
                y(u,v) = {y_expr}
                z(u,v) = {z_expr}
                ```
                
                **Parameter Ranges:**
                - u ∈ [{u_min}, {u_max}]
                - v ∈ [{v_min}, {v_max}]
                """)
            elif graph_type == "Custom Explicit Surface z=f(x,y)":
                st.markdown(f"""
                ### Custom Explicit Surface
                
                **Equation:**
                ```
                z(x,y) = {z_expr}
                ```
                
                **Domain:**
                - x ∈ [{x_min}, {x_max}]
                - y ∈ [{y_min}, {y_max}]
                """)

# Add Usage Guide
with st.expander("Usage Guide"):
    st.markdown("""
    ## How to Use This Tool
    
    ### Interactive Controls
    
    - **Rotate**: Click and drag the graph with your mouse
    - **Zoom**: Use the mouse wheel or pinch gesture
    - **Pan**: Hold Shift while clicking and dragging
    - **Reset View**: Double-click anywhere on the graph
    
    ### Basic Controls
    
    1. **Select a Graph Type**: Choose from predefined mathematical surfaces or create your own
    2. **Adjust Resolution**: Higher values create smoother surfaces but may slow down rendering
    3. **Visualization Options**: Customize colors, transparency, and viewing angles
    4. **Click "Generate Graph"**: Apply your changes to render the graph
    
    ### Working with Custom Surfaces
    
    #### For Parametric Surfaces:
    - Define x, y, and z as functions of parameters u and v
    - Set the domain for u and v
    - Use standard mathematical notation (sin, cos, exp, etc.)
    
    #### For Explicit Surfaces:
    - Define z as a function of x and y
    - Set the domain for x and y
    
    ### Mathematical Functions Available
    
    - Trigonometric: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
    - Hyperbolic: `sinh`, `cosh`, `tanh`
    - Exponential/Logarithmic: `exp`, `log`, `sqrt`
    - Constants: `pi`, `e`
    
    ### Tips for Better Visualization
    
    - Use appropriate parameter ranges for your function
    - Adjust transparency for complex surfaces
    - Try different color maps to highlight different features
    - Surface + Wireframe style often provides the best visual understanding
    """)

