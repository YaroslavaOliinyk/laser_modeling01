import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Title
st.title('3D Visualization of Conical Heat Source Model')

# Sidebar parameters
st.sidebar.header('Parameters')
r_0_surface = st.sidebar.slider('r₀ (Surface Beam Radius, μm)', min_value=20.0, max_value=500.0, value=25.0, step=0.01)
theta = st.sidebar.slider('θ (Cone Half-Angle, degrees)', min_value=0.1, max_value=45.0, value=5.0, step=0.1)
colormap = st.sidebar.selectbox('Colormap', ['rainbow', 'jet', 'hsv', 'turbo'], index=0)
z_max = st.sidebar.slider('Maximum Depth (z, μm)', min_value=50.0, max_value=1000.0, value=100.0, step=1.0)

# Function to calculate 2D intensity distribution for conical profile
def conical_intensity(I0, r_0, x_values, y_values):
    x, y = np.meshgrid(x_values, y_values)
    r = np.sqrt(x ** 2 + y ** 2)
    intensity = np.where(r <= r_0, I0 * (1 - r / r_0), 0)
    return intensity

# Generate x and y values for 2D plot
x_values = np.linspace(-50, 50, 100)
y_values = np.linspace(-50, 50, 100)

# Calculate intensity at z=0 for consistent color scaling
I0 = 1.0  # Peak intensity (you can make this adjustable via a slider if needed)
intensity_at_z0 = conical_intensity(I0, r_0_surface, x_values, y_values)
globalmax_intensity = np.max(intensity_at_z0)

# Interactive 3D Surface Plot at Selected Depth
st.write("### 3D Surface Plot at Selected Depth")
z_selected = st.slider('Select z-depth (μm)', min_value=0.0, max_value=z_max, value=z_max / 2, step=1.0)

# Compute r(z) at selected z
r_0_at_z = r_0_surface + z_selected * np.tan(np.deg2rad(theta))
intensity_at_z = conical_intensity(I0, r_0_at_z, x_values, y_values)

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
