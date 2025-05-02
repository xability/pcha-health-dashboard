# Contributing to PCHA Dashboard

Thank you for your interest in contributing to the **PCHA Dashboard**, a PyShiny-based accessible health data visualization tool.

---

## How to Contribute

### 1. Fork and Clone

```bash
git clone https://github.com/xability/pcha-health-dashboard.git
cd Dashboard
```

### 2. Set Up Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the App Locally

```bash
shiny run --reload app.py
```

---

## Guidelines

- Follow PEP8 and Python best practices
- Use `maidr` for all key data visualizations to ensure accessibility
- Clearly label all charts and filters
- Use semantic HTML where applicable for screen reader compatibility

---

## Accessibility Standards

We aim to provide full access to users who are blind or have low vision. Please:

- Ensure graphs are compatible with `maidr`
- Include alt-text or captions where possible
- Avoid relying solely on visual cues (e.g., color-only distinctions)

---

## Deployment

Deployment is handled through [shinyapps.io](https://www.shinyapps.io/)

1. Ensure the app runs correctly locally
2. Deploy using `rsconnect` with Python support or push updates to the hosting environment

---

## Reporting Issues

If you find a bug or have a feature request, open an issue at:  
[https://github.com/xabilitylab/pcha-dashboard/issues](https://github.com/xabilitylab/pcha-dashboard/issues)

Thank you for helping make this dashboard better and more inclusive.
