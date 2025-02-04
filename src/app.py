import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

from data_loader import load_all_raids, calculate_percentages
from analyzer import (
    compare_raids, 
    identify_trends, 
    get_top_specs, 
    identify_class_trends,
    analyze_class_changes
)
from visualizer import (
    create_spec_distribution_chart,
    create_spec_treemap,
    create_trend_chart,
    create_delta_chart,
    create_class_trend_chart,
    create_class_change_chart,
    create_class_pie_chart,
    create_spec_pie_chart,
    WOW_CLASS_COLORS
)

st.set_page_config(layout="wide", page_title="WoW Raid Analysis")

st.title("Class Participation Changes Over Time")

# Load all raid data
raid_data = load_all_raids()
raid_names = list(raid_data.keys())

# Define global text styling
text_style = dict(
    family='"Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", Arial, sans-serif',
    size=16,
    color='white',
    weight='bold',
    shadow="2px 2px 4px black"
)
inside_text_style = dict(
    family='"Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", Arial, sans-serif',
    size=16,
    color='white',
    weight='bold',
    shadow="2px 2px 4px black"
)
base_title_style = dict(
    font=dict(
        family='"Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", Arial, sans-serif',
        size=20,
        color='white',
        weight='bold'
    )
)
legend_style = dict(
    font=dict(
        family='"Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", Arial, sans-serif',
        size=16,
        color='white',
        weight='bold'
    ),
    bgcolor='rgba(0,0,0,0.5)',
    bordercolor='white',
    borderwidth=1
)

# Function to create title style with specific text
def create_title_style(title_text):
    return {**base_title_style, 'text': title_text}

# Sidebar for raid selection
st.sidebar.header("Raid Selection")
selected_raid = st.sidebar.selectbox(
    "Select View",
    ["All Raids", "Class Analysis", "Individual Raid"] + raid_names,
    help="Choose between overview, class analysis, or specific raid views"
)

# Main content
if selected_raid == "Class Analysis":
    st.header("Class Analysis")
    
    # Class selection
    selected_class = st.selectbox(
        "Select Class to Analyze",
        sorted(WOW_CLASS_COLORS.keys())
    )
    
    # Raid exclusion
    raids_to_exclude = st.multiselect(
        "Exclude Raids from Analysis",
        options=raid_names,
        help="Select raids to exclude from the analysis (e.g., to remove pre-patch or specific versions)"
    )
    
    if selected_class:
        # Historical representation
        st.subheader(f"{selected_class} Historical Representation")
        
        # Get class-specific trend data
        class_trend_df = identify_class_trends(raid_data, exclude_raids=raids_to_exclude)
        class_specific_trend = class_trend_df[class_trend_df['Class'] == selected_class]
        
        # Line chart for historical percentage
        fig = px.line(
            class_specific_trend,
            x='Raid',
            y='Percentage',
            title=f'{selected_class} Representation Over Time',
            color_discrete_sequence=[WOW_CLASS_COLORS[selected_class]]
        )
        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis_title='Share (%)',
            plot_bgcolor='rgba(0,0,0,0.05)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Changes between raids
        st.subheader("Raid-to-Raid Changes")
        changes_df = analyze_class_changes(raid_data, selected_class, exclude_raids=raids_to_exclude)
        if not changes_df.empty:
            fig = create_class_change_chart(changes_df, selected_class)
            fig.update_traces(
                textfont=text_style,
            )
            fig.update_layout(
                font=text_style,
                title=create_title_style(f'{selected_class} Representation Changes'),
                legend=legend_style
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Latest raid stats and spec distribution
        st.subheader("Current Status")
        
        # Add raid selection dropdown
        selected_status_raid = st.selectbox(
            "Select Raid for Status Analysis",
            options=raid_names,
            index=len(raid_names)-1,  # Default to latest raid
            help="Choose which raid to analyze for current status"
        )
        
        current_df, _ = calculate_percentages(raid_data[selected_status_raid])
        class_current = current_df[current_df['Class'] == selected_class]
        
        # Add spec pie chart for the selected class
        fig = create_spec_pie_chart(current_df, selected_class)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_class_percentage = class_current['Percentage'].sum()
            st.metric("Total Class Share", f"{total_class_percentage:.2f}%")
            
        with col2:
            total_parses = class_current['Parses'].sum()
            st.metric("Total Parses", f"{total_parses:,}")
        
        # Spec breakdown table
        st.subheader("Current Spec Distribution")
        spec_table = class_current[['Spec', 'Parses', 'Percentage']].sort_values('Percentage', ascending=False)
        st.dataframe(spec_table)
        
        # Spec distribution over time
        st.subheader("Specialization Distribution")
        spec_trend_df = identify_trends(raid_data, exclude_raids=raids_to_exclude)
        class_specs_df = spec_trend_df[spec_trend_df['Class'] == selected_class]
        
        fig = px.line(
            class_specs_df,
            x='Raid',
            y='Percentage',
            color='Spec',
            title=f'{selected_class} Spec Distribution Over Time',
            color_discrete_sequence=[WOW_CLASS_COLORS[selected_class]] * len(class_specs_df['Spec'].unique())
        )
        fig.update_layout(
            height=400,
            yaxis_title='Share (%)',
            plot_bgcolor='rgba(0,0,0,0.05)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Historical data table in expander
        with st.expander("Show Historical Data"):
            st.dataframe(class_specific_trend.sort_values('Raid'))

elif selected_raid == "All Raids":
    st.header("All Raids Overview")
    
    # Add raid exclusion multiselect
    raids_to_exclude = st.multiselect(
        "Exclude Raids from Analysis",
        options=raid_names,
        help="Select raids to exclude from the analysis (e.g., to remove pre-patch or specific versions)"
    )
    
    # Class Trends
    st.subheader("Class Representation Trends")
    class_trend_df = identify_class_trends(raid_data, exclude_raids=raids_to_exclude)
    fig = create_class_trend_chart(class_trend_df)
    fig.update_traces(
        textfont=text_style,
    )
    fig.update_layout(
        font=text_style,
        title=create_title_style('Class Representation Trends'),
        legend=legend_style
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Class Change Analysis
    st.subheader("Class Change Analysis")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_class = st.selectbox(
            "Select Class to Analyze",
            sorted(WOW_CLASS_COLORS.keys())
        )
    
    with col2:
        # Add separate raid exclusion for class analysis
        class_raids_to_exclude = st.multiselect(
            "Exclude Raids",
            options=raid_names,
            help="Select raids to exclude from this class analysis"
        )
    
    if selected_class:
        changes_df = analyze_class_changes(raid_data, selected_class, exclude_raids=class_raids_to_exclude)
        if not changes_df.empty:
            fig = create_class_change_chart(changes_df, selected_class)
            fig.update_traces(
                textfont=text_style,
            )
            fig.update_layout(
                font=text_style,
                title=create_title_style(f'{selected_class} Representation Changes'),
                legend=legend_style
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show the changes in a table
            expander = st.expander("Show Detailed Changes")
            with expander:
                st.dataframe(changes_df)
    
    # Spec Trends
    st.subheader("Specialization Trends")
    spec_trend_df = identify_trends(raid_data, exclude_raids=raids_to_exclude)
    fig = create_trend_chart(spec_trend_df)
    fig.update_traces(
        textfont=text_style,
    )
    fig.update_layout(
        font=text_style,
        title=create_title_style('Specialization Trends Across Raids'),
        legend=legend_style
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Add Total Change Analysis section
    st.subheader("Changes Between Raids")
    
    # Get list of raids excluding the ones user wants to exclude
    filtered_raids = [raid for raid in raid_names if raid not in raids_to_exclude]
    
    if filtered_raids:
        # Calculate changes between consecutive raids
        changes_data = []
        
        # Add first raid as baseline
        changes_data.append({
            'Raid': filtered_raids[0],
            'Change From Previous Raid': 0.0,
            'Biggest Increases': "Baseline",
            'Biggest Drops': "Baseline"
        })

        # Calculate changes between consecutive raids
        for i in range(len(filtered_raids)-1):
            current_raid = filtered_raids[i]
            next_raid = filtered_raids[i+1]
            comparison_df = compare_raids(raid_data[current_raid], raid_data[next_raid])
            
            total_positive = comparison_df[comparison_df['Percentage_Change'] > 0]['Percentage_Change'].sum()
            
            # Get top 3 positive changes for context
            top_positive_changes = comparison_df[comparison_df['Percentage_Change'] > 0].nlargest(3, 'Percentage_Change')
            top_positive_changes_text = ", ".join([f"{row['Spec']} (+{row['Percentage_Change']:.1f}%)" for _, row in top_positive_changes.iterrows()])
            # Get top 3 negative changes for context
            top_negative_changes = comparison_df[comparison_df['Percentage_Change'] < 0].nsmallest(3, 'Percentage_Change')
            top_negative_changes_text = ", ".join([f"{row['Spec']} ({row['Percentage_Change']:.1f}%)" for _, row in top_negative_changes.iterrows()])
            
            changes_data.append({
                'Raid': next_raid,
                'Change From Previous Raid': total_positive,
                'Biggest Increases': top_positive_changes_text,
                'Biggest Drops': top_negative_changes_text
            })

        

        # Create a DataFrame and display it
        changes_df = pd.DataFrame(changes_data)
        
        # Format and display the table
        st.dataframe(
            changes_df.style
            .format({
                'Change From Previous Raid': '{:.1f}%'
            })
            .set_properties(**{
                'text-align': 'left',
                'font-size': '16px'
            })
            .set_table_styles([
                {'selector': 'th', 'props': [('font-size', '16px'), ('text-align', 'left')]},
                {'selector': 'td', 'props': [('padding', '8px')]}
            ]),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("No raids available for analysis. Please adjust your raid exclusions.")
    
    # Latest raid composition overview with pie charts
    latest_raid = raid_names[-1]
    
    # Add raid selector for composition analysis
    selected_composition_raid = st.selectbox(
        "Select Raid for Composition Analysis",
        options=raid_names,
        index=len(raid_names)-1,  # Default to latest raid
        help="Choose which raid to analyze for class and spec distribution"
    )
    
    composition_df, composition_totals = calculate_percentages(raid_data[selected_composition_raid])
    
    st.subheader(f"Raid Composition ({selected_composition_raid})")
    
    # Add pie charts in a row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Class Distribution")
        fig = create_class_pie_chart(composition_df)
        fig.update_traces(
            textposition='inside',
            textinfo='label+percent',
            texttemplate='%{label}<br>%{percent:.1%}',
            textfont=text_style,
            insidetextfont=inside_text_style
        )
        fig.update_layout(
            font=text_style,
            title=create_title_style('Class Distribution Overview'),
            showlegend=True,
            legend=legend_style
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("All Specializations")
        fig = create_spec_pie_chart(composition_df)
        fig.update_traces(
            textposition='inside',
            textinfo='label+percent',
            texttemplate='%{label}<br>%{percent:.1%}',
            textfont=text_style,
            insidetextfont=inside_text_style
        )
        fig.update_layout(
            font=text_style,
            title=create_title_style('All Specializations Distribution'),
            showlegend=True,
            legend=legend_style,
            uniformtext=dict(
                minsize=14,
                mode='hide'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Original visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Class/Spec Distribution")
        fig = create_spec_distribution_chart(composition_df)
        fig.update_traces(
            textfont=text_style,
        )
        fig.update_layout(
            font=text_style,
            title=create_title_style('Class and Specialization Distribution'),
            legend=legend_style
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Distribution Treemap")
        fig = create_spec_treemap(composition_df)
        fig.update_traces(
            textfont=text_style,
        )
        fig.update_layout(
            font=text_style,
            title=create_title_style('Class and Specialization Hierarchy'),
            legend=legend_style
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top specs across all non-excluded raids
    st.subheader("Top 5 Specs (Latest Raid)")
    top_specs = get_top_specs(composition_df)
    st.dataframe(top_specs[['Class', 'Spec', 'Parses', 'Percentage']])

elif selected_raid == "Individual Raid":
    st.header("Select a specific raid from the dropdown above")

else:
    st.header(f"Analysis for {selected_raid}")
    
    # Get data for selected raid
    current_raid_data = raid_data[selected_raid]
    raid_df, class_totals = calculate_percentages(current_raid_data)
    
    # Display top specs
    st.subheader("Top 5 Specs")
    top_specs = get_top_specs(raid_df)
    st.dataframe(top_specs[['Class', 'Spec', 'Parses', 'Percentage']])
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Class/Spec Distribution")
        fig = create_spec_distribution_chart(raid_df)
        fig.update_traces(
            textfont=text_style,
        )
        fig.update_layout(
            font=text_style,
            title=create_title_style('Class and Specialization Distribution'),
            legend=legend_style
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Distribution Treemap")
        fig = create_spec_treemap(raid_df)
        fig.update_traces(
            textfont=text_style,
        )
        fig.update_layout(
            font=text_style,
            title=create_title_style('Class and Specialization Hierarchy'),
            legend=legend_style
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Raid comparison section
    st.header("Raid Comparison")
    comparison_raid = st.selectbox(
        "Select Raid to Compare With",
        [r for r in raid_names if r != selected_raid]
    )
    
    if comparison_raid:
        comparison_df = compare_raids(raid_data[selected_raid], raid_data[comparison_raid])
        
        st.subheader(f"Changes from {selected_raid} to {comparison_raid}")
        
        # Calculate changes
        total_positive_change = comparison_df[comparison_df['Percentage_Change'] > 0]['Percentage_Change'].sum()
        total_negative_change = comparison_df[comparison_df['Percentage_Change'] < 0]['Percentage_Change'].sum()
        net_change = total_positive_change + total_negative_change  # Should be very close to 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Positive Change", f"{total_positive_change:.1f}%", 
                     help="Sum of all positive percentage changes, indicating total class/spec movement")
        with col2:
            st.metric("Total Negative Change", f"{total_negative_change:.1f}%",
                     help="Sum of all negative percentage changes (should balance with positive)")
        with col3:
            st.metric("Net Change", f"{net_change:.2f}%",
                     help="Net change across all specs (should be very close to 0)")
        
        fig = create_delta_chart(comparison_df)
        st.plotly_chart(fig, use_container_width=True)
    
    # Raw Data
    if st.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.dataframe(raid_df) 