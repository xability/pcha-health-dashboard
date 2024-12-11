import pandas as pd
import seaborn as sns
from pathlib import Path
from shiny import App, ui
import matplotlib.pyplot as plt
from maidr.widget.shiny import render_maidr

file_path = Path(__file__).parent / "healthdata.csv"
df = pd.read_csv(file_path)

df["user_id"] = df["user_id"].astype(str)
df["stepCount"] = pd.to_numeric(df["stepCount"], errors="coerce")
df["distanceWalkingRunning"] = pd.to_numeric(df["distanceWalkingRunning"], errors="coerce")
df["basalEnergyBurned"] = pd.to_numeric(df["basalEnergyBurned"], errors="coerce")
df["activeEnergyBurned"] = pd.to_numeric(df["activeEnergyBurned"], errors="coerce")
df["appleExerciseTime"] = pd.to_numeric(df["appleExerciseTime"], errors="coerce")

users = df["user_id"].unique().tolist()

# Define the UI
app_ui = ui.page_fluid(
    ui.h2("PCHA Dashboard"),
    ui.page_sidebar(  
    ui.sidebar(ui.input_select("user_id", label="Select User", choices=users), bg="#f8f8f8"), 
    ui.navset_card_tab(  
        ui.nav_panel("Step Count", ui.card(ui.output_ui("plot_stepCount"))),
        ui.nav_panel("Distance Walking/Running", ui.card(ui.output_ui("plot_distance"))),
        ui.nav_panel("Exercise Time", ui.card(ui.output_ui("plot_exerciseTime"))),
        ui.nav_panel("Basal Energy Burned", ui.card(ui.output_ui("plot_basalEnergy")),),
        ui.nav_panel("Active Energy Burned", ui.card(ui.output_ui("plot_activeEnergy"))),
    ),
)
)

# Define the server logic
def server(inp, _, __):
    @render_maidr
    def plot_distance():
        user_data = df[df["user_id"] == inp.user_id()]
        fig, ax = plt.subplots(figsize=(8, 6))
        s_plot = sns.barplot(data=user_data, x="date", y="distanceWalkingRunning", ax=ax)
        ax.set_title("Distance Covered Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Distance Covered (m)")
        ax.tick_params(axis="x", rotation=90, labelsize=5)
        return s_plot
    
    @render_maidr
    def plot_stepCount():
        user_data = df[df["user_id"] == inp.user_id()]
        fig, ax = plt.subplots(figsize=(8, 6))
        s_plot = sns.lineplot(data=user_data, x="date", y="stepCount", marker="o", ax=ax)
        ax.set_title("Step Count Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Steps Taken")
        ax.tick_params(axis="x", rotation=90, labelsize=5)
        return s_plot
    
    @render_maidr
    def plot_basalEnergy():
        user_data = df[df["user_id"] == inp.user_id()]
        fig, ax = plt.subplots(figsize=(8, 6))
        s_plot = sns.lineplot(data=user_data, x="date", y="basalEnergyBurned", marker="o", ax=ax)
        ax.set_title("Basal Energy Burned")
        ax.set_xlabel("Date")
        ax.set_ylabel("Energy Burned")
        ax.tick_params(axis="x", rotation=90, labelsize=5)
        return s_plot
    
    @render_maidr
    def plot_activeEnergy():
        user_data = df[df["user_id"] == inp.user_id()]
        fig, ax = plt.subplots(figsize=(8, 6))
        s_plot = sns.lineplot(data=user_data, x="date", y="activeEnergyBurned", marker="o", ax=ax)
        ax.set_title("Active Energy Burned")
        ax.set_xlabel("Date")
        ax.set_ylabel("Energy Burned")
        ax.tick_params(axis="x", rotation=90, labelsize=5)
        return s_plot
    
    @render_maidr
    def plot_exerciseTime():
        user_data = df[df["user_id"] == inp.user_id()]
        fig, ax = plt.subplots(figsize=(8, 6))
        s_plot = sns.barplot(data=user_data, x="date", y="appleExerciseTime", ax=ax)
        ax.set_title("Exercise Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Time Spent")
        ax.tick_params(axis="x", rotation=90, labelsize=5)
        return s_plot

# Create the app
app = App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run()
