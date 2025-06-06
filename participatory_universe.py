"""
This script visualizes the participatory universe by showing how each particle's potential states collapse upon observation into a single realized state. Use the toggle to switch between Superposition Mode and Collapsed Mode.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.cm as cm


def generate_particle_data(N, M, seed=None):
    """Generate random particle positions and probability distributions."""
    if seed is not None:
        np.random.seed(seed)
    x_positions = np.random.rand(N)
    y_positions = np.random.rand(N)
    z_states = np.linspace(0, 1, M)
    probabilities = np.random.rand(N, M)
    probabilities /= probabilities.sum(axis=1, keepdims=True)
    return x_positions, y_positions, z_states, probabilities


def collapse_states(probabilities, z_states):
    """Select a collapsed z-state for each particle based on its probability distribution."""
    N = probabilities.shape[0]
    collapsed = np.array([
        np.random.choice(z_states, p=probabilities[i])
        for i in range(N)
    ])
    return collapsed


def probability_to_rgba(p, cmap='viridis', alpha_scale=2.5, alpha_min=0.1, alpha_max=0.8):
    """Map a probability value to an RGBA color string using the specified colormap."""
    colormap = cm.get_cmap(cmap)
    r, g, b, _ = colormap(p)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    alpha = float(np.clip(p * alpha_scale, alpha_min, alpha_max))
    return f"rgba({r}, {g}, {b}, {alpha})"


# Configuration
N = 50
M = 10
SEED = 42

# Generate particle data
x_positions, y_positions, z_states, probabilities = generate_particle_data(N, M, seed=SEED)

# ------------------------- Superposition Mode ----------------------------
super_x = []
super_y = []
super_z = []
super_colors = []

for i in range(N):
    for j in range(M):
        super_x.append(x_positions[i])
        super_y.append(y_positions[i])
        super_z.append(z_states[j])
        p = probabilities[i, j]
        super_colors.append(probability_to_rgba(p))

super_trace = go.Scatter3d(
    x=super_x,
    y=super_y,
    z=super_z,
    mode='markers',
    marker=dict(
        size=4,
        color=super_colors,
        opacity=1.0,
        line=dict(width=0.2, color='black')
    ),
    hoverinfo='none',
    name='Superposition'
)

# --------------------------- Collapsed Mode ------------------------------
collapsed_z = collapse_states(probabilities, z_states)
collapse_trace = go.Scatter3d(
    x=x_positions,
    y=y_positions,
    z=collapsed_z,
    mode='markers',
    marker=dict(
        size=6,
        color=collapsed_z,
        colorscale='Viridis',
        opacity=1.0,
        line=dict(width=0.5, color='black')
    ),
    hoverinfo='none',
    name='Collapsed Realities'
)
collapse_trace.visible = False

# ----------------------------- Figure ------------------------------------
fig = go.Figure(data=[super_trace, collapse_trace])

fig.update_layout(
    title='Superposition Field (All Potential States)',
    paper_bgcolor='rgba(0,0,0,1)',
    plot_bgcolor='rgba(0,0,0,1)',
    updatemenus=[
        dict(
            type='buttons',
            showactive=True,
            x=0.02,
            y=0.98,
            xanchor='left',
            yanchor='top',
            buttons=[
                dict(
                    method='update',
                    label='Superposition',
                    args=[{'visible': [True, False]},
                          {'title.text': 'Superposition Field (All Potential States)'}]
                ),
                dict(
                    method='update',
                    label='Collapsed',
                    args=[{'visible': [False, True]},
                          {'title.text': 'Collapsed Reality (Observed States)'}]
                )
            ]
        )
    ]
)

fig.update_scenes(
    xaxis=dict(
        title='X',
        showticklabels=False,
        showgrid=True,
        gridcolor='gray',
        zeroline=False,
        backgroundcolor='rgba(20,20,20,1)'
    ),
    yaxis=dict(
        title='Y',
        showticklabels=False,
        showgrid=True,
        gridcolor='gray',
        zeroline=False,
        backgroundcolor='rgba(20,20,20,1)'
    ),
    zaxis=dict(
        title='Potential Z-Levels',
        showticklabels=False,
        showgrid=True,
        gridcolor='gray',
        zeroline=False,
        backgroundcolor='rgba(20,20,20,1)'
    ),
    camera=dict(
        eye=dict(x=1.5, y=1.5, z=1.2),
        center=dict(x=0, y=0, z=0)
    )
)

if __name__ == "__main__":
    fig.show()
