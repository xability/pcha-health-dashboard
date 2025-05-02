# PCHA Dashboard

The **PCHA Dashboard** is a PyShiny-based web application for visualizing user health data collected through the PCHA app. This tool extends the functionality of the mobile application by providing accessible visual analytics, including step count, calories burned, and distance walked over time.

## Live App

The dashboard is hosted at:  
[https://xabilitylab.shinyapps.io/pcha-dashboard/](https://xabilitylab.shinyapps.io/pcha-dashboard/)

## Features

- Interactive visualization of health metrics
- Date-based filtering for time-series analysis
- Designed with accessibility in mind using the `maidr` visualization library for blind and low vision users
- Responsive and accessible interface using PyShiny

## Technologies Used

- [PyShiny](https://shiny.posit.co/py/)
- `maidr` (for accessible graphs)
- Python, Plotly, and Pandas

## Getting Started

### Prerequisites

- Python 3.8+
- Packages: `shiny`, `maidr`, `pandas`, `plotly`, `datetime`, `numpy`

### Run Locally

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd Dashboard
pip install -r requirements.txt

# Run the app
shiny run --reload app.py
```

## Deployment

Whenever changes are pushed to the repository, the `deploy.yaml` workflow is triggered, and the latest version of the app is deployed to [shinyapps.io](https://www.shinyapps.io/). Log in to shinyapps.io using the organization credentials to manage deployments and application settings.

You can find the workflow file at `.github/workflows/deploy.yaml`.

## Contributing

We welcome improvements in UI, accessibility, or visualization logic. Please see the [CONTRIBUTING.md](./CONTRIBUTING.md) file for more details.
