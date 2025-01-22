import pandas as pd
import seaborn as sns
from pathlib import Path
from shiny import App, ui
import matplotlib.pyplot as plt
from maidr.widget.shiny import render_maidr

file_path = Path(__file__).parent / "healthdata.csv"
df = pd.read_csv(file_path)

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str, format="%b %d, %Y")  # Format: "Jun 13, 2024"
    except ValueError:
        try:
            return pd.to_datetime(date_str, format="%d %b %Y", dayfirst=True)
        except ValueError:
            return pd.NaT  # Handle invalid dates

df['parsed_date'] = df['date'].apply(parse_date)
df = df.dropna(subset=['parsed_date'])  # Remove rows with invalid parsed dates

# min_date = df['parsed_date'].min()
# max_date = df['parsed_date'].max()

users = df["user_id"].unique().tolist()

# Define the UI
app_ui = ui.page_fluid(
    ui.h2("PCHA Dashboard"),
    ui.page_sidebar(  
    ui.sidebar(ui.input_select("user_id", label="Select User", choices=users), 
            #    ui.input_slider("start_date_slider", "Start Date", min_date, max_date, min_date),
            #    ui.input_slider("end_date_slider", "End Date",  min_date, max_date, max_date),
            ui.input_text("start_day", label="Start Day", placeholder="DD"),
            ui.input_text("start_month", label="Start Month", placeholder="MM"),
            ui.input_text("start_year", label="Start Year", placeholder="YYYY"),
            ui.input_text("end_day", label="End Day", placeholder="DD"),
            ui.input_text("end_month", label="End Month", placeholder="MM"),
            ui.input_text("end_year", label="End Year", placeholder="YYYY"),
                bg="#f8f8f8"
            ), 
    ui.navset_card_tab(  
        ui.nav_panel("Step Count", ui.card(ui.output_ui("plot_stepCount"))),
        ui.nav_panel("Distance Walking/Running", ui.card(ui.output_ui("plot_distance"))),
        ui.nav_panel("Exercise Time", ui.card(ui.output_ui("plot_exerciseTime"))),
        ui.nav_panel("Basal Energy Burned", ui.card(ui.output_ui("plot_basalEnergy")),),
        ui.nav_panel("Active Energy Burned", ui.card(ui.output_ui("plot_activeEnergy"))),
    ),
)
)

def server(inp, _, __):
    
    @render_maidr
    def plot_stepCount():
        user_data = df[df["user_id"] == inp.user_id()]
        user_id = inp.user_id()  # Selected user

        # Fetch start and end dates. If null, default to min and max dates
        try:
            start_date = pd.to_datetime(f"{inp.start_year()}-{inp.start_month()}-{inp.start_day()}")
        except ValueError:
            start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

        try:
            end_date = pd.to_datetime(f"{inp.end_year()}-{inp.end_month()}-{inp.end_day()}")
        except ValueError:
            end_date = df['parsed_date'].max()

        # Filter data for the selected user and date range
        user_data = df[
            (df["user_id"] == user_id) &
            (df["parsed_date"] >= start_date) &
            (df["parsed_date"] <= end_date)
        ]

        fig, ax = plt.subplots(figsize=(10, 8))
        s_plot = sns.lineplot(data=user_data, x="date", y="stepCount", marker="o", ax=ax)
        ax.set_title("Step Count Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Steps Taken")
        ax.tick_params(axis="x", rotation=90, labelsize=5)
        return s_plot
    
    @render_maidr
    def plot_distance():
        user_data = df[df["user_id"] == inp.user_id()]  
        user_id = inp.user_id()  # Selected user

        # Fetch start and end dates. If null, default to min and max dates
        try:
            start_date = pd.to_datetime(f"{inp.start_year()}-{inp.start_month()}-{inp.start_day()}")
        except ValueError:
            start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

        try:
            end_date = pd.to_datetime(f"{inp.end_year()}-{inp.end_month()}-{inp.end_day()}")
        except ValueError:
            end_date = df['parsed_date'].max()


        # Filter data for the selected user and date range
        user_data = df[
            (df["user_id"] == user_id) &
            (df["parsed_date"] >= start_date) &
            (df["parsed_date"] <= end_date)
        ]

        fig, ax = plt.subplots(figsize=(10, 8))
        s_plot = sns.barplot(data=user_data, x="date", y="distanceWalkingRunning", ax=ax)
        ax.set_title("Distance Covered Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Distance Covered (m)")
        ax.tick_params(axis="x", rotation=90, labelsize=5)
        return s_plot
    
    @render_maidr
    def plot_basalEnergy():
        user_data = df[df["user_id"] == inp.user_id()]
        user_id = inp.user_id()  # Selected user

        # Fetch start and end dates. If null, default to min and max dates
        try:
            start_date = pd.to_datetime(f"{inp.start_year()}-{inp.start_month()}-{inp.start_day()}")
        except ValueError:
            start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

        try:
            end_date = pd.to_datetime(f"{inp.end_year()}-{inp.end_month()}-{inp.end_day()}")
        except ValueError:
            end_date = df['parsed_date'].max()

        # Filter data for the selected user and date range
        user_data = df[
            (df["user_id"] == user_id) &
            (df["parsed_date"] >= start_date) &
            (df["parsed_date"] <= end_date)
        ]

        fig, ax = plt.subplots(figsize=(10, 8))
        s_plot = sns.lineplot(data=user_data, x="date", y="basalEnergyBurned", marker="o", ax=ax)
        ax.set_title("Basal Energy Burned")
        ax.set_xlabel("Date")
        ax.set_ylabel("Energy Burned (cals)")
        ax.tick_params(axis="x", rotation=90, labelsize=5)
        return s_plot
    
    @render_maidr
    def plot_activeEnergy():
        user_data = df[df["user_id"] == inp.user_id()]
        user_id = inp.user_id()  # Selected user

        # Fetch start and end dates. If null, default to min and max dates
        try:
            start_date = pd.to_datetime(f"{inp.start_year()}-{inp.start_month()}-{inp.start_day()}")
        except ValueError:
            start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

        try:
            end_date = pd.to_datetime(f"{inp.end_year()}-{inp.end_month()}-{inp.end_day()}")
        except ValueError:
            end_date = df['parsed_date'].max()

        # Filter data for the selected user and date range
        user_data = df[
            (df["user_id"] == user_id) &
            (df["parsed_date"] >= start_date) &
            (df["parsed_date"] <= end_date)
        ]

        fig, ax = plt.subplots(figsize=(10, 8))
        s_plot = sns.lineplot(data=user_data, x="date", y="activeEnergyBurned", marker="o", ax=ax)
        ax.set_title("Active Energy Burned")
        ax.set_xlabel("Date")
        ax.set_ylabel("Energy Burned (cals)")
        ax.tick_params(axis="x", rotation=90, labelsize=5)
        return s_plot
    
    @render_maidr
    def plot_exerciseTime():
        user_data = df[df["user_id"] == inp.user_id()]
        user_id = inp.user_id()  # Selected user

        # Fetch start and end dates. If null, default to min and max dates
        try:
            start_date = pd.to_datetime(f"{inp.start_year()}-{inp.start_month()}-{inp.start_day()}")
        except ValueError:
            start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

        try:
            end_date = pd.to_datetime(f"{inp.end_year()}-{inp.end_month()}-{inp.end_day()}")
        except ValueError:
            end_date = df['parsed_date'].max()

        # Filter data for the selected user and date range
        user_data = df[
            (df["user_id"] == user_id) &
            (df["parsed_date"] >= start_date) &
            (df["parsed_date"] <= end_date)
        ]


        fig, ax = plt.subplots(figsize=(10, 8))
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
