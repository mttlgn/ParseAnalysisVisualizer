import streamlit as st
from mythic_data_loader import load_mythic_scaling_data
from mythic_visualizer import (
    create_scaling_line_chart,
    create_scaling_percentage_chart,
    create_scaling_comparison_chart
)

def show_mythic_page():
    st.title("Mythic+ Scaling Analysis")
    
    # Load data
    scaling_data = load_mythic_scaling_data()
    
    # Add description
    st.markdown("""
    This page analyzes the scaling differences between Season 1 and Season 2 Mythic+ dungeons.
    We look at different scaling scenarios and their implications for dungeon difficulty.
    """)
    
    # Animation controls
    st.sidebar.header("Animation Controls")
    use_animation = st.sidebar.checkbox("Enable Animation", value=False)
    
    # Base Scaling Analysis
    st.header("Base Scaling Comparison")
    st.markdown("""
    This section shows the base scaling values for both seasons and how they compare.
    The percentage difference indicates how much higher/lower Season 2 scaling is compared to Season 1.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_scaling_line_chart(
            scaling_data['percentages'],
            'Season 1 vs Season 2 Base Scaling',
            animate=use_animation,
            show_notes=False  # No notes for base comparison
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_scaling_percentage_chart(
            scaling_data['percentages'],
            animate=use_animation
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Alternative Scaling Scenarios
    st.header("Alternative Scaling Scenarios")
    st.markdown("""
    These scenarios show how the scaling would look with different baseline adjustments:
    - Scenario 1: Season 2 with 10% higher baseline
    - Scenario 2: Season 2 with 25% higher baseline
    
    Note: Hover over 📝 icons to see important notes about specific key levels.
    """)
    
    # 10% Higher Baseline
    st.subheader("Scenario 1: 10% Higher Baseline")
    fig = create_scaling_line_chart(
        scaling_data['10_higher'],
        'Scaling with 10% Higher Baseline in Season 2',
        animate=use_animation,
        show_notes=True  # Show notes for alternative scenarios
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 25% Higher Baseline
    st.subheader("Scenario 2: 25% Higher Baseline")
    fig = create_scaling_line_chart(
        scaling_data['25_higher'],
        'Scaling with 25% Higher Baseline in Season 2',
        animate=use_animation,
        show_notes=True  # Show notes for alternative scenarios
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparison View
    st.header("Bar Chart Comparison")
    st.markdown("""
    This view provides a direct comparison of scaling values between seasons using bars,
    which can make it easier to see the absolute differences at each key level.
    """)
    
    fig = create_scaling_comparison_chart(
        scaling_data['percentages'],
        animate=use_animation
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Data Tables
    with st.expander("Show Raw Data"):
        st.subheader("Base Scaling Percentages")
        st.dataframe(scaling_data['percentages'])
        
        st.subheader("10% Higher Baseline")
        st.dataframe(scaling_data['10_higher'])
        
        st.subheader("25% Higher Baseline")
        st.dataframe(scaling_data['25_higher']) 