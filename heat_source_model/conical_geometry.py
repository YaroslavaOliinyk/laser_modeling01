import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# Title
st.title('3D Visualization of Conical Heat Source Model')

# Sidebar parameters
st.sidebar.header('Parameters')
A = st.sidebar.slider('A', min_value=0.00001, max_value=5.0, value=2.0, step=0.0001)
P = st.sidebar.slider('P (Power, W)', min_value=1, max_value=5000, value=250, step=1)
k = st.sidebar.slider('k', min_value=0.1, max_value=10.0, value=1.0, step=0.1)
eta = st.sidebar.slider('η (Efficiency)', min_value=0.0, max_value=1.0, value=1.0, step=0.01)
r_0_surface = st.sidebar.slider('r₀ (Surface Beam Radius, μm)', min_value=20.0, max_value=500.0, value=25.0, step=0.01)
theta = st.sidebar.slider('θ (Cone Half-Angle, degrees)', min_value=0.1, max_value=45.0, value=5.0, step=0.1)
C = st.sidebar.slider('C', min_value=0.1, max_value=4.0, value=2.0, step=0.1)
colormap = st.sidebar.selectbox('Colormap', ['rainbow', 'jet', 'hsv', 'turbo'], index=0)
z_max = st.sidebar.slider('Maximum Depth (z, μm)', min_value=50.0, max_value=1000.0, value=100.0, step=1.0)

# Function to calculate 2D intensity distribution (exponential decay)
def conical_intensity(A, P, k, eta, r_0, C, x_values, y_values):
    x, y = np.meshgrid(x_values, y_values)
    r = np.sqrt(x ** 2 + y ** 2)
    r_max = r_0  # Maximum radius at the current depth
    intensity = np.zeros_like(r)
    mask = r <= r_max  # Only calculate intensity within the cone
    intensity[mask] = (P * eta / (np.pi * r_max ** 2)) * np.exp(-C * (r[mask] / r_max))
    return intensity

# Generate x and y values for 2D plot
x_values = np.linspace(-50, 50, 100)
y_values = np.linspace(-50, 50, 100)

# Calculate intensity at z=0 for consistent color scaling
intensity_at_z0 = conical_intensity(A, P, k, eta, r_0_surface, C, x_values, y_values)
globalmax_intensity = np.max(intensity_at_z0)

# Interactive 3D Surface Plot at Selected z
st.write("### 3D Surface Plot at Selected Depth")
z_selected = st.slider('Select z-depth (μm)', min_value=0.0, max_value=z_max, value=z_max/2, step=1.0)

# Compute r(z) at selected z
r_0_at_z = r_0_surface + z_selected * np.tan(np.deg2rad(theta))  

intensity_at_z = conical_intensity(A, P, k, eta, r_0_at_z, C, x_values, y_values)

# Create 3D surface plot
fig = go.Figure(data=[go.Surface(z=intensity_at_z, x=x_values, y=y_values, colorscale=colormap, cmin=0, cmax=globalmax_intensity)])
fig.update_layout(
    scene=dict(
        xaxis_title='X (μm)',
        yaxis_title='Y (μm)',
        zaxis_title='Intensity (W/μm²)',
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20)),
        zaxis=dict(title_font=dict(size=20), range=[0, globalmax_intensity]),
    ),
    title=f'Conical Heat Source at z={z_selected} μm',
    width=800,
    height=600
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)
