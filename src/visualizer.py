import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict

# Official World of Warcraft class colors
WOW_CLASS_COLORS = {
    'Death Knight': '#C41F3B',  # Red
    'Demon Hunter': '#A330C9',  # Purple
    'Druid': '#FF7D0A',        # Orange
    'Evoker': '#33937F',       # Teal
    'Hunter': '#ABD473',       # Green
    'Mage': '#69CCF0',         # Light Blue
    'Monk': '#00FF96',         # Jade Green
    'Paladin': '#F58CBA',      # Pink
    'Priest': '#FFFFFF',       # White
    'Rogue': '#FFF569',        # Yellow
    'Shaman': '#0070DE',       # Blue
    'Warlock': '#9482C9',      # Purple
    'Warrior': '#C79C6E'       # Brown
}

# Animation chart styles
ANIMATED_CHART_STYLE = {
    'bar': dict(
        width=0.8,  # Bar width
    ),
    'axis': dict(
        tickfont=dict(
            size=16,  # X-axis label size
            color='#E0E0E0'
        ),
        title_font=dict(
            size=18,  # Axis title size
            color='#FFFFFF'
        ),
        gridcolor='rgba(255,255,255,0.1)',
        title_standoff=15
    ),
    'title': dict(
        font=dict(
            size=24,  # Title size
            color='#FFFFFF'
        )
    ),
    'animation_controls': dict(
        bgcolor='rgba(0,0,0,0.5)',
        font=dict(
            color='white',
            size=14
        )
    )
}

# Common theme settings
CHART_THEME = {
    'font': dict(
        family="Segoe UI, Arial, sans-serif",
        size=12,
        color="#E0E0E0"
    ),
    'title': dict(
        font=dict(size=20, color="#FFFFFF", family="Segoe UI, Arial, sans-serif"),
        x=0.5,
        xanchor='center',
        y=0.95
    ),
    'plot_bgcolor': 'rgba(0,0,0,0.05)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'margin': dict(t=80, l=60, r=40, b=60)
}

def apply_common_theme(fig: go.Figure) -> go.Figure:
    """Apply common theme settings to a figure."""
    fig.update_layout(
        **CHART_THEME,
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#E0E0E0'),
            title_font=dict(color='#FFFFFF', size=14),
            title_standoff=15
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#E0E0E0'),
            title_font=dict(color='#FFFFFF', size=14),
            title_standoff=15
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0.3)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1,
            font=dict(color='#E0E0E0')
        )
    )
    return fig

def create_spec_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a stacked bar chart showing spec distribution within classes.
    
    Args:
        df (pd.DataFrame): Input DataFrame with class/spec data
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.bar(
        df,
        x='Class',
        y='Percentage',
        color='Class',
        title='Class and Specialization Distribution',
        labels={'Percentage': 'Share (%)', 'Class': 'Character Class'},
        hover_data=['Parses', 'Spec'],
        color_discrete_map=WOW_CLASS_COLORS
    )
    
    fig.update_traces(
        hovertemplate='<b>%{customdata[1]}</b><br>' +
                      'Class: %{x}<br>' +
                      'Share: %{y:.1f}%<br>' +
                      'Parses: %{customdata[0]:,}<extra></extra>'
    )
    
    fig.update_layout(
        barmode='stack',
        xaxis_title='Character Class',
        yaxis_title='Share (%)',
        showlegend=True,
        height=600
    )
    
    return apply_common_theme(fig)

def create_spec_treemap(df: pd.DataFrame) -> go.Figure:
    """
    Create a treemap visualization of class/spec distribution.
    
    Args:
        df (pd.DataFrame): Input DataFrame with class/spec data
        
    Returns:
        go.Figure: Plotly figure object
    """
    color_map = {**WOW_CLASS_COLORS, '(?)': '#1E1E1E'}
    
    fig = px.treemap(
        df,
        path=[px.Constant('All Classes'), 'Class', 'Spec'],
        values='Parses',
        title='Class and Specialization Distribution Hierarchy',
        color='Class',
        color_discrete_map=color_map
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(width=2, color='rgba(255, 255, 255, 0.2)')
        ),
        hovertemplate='<b>%{label}</b><br>' +
                      'Parses: %{value:,.0f}<br>' +
                      'Share: %{percentParent:.1%}<extra></extra>',
        textfont=dict(family="Segoe UI, Arial, sans-serif", size=13)
    )
    
    fig.update_layout(
        height=700,
        margin=dict(t=50, l=10, r=10, b=10)
    )
    
    return apply_common_theme(fig)

def create_trend_chart(trend_df: pd.DataFrame) -> go.Figure:
    """
    Create a line chart showing spec trends across raids.
    
    Args:
        trend_df (pd.DataFrame): Trend data DataFrame
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.line(
        trend_df,
        x='Raid',
        y='Percentage',
        color='Class',
        line_dash='Spec',
        title='Specialization Trends Across Raids',
        labels={'Percentage': 'Share (%)', 'Raid': 'Raid Instance'},
        color_discrete_map=WOW_CLASS_COLORS
    )
    
    fig.update_traces(
        line=dict(width=3),
        hovertemplate='<b>%{customdata}</b><br>' +
                      'Raid: %{x}<br>' +
                      'Share: %{y:.1f}%<extra></extra>',
        customdata=trend_df['Spec']
    )
    
    fig.update_layout(
        showlegend=True,
        height=800,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02
        ),
        xaxis_tickangle=-30
    )
    
    return apply_common_theme(fig)

def create_delta_chart(comparison_df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing changes between raids.
    
    Args:
        comparison_df (pd.DataFrame): Raid comparison DataFrame
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.bar(
        comparison_df,
        x='Spec',
        y='Percentage_Change',
        color='Class',
        title='Specialization Distribution Changes Between Raids',
        labels={'Percentage_Change': 'Change in Share (%)', 'Spec': 'Specialization'},
        color_discrete_map=WOW_CLASS_COLORS
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>' +
                      'Change: %{y:+.1f}%<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title='Specialization',
        yaxis_title='Change in Share (%)',
        showlegend=True,
        height=600,
        xaxis_tickangle=-45,
        yaxis=dict(
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.2)',
            zerolinewidth=2
        )
    )
    
    return apply_common_theme(fig)

def create_class_trend_chart(trend_df: pd.DataFrame) -> go.Figure:
    """
    Create a line chart showing class trends across raids.
    
    Args:
        trend_df (pd.DataFrame): Class trend data DataFrame
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.line(
        trend_df,
        x='Raid',
        y='Percentage',
        color='Class',
        title='Class Representation Trends Across Raids',
        labels={'Percentage': 'Share (%)', 'Raid': 'Raid Instance'},
        color_discrete_map=WOW_CLASS_COLORS
    )
    
    fig.update_traces(
        line=dict(width=3),
        hovertemplate='<b>%{customdata}</b><br>' +
                      'Raid: %{x}<br>' +
                      'Share: %{y:.1f}%<extra></extra>',
        customdata=trend_df['Class']
    )
    
    fig.update_layout(
        showlegend=True,
        height=600,
        xaxis_title='Raid Instance',
        yaxis_title='Class Share (%)',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02
        ),
        xaxis_tickangle=-30
    )
    
    return apply_common_theme(fig)

def create_class_change_chart(changes_df: pd.DataFrame, class_name: str) -> go.Figure:
    """
    Create a visualization of class percentage changes between raids.
    
    Args:
        changes_df (pd.DataFrame): DataFrame with class changes
        class_name (str): Name of the class being analyzed
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    # Add bars for percentage changes
    fig.add_trace(go.Bar(
        x=[f"{row['From Raid']} → {row['To Raid']}" for _, row in changes_df.iterrows()],
        y=changes_df['Change'],
        marker_color=WOW_CLASS_COLORS[class_name],
        name='Change',
        hovertemplate='<b>Change:</b> %{y:+.1f}%<extra></extra>'
    ))
    
    # Add line for absolute percentages
    fig.add_trace(go.Scatter(
        x=[f"{row['From Raid']} → {row['To Raid']}" for _, row in changes_df.iterrows()],
        y=changes_df['To Percentage'],
        name='Total Share',
        line=dict(color='white', width=3, dash='dot'),
        yaxis='y2',
        hovertemplate='<b>Total Share:</b> %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'{class_name} Representation Changes Between Raids',
        yaxis=dict(
            title='Change in Share (%)',
            side='left',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.2)',
            zerolinewidth=2
        ),
        yaxis2=dict(
            title='Total Share (%)',
            side='right',
            overlaying='y',
            showgrid=False,
            tickfont=dict(color='#E0E0E0'),
            title_font=dict(color='#FFFFFF')
        ),
        xaxis=dict(
            tickangle=-30,
            showticklabels=True
        ),
        showlegend=True,
        height=600,
        barmode='relative',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor='rgba(0,0,0,0.3)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        )
    )
    
    return apply_common_theme(fig)

def create_class_pie_chart(df: pd.DataFrame) -> go.Figure:
    """Create a pie chart showing class distribution."""
    # Aggregate by Class if not already aggregated
    if 'Spec' in df.columns:
        class_df = df.groupby('Class')['Parses'].sum().reset_index()
        class_df['Percentage'] = (class_df['Parses'] / class_df['Parses'].sum()) * 100
    else:
        class_df = df

    fig = go.Figure(data=[go.Pie(
        labels=class_df['Class'],
        values=class_df['Percentage'],
        hole=0.4,  # Creates a donut chart
        marker=dict(
            colors=[WOW_CLASS_COLORS[cls] for cls in class_df['Class']],
            line=dict(color='rgba(0, 0, 0, 0.8)', width=4)  # Thicker dark borders
        ),
        textinfo='label+percent',
        textfont=dict(color='white', size=14),
        hovertemplate='<b>%{label}</b><br>' +
                      'Share: %{value:.1f}%<extra></extra>',
        customdata=class_df['Parses']
    )])

    fig.update_layout(
        height=700,
        showlegend=True,
        legend=dict(
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        annotations=[
            dict(
                text='Class<br>Distribution',
                x=0.5,
                y=0.5,
                font=dict(size=16, color='white'),
                showarrow=False
            )
        ]
    )

    return apply_common_theme(fig)

def create_spec_pie_chart(df: pd.DataFrame, class_name: str = None) -> go.Figure:
    """
    Create a pie chart showing spec distribution, optionally filtered by class.
    
    Args:
        df (pd.DataFrame): Input DataFrame with spec data
        class_name (str, optional): If provided, show only specs for this class
    """
    if class_name:
        spec_df = df[df['Class'] == class_name].copy()
        title = f'{class_name} Specialization Distribution'
        center_text = f'{class_name}<br>Specs'
    else:
        spec_df = df.copy()
        title = 'All Specializations Distribution'
        center_text = 'Spec<br>Distribution'

    fig = go.Figure(data=[go.Pie(
        labels=spec_df['Spec'],
        values=spec_df['Percentage'],
        hole=0.4,  # Creates a donut chart
        marker=dict(
            colors=[WOW_CLASS_COLORS[spec_df['Class'].iloc[i]] 
                   for i in range(len(spec_df))],
            line=dict(color='rgba(0, 0, 0, 0.8)', width=4)  # Thicker dark borders
        ),
        textinfo='label+percent',
        textfont=dict(color='white', size=14),
        hovertemplate='<b>%{label}</b><br>' +
                      'Class: %{customdata[0]}<br>' +
                      'Share: %{value:.1f}%<extra></extra>',
        customdata=list(zip(spec_df['Class'], spec_df['Parses']))
    )])

    fig.update_layout(
        title=title,
        height=700,
        showlegend=True,
        legend=dict(
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        annotations=[
            dict(
                text=center_text,
                x=0.5,
                y=0.5,
                font=dict(size=16, color='white'),
                showarrow=False
            )
        ]
    )

    return apply_common_theme(fig)

def create_animated_trend_chart(trend_df: pd.DataFrame, animation_type: str = 'class', frame_duration: int = 1000, transition_duration: int = 500) -> go.Figure:
    """
    Create an animated bar chart showing changes over time.
    
    Args:
        trend_df (pd.DataFrame): Trend data DataFrame
        animation_type (str): Either 'class' or 'spec' to determine visualization type
        frame_duration (int): Duration of each frame in milliseconds
        transition_duration (int): Duration of transitions in milliseconds
        
    Returns:
        go.Figure: Plotly figure object with animation
    """
    # Make a copy of the DataFrame to avoid modifying the original
    trend_df = trend_df.copy()
    
    # Define raid order (from oldest to newest)
    RAID_ORDER = [
        'Uldir (8.1)',
        'Battle of Dazar\'alor',
        'Crucible of Storms',
        'Eternal Palace',
        'Nya\'lotha (Pre-Nerf)',
        'Sepulcher of the First Ones (9.2)',
        'Vault of the Incarnates',
        'Aberrus, The Shadowed Crucible',
        'Amirdrassil, the Dream\'s Hope',
        'Nerub-ar Palace'
    ]
    
    # Ensure all raid names in the DataFrame match the expected names
    unique_raids = trend_df['Raid'].unique()
    print(f"Unique raids in DataFrame: {unique_raids}")  # Debug print
    
    # Create a categorical type for raid names with the correct order
    trend_df['Raid'] = pd.Categorical(trend_df['Raid'], categories=RAID_ORDER, ordered=True)
    
    # Sort by raid to ensure correct animation sequence
    trend_df = trend_df.sort_values('Raid')
    
    # Create figure
    fig = go.Figure()
    
    # Get initial data for the first raid that exists in the DataFrame
    available_raids = [raid for raid in RAID_ORDER if raid in trend_df['Raid'].unique()]
    if not available_raids:
        print("No matching raids found in DataFrame")  # Debug print
        return fig
    
    first_raid = available_raids[0]
    initial_data = trend_df[trend_df['Raid'] == first_raid]
    
    if animation_type == 'class':
        # Add a bar for each class
        for class_name in sorted(trend_df['Class'].unique()):
            class_data = initial_data[initial_data['Class'] == class_name]
            percentage = class_data['Percentage'].iloc[0] if not class_data.empty else 0
            
            fig.add_trace(
                go.Bar(
                    x=[class_name],
                    y=[percentage],
                    name=class_name,
                    marker_color=WOW_CLASS_COLORS[class_name],
                    width=ANIMATED_CHART_STYLE['bar']['width'],
                    hovertemplate='<b>%{x}</b><br>' +
                                'Share: %{y:.1f}%<extra></extra>'
                )
            )
    else:
        # Add a bar for each spec
        class_spec_pairs = [(class_name, spec) 
                           for class_name in sorted(trend_df['Class'].unique())
                           for spec in sorted(trend_df[trend_df['Class'] == class_name]['Spec'].unique())]
        
        for class_name, spec in class_spec_pairs:
            spec_data = initial_data[(initial_data['Class'] == class_name) & 
                                   (initial_data['Spec'] == spec)]
            percentage = spec_data['Percentage'].iloc[0] if not spec_data.empty else 0
            
            x_pos = f"{spec}<br><span style='opacity:0'>{class_name}</span>"
            
            fig.add_trace(
                go.Bar(
                    x=[x_pos],
                    y=[percentage],
                    name=f"{spec} ({class_name})",
                    marker_color=WOW_CLASS_COLORS[class_name],
                    width=ANIMATED_CHART_STYLE['bar']['width'],
                    hovertemplate='<b>%{x}</b><br>' +
                                'Class: ' + class_name + '<br>' +
                                'Share: %{y:.1f}%<extra></extra>'
                )
            )
    
    # Create frames for animation
    frames = []
    for raid in available_raids:
        frame_data = trend_df[trend_df['Raid'] == raid]
        print(f"Creating frame for raid: {raid}, data shape: {frame_data.shape}")  # Debug print
        
        frame = {
            "data": [], 
            "name": str(raid),
            "layout": {
                "annotations": [{
                    "text": f"Raid: {raid}",
                    "x": 0.5,
                    "y": 0.91,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 18, "color": "white"}
                }]
            }
        }
        
        if animation_type == 'class':
            for class_name in sorted(trend_df['Class'].unique()):
                class_data = frame_data[frame_data['Class'] == class_name]
                percentage = class_data['Percentage'].iloc[0] if not class_data.empty else 0
                
                frame["data"].append(
                    go.Bar(
                        x=[class_name],
                        y=[percentage],
                        marker_color=WOW_CLASS_COLORS[class_name]
                    )
                )
        else:
            # Create list of (class, spec) tuples for this frame
            class_spec_pairs = [(class_name, spec) 
                              for class_name in sorted(trend_df['Class'].unique())
                              for spec in sorted(trend_df[trend_df['Class'] == class_name]['Spec'].unique())]
            
            for class_name, spec in class_spec_pairs:
                spec_data = frame_data[(frame_data['Class'] == class_name) & 
                                     (frame_data['Spec'] == spec)]
                percentage = spec_data['Percentage'].iloc[0] if not spec_data.empty else 0
                
                # Use the same unique x-axis position with hidden class identifier
                x_pos = f"{spec}<br><span style='opacity:0'>{class_name}</span>"
                
                frame["data"].append(
                    go.Bar(
                        x=[x_pos],
                        y=[percentage],
                        marker_color=WOW_CLASS_COLORS[class_name],
                        width=ANIMATED_CHART_STYLE['bar']['width']
                    )
                )
        
        frames.append(frame)
    
    # Update layout with new styles
    title = 'Class Distribution by Raid' if animation_type == 'class' else 'Spec Distribution by Raid'
    
    fig.update_layout(
        title=dict(
            text=title,
            y=0.98,  # Move title up slightly
            **ANIMATED_CHART_STYLE['title']
        ),
        showlegend=False,
        height=600,
        margin=dict(t=120, l=60, r=40, b=100),  # Increase top and bottom margins
        xaxis=dict(
            title='',
            tickangle=-45 if animation_type == 'spec' else -30,
            showgrid=False,
            **ANIMATED_CHART_STYLE['axis']
        ),
        yaxis=dict(
            title='Share (%)',
            range=[0, max(trend_df['Percentage']) * 1.1],
            showgrid=True,
            **ANIMATED_CHART_STYLE['axis']
        ),
        annotations=[{
            "text": f"Raid: {first_raid}",
            "x": 0.5,
            "y": 0.91,  # Adjust position below title
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": {"size": 18, "color": "white"}
        }],
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": frame_duration, "redraw": True},
                                  "fromcurrent": True,
                                  "transition": {"duration": transition_duration, "easing": "cubic-in-out"}}],
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
            "active": -1,
            "type": "buttons",
            "x": 0.05,
            "xanchor": "right",
            "y": -0.15,  # Move buttons down
            "yanchor": "top",
            "bgcolor": "rgba(0,0,0,0.5)",
            "bordercolor": "rgba(255,255,255,0.2)",
            "font": {"color": "white", "size": 14}
        }],
        sliders=[{
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 18, "color": "white"},
                "prefix": "Raid: ",
                "visible": False,
                "xanchor": "right"
            },
            "transition": {"duration": transition_duration, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": -0.2,  # Move slider down
            "bgcolor": "rgba(0,0,0,0.5)",
            "bordercolor": "rgba(255,255,255,0.2)",
            "tickcolor": "white",
            "font": {"color": "white", "size": 14},
            "steps": [
                {
                    "args": [[raid],
                            {"frame": {"duration": frame_duration, "redraw": True},
                             "mode": "immediate",
                             "transition": {"duration": transition_duration}}],
                    "label": str(raid),
                    "method": "animate"
                } for raid in available_raids
            ]
        }]
    )
    
    # Add frames to the figure
    fig.frames = frames
    
    return apply_common_theme(fig) 