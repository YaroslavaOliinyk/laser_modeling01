import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# Title
st.title('3D Visualization of Conical Heat Source Model')

# Sidebar parameters
st.sidebar.header('Parameters')
P = st.sidebar.slider('P (Power, W)', min_value=1, max_value=5000, value=250, step=1)
eta = st.sidebar.slider('η (Efficiency)', min_value=0.0, max_value=1.0, value=1.0, step=0.01)
z_max = st.sidebar.slider('Maximum Depth (z, μm)', min_value=50.0, max_value=1000.0, value=100.0, step=1.0)
ze = st.sidebar.slider('zₑ (Top of Heat Cone, μm)', min_value=0.0, max_value=z_max, value=10.0, step=1.0)
zi = st.sidebar.slider('zᵢ (Bottom of Heat Cone, μm)', min_value=0.0, max_value=z_max, value=100.0, step=1.0)
re = st.sidebar.slider('rₑ (Top Radius, μm)', min_value=1.0, max_value=200.0, value=25.0, step=0.1)
ri = st.sidebar.slider('rᵢ (Bottom Radius, μm)', min_value=1.0, max_value=200.0, value=100.0, step=0.1)
colormap = st.sidebar.selectbox('Colormap', ['rainbow', 'jet', 'hsv', 'turbo'], index=0)


# Function to calculate 2D intensity distribution
def conical_intensity(P, eta, re, ri, ze, zi, x_values, y_values, z):
    x, y = np.meshgrid(x_values, y_values)
    r = np.sqrt(x ** 2 + y ** 2)
    e = math.e

# Compute r0 as a function of z
    r0_z = re + ((ri - re) / (zi - ze)) * (z - ze)

# Avoid division by zero or negative radius
    if r0_z <= 0 or zi == ze:
        return np.zeros_like(r)

# Heat distribution Qv(r, z)
    Qv = (9 * P * eta * e ** 3) / (np.pi * (e ** 3 - 1) * (ze - zi) * (re ** 2))
    intensity = Qv * np.exp(-3 * (r ** 2) / (r0_z ** 2))
    return intensity

# Generate x and y values for 2D plot
x_values = np.linspace(-50, 50, 100)
y_values = np.linspace(-50, 50, 100)

# Calculate intensity at z=0 for consistent color scaling
intensity_at_z0 = conical_intensity(P, eta, re, ri, ze, zi, x_values, y_values, 0.0)
globalmax_intensity = np.max(intensity_at_z0)

# Interactive 3D Surface Plot at Selected z
st.write("### 3D Surface Plot at Selected Depth")
z_selected = st.slider('Select z-depth (μm)', min_value=0.0, max_value=z_max, value=z_max/2, step=1.0)

# Compute r(z) at selected z
intensity_at_z = conical_intensity(P, eta, re, ri, ze, zi, x_values, y_values, z_selected)
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
