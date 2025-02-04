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