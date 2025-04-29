import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# Title
st.title('Comparative Visualization of  Heat Sources for Constant and Linear Growth of Beam Radius')

# Define an expanded list of colormaps
cmaps = [
    'aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance', 'blackbody', 'bluered', 
    'blues', 'blugrn', 'bluyl', 'brbg', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 
    'cividis', 'curl', 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric', 
    'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys', 'haline', 'hot', 'hsv', 
    'ice', 'icefire', 'inferno', 'jet', 'magenta', 'magma', 'matter', 'mint', 'mrybm', 
    'mygbm', 'oranges', 'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl', 
    'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'puor', 'purp', 'purples', 'purpor', 
    'rainbow', 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'reds', 'solar', 'spectral', 'speed', 
    'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose', 'tempo', 'temps', 'thermal', 
    'tropic', 'turbid', 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd'
]

# Sidebar parameters
st.sidebar.header('Parameters')
A = st.sidebar.slider('A', min_value=0.00001, max_value=5.0, value=2.0, step=0.0001)
P = st.sidebar.slider('P (Power, W)', min_value=1, max_value=5000, value=100, step=1)
k = st.sidebar.slider('k', min_value=0.1, max_value=10.0, value=1.0, step=0.1)
eta = st.sidebar.slider('η (Efficiency)', min_value=0.0, max_value=1.0, value=0.8, step=0.01)
r_0_surface = st.sidebar.slider('r₀ (Surface Beam Radius, μm)', min_value=50.0, max_value=500.0, value=25.0, step=0.01)
# Replace theta with m (radius growth rate)
m = st.sidebar.slider('m (Radius Growth Rate, μm/μm)', min_value=0.0, max_value=1.0, value=0.087, step=0.001)
C = st.sidebar.slider('C', min_value=0.1, max_value=4.0, value=2.0, step=0.1)
z_max = st.sidebar.slider('Maximum Depth (z, μm)', min_value=50.0, max_value=1000.0, value=100.0, step=1.0)
#z_depth = st.sidebar.slider('Depth for Linear Radius Plot (z, μm)', min_value=0.0, max_value=z_max, value=0.0, step=1.0)
#z_depth = st.sidebar.slider('Depth for Linear Radius Plot (z, μm)', min_value=0.0, max_value=z_max, value=z_max/2, step=1.0)
z_depth = st.slider('Depth for Linear Radius Plot (z, μm)', min_value=0.0, max_value=z_max, value=20.0, step=1.0)


# Colormap selection using selectbox with expanded options
colormap_name = st.sidebar.selectbox('Colormap', cmaps, index=cmaps.index('rainbow'))

# Function to calculate 2D intensity distribution for a given r_0
def super_gaussian_intensity(A, P, k, eta, r_0, C, x_values, y_values):
    x, y = np.meshgrid(x_values, y_values)
    r = np.sqrt(x ** 2 + y ** 2)
    F = 1.0
    intensity = F * ((A ** (1 / k) * k * P * eta) / (np.pi * r_0 ** 2 * math.gamma(1 / k))) * np.exp(-C * (r ** 2 / r_0 ** 2) ** k)
    return intensity

# Function to calculate peak intensity at r=0 for a given r_0
def peak_intensity(A, P, k, eta, r_0):
    F = 1.0
    intensity_peak = F * ((A ** (1 / k) * k * P * eta) / (np.pi * r_0 ** 2 * math.gamma(1 / k)))
    return intensity_peak

# Generate x and y values for 2D plot
x_values = np.linspace(-50, 50, 100)
y_values = np.linspace(-50, 50, 100)

# Calculate intensity distribution at z=0 (constant radius model and linear growth at z=0)
intensity_at_z0 = super_gaussian_intensity(A, P, k, eta, r_0_surface, C, x_values, y_values)

# Calculate intensity distribution for linear radius model at selected z_depth using m
r_0_at_z = r_0_surface + z_depth * m
intensity_linear_at_z = super_gaussian_intensity(A, P, k, eta, r_0_at_z, C, x_values, y_values)

# Find the global maximum intensity (at z=0)
globalmax_intensity = np.max(intensity_at_z0)

# Display peak intensity at z=0
st.sidebar.subheader('Peak Intensity at z=0')
st.sidebar.write(f'Peak intensity at z=0: {globalmax_intensity:.2e} W/μm²')

# Create 3D surface plot for constant radius model at z=0
fig_constant = go.Figure(data=[go.Surface(z=intensity_at_z0, x=x_values, y=y_values, colorscale=colormap_name, cmin=0, cmax=globalmax_intensity)])
fig_constant.update_layout(
    scene=dict(
        xaxis_title='X (μm)',
        yaxis_title='Y (μm)',
        zaxis_title='Intensity (W/μm²)',
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20)),
        zaxis=dict(title_font=dict(size=20), range=[0, globalmax_intensity]),
    ),
    title=dict(text=f"Constant Radius Intensity at z=0, P = {P} W", font=dict(size=30), automargin=True, yref='paper'),
    width=800,
    height=600
)
fig_constant.update_coloraxes(colorbar=dict(exponentformat='none', thickness=20, tickfont=dict(size=15)))

# Create 3D surface plot for linear radius model at selected z_depth
fig_linear = go.Figure(data=[go.Surface(z=intensity_linear_at_z, x=x_values, y=y_values, colorscale=colormap_name, cmin=0, cmax=globalmax_intensity)])
fig_linear.update_layout(
    scene=dict(
        xaxis_title='X (μm)',
        yaxis_title='Y (μm)',
        zaxis_title='Intensity (W/μm²)',
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20)),
        zaxis=dict(title_font=dict(size=20), range=[0, globalmax_intensity]),
    ),
    title=dict(text=f"Linear Radius Growth Intensity at z={z_depth} μm, P = {P} W", font=dict(size=30), automargin=True, yref='paper'),
    width=800,
    height=600
)
fig_linear.update_coloraxes(colorbar=dict(exponentformat='none', thickness=20, tickfont=dict(size=15)))

# Generate z values for line plot
z_values = np.linspace(0, z_max, 100)

# Calculate peak intensity along z for constant radius model (constant)
intensity_r0_constant = peak_intensity(A, P, k, eta, r_0_surface)

# Calculate peak intensity along z for linear radius model using m
r_0_z = r_0_surface + z_values * m
intensity_r0_linear = peak_intensity(A, P, k, eta, r_0_z)

# Create ENHANCED line plot for peak intensity vs. z
fig_line = go.Figure()

# Add traces with custom styling
fig_line.add_trace(go.Scatter(
    x=z_values,
    y=[intensity_r0_constant] * len(z_values),
    mode='lines',
    name='Constant Radius',
    line=dict(color='#FF4B4B', width=3, dash='dot'),
    hoverinfo='skip'
))

fig_line.add_trace(go.Scatter(
    x=z_values,
    y=intensity_r0_linear,
    mode='lines',
    name='Linear Radius Growth',
    line=dict(color='#0068C9', width=3),
    hoverinfo='skip'
))

# Add highlighted point at current z_depth
current_intensity = peak_intensity(A, P, k, eta, r_0_surface + z_depth * m)
fig_line.add_trace(go.Scatter(
    x=[z_depth],
    y=[current_intensity],
    mode='markers+text',
    marker=dict(color='#FFD700', size=12, line=dict(width=2, color='DarkSlateGrey')),
    text=[f'z = {z_depth} μm<br>Intensity = {current_intensity:.2e} W/μm²'],
    textposition='top right',
    name='Current Depth',
    hoverinfo='text'
))

# Add vertical line at current z_depth
fig_line.add_vline(
    x=z_depth,
    line=dict(color='#30A46C', width=2, dash='dash'),
    annotation_text="Selected Depth",
    annotation_position="top right"
)

# Update layout for better visual appeal
fig_line.update_layout(
    title=dict(
        text=f'<b>Peak Intensity vs. Depth from the Surface </b>',
        font=dict(size=24, family="Arial", color='#1F1F1F')
    ),
    xaxis=dict(
        title='<b>Depth (z, μm)</b>',
        tickfont=dict(size=18),
        gridcolor='#EAEAEA',
        linecolor='#B0B0B0',
        showgrid=True
    ),
    yaxis=dict(
        title='<b>Intensity (W/μm²)</b>',
        tickfont=dict(size=18),
        gridcolor='#EAEAEA',
        linecolor='#B0B0B0',
        showgrid=True,
        range=[0, globalmax_intensity * 1.1]  # Add 10% padding
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=14)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=60, b=20),
    height=500
)

# Display plots in Streamlit
st.write("### 3D Surface Plots")
st.write("The 3D surface plots below show the intensity distribution for the constant radius model at \( z = 0 \) and the linear radius growth model at a selectable depth \( z \). At \( z = 0 \), both models are identical, but as \( z \) increases, the linear growth model's intensity spreads due to the increasing beam radius.")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_constant, use_container_width=True)
with col2:
    st.plotly_chart(fig_linear, use_container_width=True)

st.write("### Peak Intensity vs. Depth")
st.write("The line plot below compares how the peak intensity (at \( r = 0 \)) changes with depth \( z \). The constant radius model shows no variation, while the linear radius growth model shows a decrease due to beam spreading.")
st.plotly_chart(fig_line, use_container_width=True)
