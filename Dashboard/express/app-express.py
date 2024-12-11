import maidr
from maidr.widget.shiny import render_maidr

import pandas as pd
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.express as px

from shinywidgets import render_plotly
from shiny.express import ui, render, input

# Load and preprocess data
file_path = Path(__file__).parent / "healthdata.csv"
df = pd.read_csv(file_path)

# Ensure proper data types
df["user_id"] = df["user_id"].astype(str)  # Ensure user_id is string
df["stepCount"] = pd.to_numeric(df["stepCount"], errors="coerce")
df["distanceWalkingRunning"] = pd.to_numeric(df["distanceWalkingRunning"], errors="coerce")

# Get unique user IDs
users = df["user_id"].unique().tolist()
ui.page_opts(title="PCHA Dashboard")
ui.input_select("user_id", label="Select user", choices=users)


##PLOTS
with ui.layout_columns():  
    with ui.card():  
        ui.card_header("Step count")
        @render_plotly
        def stepCount():
            user_data = df[df["user_id"] == input.user_id()]
            if user_data.empty:
                return px.line(title="No Data Found")  # Handle empty data
            return px.bar(user_data, x="date", y="stepCount")

    with ui.card():  
        ui.card_header("Distance Walking/Running")
        @render_plotly
        def distWalkingRunning():
            user_data = df[df["user_id"] == input.user_id()]
            if user_data.empty:
                return px.line(title="No Data Found")
            return px.line(user_data, x="date", y="distanceWalkingRunning", labels={"distanceWalkingRunning": "Distance covered (m)", "date": "Date"})
        
with ui.layout_columns():  
    with ui.card():  
        ui.card_header("Basal Energy Burned")
        @render_plotly
        def basalEnergyBurned():
            user_data = df[df["user_id"] == input.user_id()]
            if user_data.empty:
                return px.line(title="No Data Found")

            plot_data = user_data[["date", "basalEnergyBurned"]]

            # Reshape the data for multiple lines
            plot_data = plot_data.melt(id_vars="date", 
                                    value_vars=["basalEnergyBurned"], 
                                    var_name="EnergyType", 
                                    value_name="Energy")

            # Plot the lines
            fig = px.line(plot_data, x="date", y="Energy", color="EnergyType", labels={"Energy": "Energy Burned (kcal)", "date": "Date"})
            return fig
        
    with ui.card():  
        ui.card_header("Active Energy Burned")
        @render_plotly
        def activeEnergyBurned():
            user_data = df[df["user_id"] == input.user_id()]
            if user_data.empty:
                return px.line(title="No Data Found")

            plot_data = user_data[["date", "activeEnergyBurned"]]

            # Reshape the data for multiple lines
            plot_data = plot_data.melt(id_vars="date", 
                                    value_vars=["activeEnergyBurned"], 
                                    var_name="EnergyType", 
                                    value_name="Energy")

            # Plot the lines
            fig = px.line(plot_data, x="date", y="Energy", color="EnergyType", labels={"Energy": "Energy Burned (kcal)", "date": "Date"})
            return fig

with ui.layout_columns(): 
     with ui.card():  
        ui.card_header("Exercise Time")
        @render_plotly
        def appleExerciseTime():
            user_data = df[df["user_id"] == input.user_id()]
            if user_data.empty:
                return px.line(title="No Data Found")  # Handle empty data

            plot_data = user_data[["date", "appleExerciseTime"]]

            # Reshape the data for multiple lines
            plot_data = plot_data.melt(id_vars="date", 
                                    value_vars="appleExerciseTime", 
                                    var_name="exerciseTime", 
                                    value_name="Time")

            # Plot the lines
            fig = px.bar(plot_data, x="date", y="Time", labels={"Time": "Exercise Time (minutes)", "date": "Date"})
            return fig