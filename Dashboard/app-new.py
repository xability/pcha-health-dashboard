# import datetime
# import pandas as pd
# import seaborn as sns
# from pathlib import Path
# import matplotlib.pyplot as plt
# from pymongo import MongoClient
# from shiny import App, ui, reactive, render_ui, render
# from maidr.widget.shiny import render_maidr


# def parse_date(date_str):
#     """Try parsing the date in two possible formats."""
#     try:
#         return pd.to_datetime(date_str, format="%b %d, %Y")  # e.g., "Jun 13, 2024"
#     except ValueError:
#         try:
#             return pd.to_datetime(date_str, format="%d %b %Y", dayfirst=True)
#         except ValueError:
#             return pd.NaT  # Return NaT for invalid dates

# def fetch_data():
#     """Connect to Azure Cosmos DB, flatten the nested documents, and return a DataFrame."""
#     connection_string = (
#         "mongodb://pcha:DBQWfFLdaAwofXET3QyLDt1ndCAbJdGwoq8iF4u79P2A0QArmODzkbENAMqtobHZOhDn765q2dlmACDbeuMcHg=="
#         "@pcha.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb"
#         "&maxIdleTimeMS=120000&appName=@pcha@"
#     )
#     client = MongoClient(connection_string, tlsAllowInvalidCertificates=True)
#     db = client['pcha_db']
#     collection = db['health_data']
#     cursor = collection.find()

#     flattened_data = []
#     for document in cursor:
#         _id = document["_id"]
#         user_id = document["user_id"]
#         for date_entry in document["dates"]:
#             flattened_entry = {"_id": _id, "user_id": user_id, "date": date_entry["date"]}
#             # Unpack nested data values
#             for key, value in date_entry["data"].items():
#                 flattened_entry[key] = value["value"]
#             flattened_data.append(flattened_entry)
    
#     df = pd.DataFrame(flattened_data)
#     # Parse dates and drop rows with invalid dates
#     df['parsed_date'] = df['date'].apply(parse_date)
#     df = df.dropna(subset=['parsed_date'])
#     return df

# # Fetch the initial data when the app starts.
# initial_df = fetch_data()
# users = initial_df["user_id"].unique().tolist()

# # -------------------------------------------------------
# # 2. Define the UI
# # -------------------------------------------------------

# app_ui = ui.page_fluid(
#     ui.h2("PCHA Health Dashboard"),
#     ui.page_sidebar(
#         ui.sidebar(
#             # Render the user selection dynamically.
#             ui.input_select("user_id", label="Select User", choices=users),
#             # Button to refresh the data.
#             ui.input_action_button("refresh_data", "Refresh Data"),
#             # ui.input_action_button("reset_filter", "Reset Filters"),
#             # Additional inputs (e.g., for date filtering)
#             ui.input_text("start_day", label="Start Day", placeholder="DD"),
#             ui.input_text("start_month", label="Start Month", placeholder="MM"),
#             ui.input_text("start_year", label="Start Year", placeholder="YYYY"),
#             ui.input_text("end_day", label="End Day", placeholder="DD"),
#             ui.input_text("end_month", label="End Month", placeholder="MM"),
#             ui.input_text("end_year", label="End Year", placeholder="YYYY"),
#             bg="#f8f8f8"
#         ),
#         ui.navset_card_tab(  
#             ui.nav_panel("Step Count", ui.card(ui.output_ui("plot_stepCount"))),
#             ui.nav_panel("Distance Walking/Running", ui.card(ui.output_ui("plot_distance"))),
#             ui.nav_panel("Exercise Time", ui.card(ui.output_ui("plot_exerciseTime"))),
#             ui.nav_panel("Basal Energy Burned", ui.card(ui.output_ui("plot_basalEnergy")),),
#             ui.nav_panel("Active Energy Burned", ui.card(ui.output_ui("plot_activeEnergy"))),
#         ),
#     )
# )


# # -------------------------------------------------------
# # 3. Define Server Logic
# # -------------------------------------------------------

# def server(input, output, session):
#     data_store = reactive.Value(initial_df)
    
#     @reactive.Effect
#     def refresh_data_effect():
#         _ = input.refresh_data()
#         new_df = fetch_data()
#         data_store.set(new_df)
#         print("Data refreshed at", datetime.datetime.now())

#     # @reactive.Effect
#     # def reset_filter_effect():
#     #     _ = input.reset_filter()
#     #     df = fetch_data()
#     #     start_date = df['parsed_date'].min() 
#     #     end_date = df['parsed_date'].max()
    
    
#     @render_maidr
#     def plot_stepCount():
#         df_latest = data_store.get()
#         user_id = input.user_id()
#         df = df_latest[df_latest["user_id"] == user_id]
#         try:
#             start_date = pd.to_datetime(f"{input.start_year()}-{input.start_month()}-{input.start_day()}")
#         except ValueError:
#             start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

#         try:
#             end_date = pd.to_datetime(f"{input.end_year()}-{input.end_month()}-{input.end_day()}")
#         except ValueError:
#             end_date = df['parsed_date'].max()

#         # Filter data for the selected user and date range
#         user_data = df[
#             (df["user_id"] == user_id) &
#             (df["parsed_date"] >= start_date) &
#             (df["parsed_date"] <= end_date)
#         ]
#         user_data = user_data.sort_values(by="parsed_date")

#         fig, ax = plt.subplots(figsize=(10, 8))
#         s_plot = sns.lineplot(data=user_data, x="date", y="stepCount", marker="o", ax=ax)
#         ax.set_title("Step Count Over Time")
#         ax.set_xlabel("Date")
#         ax.set_ylabel("Steps Taken")
#         ax.tick_params(axis="x", rotation=90, labelsize=5)
#         return s_plot
    
#     @render_maidr
#     def plot_distance():
#         df_latest = data_store.get()
#         user_id = input.user_id()
#         df = df_latest[df_latest["user_id"] == user_id]

#         # Fetch start and end dates. If null, default to min and max dates
#         try:
#             start_date = pd.to_datetime(f"{input.start_year()}-{input.start_month()}-{input.start_day()}")
#         except ValueError:
#             start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

#         try:
#             end_date = pd.to_datetime(f"{input.end_year()}-{input.end_month()}-{input.end_day()}")
#         except ValueError:
#             end_date = df['parsed_date'].max()


#         # Filter data for the selected user and date range
#         user_data = df[
#             (df["user_id"] == user_id) &
#             (df["parsed_date"] >= start_date) &
#             (df["parsed_date"] <= end_date)
#         ]

#         fig, ax = plt.subplots(figsize=(10, 8))
#         s_plot = sns.barplot(data=user_data, x="date", y="distanceWalkingRunning", ax=ax)
#         ax.set_title("Distance Covered Over Time")
#         ax.set_xlabel("Date")
#         ax.set_ylabel("Distance Covered (m)")
#         ax.tick_params(axis="x", rotation=90, labelsize=5)
#         return s_plot
    
#     @render_maidr
#     def plot_basalEnergy():
#         df_latest = data_store.get()
#         user_id = input.user_id()
#         df = df_latest[df_latest["user_id"] == user_id]

#         # Fetch start and end dates. If null, default to min and max dates
#         try:
#             start_date = pd.to_datetime(f"{input.start_year()}-{input.start_month()}-{input.start_day()}")
#         except ValueError:
#             start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

#         try:
#             end_date = pd.to_datetime(f"{input.end_year()}-{input.end_month()}-{input.end_day()}")
#         except ValueError:
#             end_date = df['parsed_date'].max()

#         # Filter data for the selected user and date range
#         user_data = df[
#             (df["user_id"] == user_id) &
#             (df["parsed_date"] >= start_date) &
#             (df["parsed_date"] <= end_date)
#         ]

#         fig, ax = plt.subplots(figsize=(10, 8))
#         s_plot = sns.lineplot(data=user_data, x="date", y="basalEnergyBurned", marker="o", ax=ax)
#         ax.set_title("Basal Energy Burned")
#         ax.set_xlabel("Date")
#         ax.set_ylabel("Energy Burned (cals)")
#         ax.tick_params(axis="x", rotation=90, labelsize=5)
#         return s_plot
    
#     @render_maidr
#     def plot_activeEnergy():
#         df_latest = data_store.get()
#         user_id = input.user_id()
#         df = df_latest[df_latest["user_id"] == user_id]

#         # Fetch start and end dates. If null, default to min and max dates
#         try:
#             start_date = pd.to_datetime(f"{input.start_year()}-{input.start_month()}-{input.start_day()}")
#         except ValueError:
#             start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

#         try:
#             end_date = pd.to_datetime(f"{input.end_year()}-{input.end_month()}-{input.end_day()}")
#         except ValueError:
#             end_date = df['parsed_date'].max()

#         # Filter data for the selected user and date range
#         user_data = df[
#             (df["user_id"] == user_id) &
#             (df["parsed_date"] >= start_date) &
#             (df["parsed_date"] <= end_date)
#         ]

#         fig, ax = plt.subplots(figsize=(10, 8))
#         s_plot = sns.lineplot(data=user_data, x="date", y="activeEnergyBurned", marker="o", ax=ax)
#         ax.set_title("Active Energy Burned")
#         ax.set_xlabel("Date")
#         ax.set_ylabel("Energy Burned (cals)")
#         ax.tick_params(axis="x", rotation=90, labelsize=5)
#         return s_plot
    
#     @render_maidr
#     def plot_exerciseTime():
#         df_latest = data_store.get()
#         user_id = input.user_id()
#         df = df_latest[df_latest["user_id"] == user_id]

#         # Fetch start and end dates. If null, default to min and max dates
#         try:
#             start_date = pd.to_datetime(f"{input.start_year()}-{input.start_month()}-{input.start_day()}")
#         except ValueError:
#             start_date = df['parsed_date'].min()  # Default to earliest date in the dataset

#         try:
#             end_date = pd.to_datetime(f"{input.end_year()}-{input.end_month()}-{input.end_day()}")
#         except ValueError:
#             end_date = df['parsed_date'].max()

#         # Filter data for the selected user and date range
#         user_data = df[
#             (df["user_id"] == user_id) &
#             (df["parsed_date"] >= start_date) &
#             (df["parsed_date"] <= end_date)
#         ]


#         fig, ax = plt.subplots(figsize=(10, 8))
#         s_plot = sns.barplot(data=user_data, x="date", y="appleExerciseTime", ax=ax)
#         ax.set_title("Exercise Time")
#         ax.set_xlabel("Date")
#         ax.set_ylabel("Time Spent")
#         ax.tick_params(axis="x", rotation=90, labelsize=5)
#         return s_plot

# # -------------------------------------------------------
# # 4. Create and Run the App
# # -------------------------------------------------------

# app = App(app_ui, server)

# if __name__ == "__main__":
#     app.run()