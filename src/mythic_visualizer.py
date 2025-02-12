import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from visualizer import apply_common_theme

def create_scaling_line_chart(df: pd.DataFrame, title: str, animate: bool = False, show_notes: bool = False) -> go.Figure:
    """Create a line chart showing scaling values across key levels."""
    fig = go.Figure()
    
    # Add Season 1 line (using Season 1 w/ Guile if available)
    s1_col = 'Season 1 w/ Guile' if 'Season 1 w/ Guile' in df.columns else 'Season 1'
    
    # Prepare hover text with notes
    hover_text = []
    for i, row in df.iterrows():
        if show_notes:
            note = row.get('Notes', '')  # Note: 'Notes' for higher baseline files
            if pd.isna(note):
                note = ''
            hover_text.append(f"Key Level: {row['Mythic']}<br>" +
                            f"Season 1: {row[s1_col]}<br>" +
                            f"Season 2: {row['Season 2']}" +
                            (f"<br>Note: {note}" if note else ""))
        else:
            hover_text.append(f"Key Level: {row['Mythic']}<br>" +
                            f"Season 1: {row[s1_col]}<br>" +
                            f"Season 2: {row['Season 2']}")
    
    if not animate:
        fig.add_trace(go.Scatter(
            x=df['Mythic'],
            y=df[s1_col],
            name='Season 1',
            line=dict(color='#69CCF0', width=3),  # Light blue
            mode='lines+markers',
            hovertemplate='%{text}<extra></extra>',
            text=hover_text
        ))
        
        # Add Season 2 line
        fig.add_trace(go.Scatter(
            x=df['Mythic'],
            y=df['Season 2'],
            name='Season 2',
            line=dict(color='#FF7D0A', width=3),  # Orange
            mode='lines+markers',
            hovertemplate='%{text}<extra></extra>',
            text=hover_text
        ))
        
        # Add annotations for non-empty notes only if show_notes is True
        if show_notes:
            annotations = []
            for i, row in df.iterrows():
                note = row.get('Notes', '')  # Note: 'Notes' for higher baseline files
                if pd.notna(note) and note.strip():
                    annotations.append(dict(
                        x=row['Mythic'],
                        y=max(float(str(row[s1_col]).rstrip('%')), float(str(row['Season 2']).rstrip('%'))),
                        text='📝',  # Note emoji
                        showarrow=False,
                        yshift=10,
                        hovertext=note,
                        hoverlabel=dict(bgcolor='rgba(0,0,0,0.8)')
                    ))
            fig.update_layout(annotations=annotations)
    else:
        # Create frames for animation
        frames = []
        for i in range(len(df)):
            frame_data = df.iloc[:i+1]
            frame_hover = hover_text[:i+1]
            
            frame = go.Frame(
                data=[
                    go.Scatter(
                        x=frame_data['Mythic'],
                        y=frame_data[s1_col],
                        name='Season 1',
                        line=dict(color='#69CCF0', width=3),
                        mode='lines+markers',
                        hovertemplate='%{text}<extra></extra>',
                        text=frame_hover
                    ),
                    go.Scatter(
                        x=frame_data['Mythic'],
                        y=frame_data['Season 2'],
                        name='Season 2',
                        line=dict(color='#FF7D0A', width=3),
                        mode='lines+markers',
                        hovertemplate='%{text}<extra></extra>',
                        text=frame_hover
                    )
                ],
                name=str(i)
            )
            frames.append(frame)
        
        # Add initial empty traces with full data range
        fig.add_trace(go.Scatter(
            x=df['Mythic'],
            y=[None] * len(df),
            name='Season 1',
            line=dict(color='#69CCF0', width=3),
            mode='lines+markers',
            showlegend=True,
            hovertemplate='%{text}<extra></extra>',
            text=hover_text
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Mythic'],
            y=[None] * len(df),
            name='Season 2',
            line=dict(color='#FF7D0A', width=3),
            mode='lines+markers',
            showlegend=True,
            hovertemplate='%{text}<extra></extra>',
            text=hover_text
        ))
        
        # Add frames to figure
        fig.frames = frames
        
        # Add animation buttons
        fig.update_layout(
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True},
                                      "fromcurrent": True,
                                      "transition": {"duration": 300}}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }],
            sliders=[{
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 16},
                    "prefix": "Key Level: ",
                    "visible": True,
                    "xanchor": "right"
                },
                "transition": {"duration": 300, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[str(i)], {"frame": {"duration": 300, "redraw": True},
                                          "mode": "immediate",
                                          "transition": {"duration": 300}}],
                        "label": str(df['Mythic'].iloc[i]),
                        "method": "animate"
                    } for i in range(len(df))
                ]
            }]
        )
    
    fig.update_layout(
        title=title,
        xaxis=dict(
            title='Key Level',
            type='category',  # Treat x-axis as categories
            autorange=True,
            fixedrange=True  # Prevent zooming on x-axis
        ),
        yaxis=dict(
            title='Scaling Value (%)',
            autorange=True,
            fixedrange=True  # Prevent zooming on y-axis
        ),
        height=500,
        hovermode='x unified'
    )
    
    return apply_common_theme(fig)

def create_scaling_percentage_chart(df: pd.DataFrame, animate: bool = False) -> go.Figure:
    """Create a line chart showing scaling percentages between seasons."""
    # Calculate percentage difference
    s1_col = 'Season 1 w/ Guile' if 'Season 1 w/ Guile' in df.columns else 'Season 1'
    s1_values = df[s1_col]
    s2_values = df['Season 2']
    percentage_diff = ((s2_values - s1_values) / s1_values) * 100
    
    fig = go.Figure()
    
    if not animate:
        # Add percentage difference line
        fig.add_trace(go.Scatter(
            x=df['Mythic'],
            y=percentage_diff,
            name='Percentage Difference',
            line=dict(color='#ABD473', width=3),  # Green
            mode='lines+markers',
            hovertemplate='Key Level: %{x}<br>Difference: %{y:.1f}%<extra></extra>'
        ))
    else:
        # Create frames for animation
        frames = []
        for i in range(len(df)):
            frame_data = percentage_diff.iloc[:i+1]
            frame_x = df['Mythic'].iloc[:i+1]
            
            frame = go.Frame(
                data=[go.Scatter(
                    x=frame_x,
                    y=frame_data,
                    name='Percentage Difference',
                    line=dict(color='#ABD473', width=3),
                    mode='lines+markers',
                    hovertemplate='Key Level: %{x}<br>Difference: %{y:.1f}%<extra></extra>'
                )],
                name=str(i)
            )
            frames.append(frame)
        
        # Add initial empty trace with full data range
        fig.add_trace(go.Scatter(
            x=df['Mythic'],
            y=[None] * len(df),
            name='Percentage Difference',
            line=dict(color='#ABD473', width=3),
            mode='lines+markers',
            hovertemplate='Key Level: %{x}<br>Difference: %{y:.1f}%<extra></extra>'
        ))
        
        # Add frames to figure
        fig.frames = frames
        
        # Add animation buttons
        fig.update_layout(
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True},
                                      "fromcurrent": True,
                                      "transition": {"duration": 300}}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }],
            sliders=[{
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 16},
                    "prefix": "Key Level: ",
                    "visible": True,
                    "xanchor": "right"
                },
                "transition": {"duration": 300, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[str(i)], {"frame": {"duration": 300, "redraw": True},
                                          "mode": "immediate",
                                          "transition": {"duration": 300}}],
                        "label": str(df['Mythic'].iloc[i]),
                        "method": "animate"
                    } for i in range(len(df))
                ]
            }]
        )
    
    fig.update_layout(
        title='Percentage Difference in Scaling Between Seasons',
        xaxis=dict(
            title='Key Level',
            type='category',  # Treat x-axis as categories
            autorange=True,
            fixedrange=True  # Prevent zooming on x-axis
        ),
        yaxis=dict(
            title='Percentage Difference (%)',
            autorange=True,
            fixedrange=True  # Prevent zooming on y-axis
        ),
        height=500,
        showlegend=False
    )
    
    # Add a zero line for reference
    fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.3)
    
    return apply_common_theme(fig)

def create_scaling_comparison_chart(df: pd.DataFrame, animate: bool = False) -> go.Figure:
    """Create a bar chart comparing Season 1 and Season 2 scaling."""
    fig = go.Figure()
    
    s1_col = 'Season 1 w/ Guile' if 'Season 1 w/ Guile' in df.columns else 'Season 1'
    
    if not animate:
        # Add bars for each season
        fig.add_trace(go.Bar(
            x=df['Mythic'],
            y=df[s1_col],
            name='Season 1',
            marker_color='#69CCF0'  # Light blue
        ))
        
        fig.add_trace(go.Bar(
            x=df['Mythic'],
            y=df['Season 2'],
            name='Season 2',
            marker_color='#FF7D0A'  # Orange
        ))
    else:
        # Create frames for animation
        frames = []
        for i in range(len(df)):
            frame_data = df.iloc[:i+1]
            
            frame = go.Frame(
                data=[
                    go.Bar(
                        x=frame_data['Mythic'],
                        y=frame_data[s1_col],
                        name='Season 1',
                        marker_color='#69CCF0'
                    ),
                    go.Bar(
                        x=frame_data['Mythic'],
                        y=frame_data['Season 2'],
                        name='Season 2',
                        marker_color='#FF7D0A'
                    )
                ],
                name=str(i)
            )
            frames.append(frame)
        
        # Add initial empty traces with full data range
        fig.add_trace(go.Bar(
            x=df['Mythic'],
            y=[None] * len(df),
            name='Season 1',
            marker_color='#69CCF0'
        ))
        
        fig.add_trace(go.Bar(
            x=df['Mythic'],
            y=[None] * len(df),
            name='Season 2',
            marker_color='#FF7D0A'
        ))
        
        # Add frames to figure
        fig.frames = frames
        
        # Add animation buttons
        fig.update_layout(
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True},
                                      "fromcurrent": True,
                                      "transition": {"duration": 300}}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }],
            sliders=[{
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 16},
                    "prefix": "Key Level: ",
                    "visible": True,
                    "xanchor": "right"
                },
                "transition": {"duration": 300, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[str(i)], {"frame": {"duration": 300, "redraw": True},
                                          "mode": "immediate",
                                          "transition": {"duration": 300}}],
                        "label": str(df['Mythic'].iloc[i]),
                        "method": "animate"
                    } for i in range(len(df))
                ]
            }]
        )
    
    fig.update_layout(
        title='Season 1 vs Season 2 Scaling Comparison',
        xaxis=dict(
            title='Key Level',
            type='category',  # Treat x-axis as categories
            autorange=True,
            fixedrange=True  # Prevent zooming on x-axis
        ),
        yaxis=dict(
            title='Scaling Value (%)',
            autorange=True,
            fixedrange=True  # Prevent zooming on y-axis
        ),
        height=500,
        barmode='group'
    )
    
    return apply_common_theme(fig) 