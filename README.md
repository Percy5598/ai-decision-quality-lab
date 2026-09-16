cat > README.md <<'EOF'
# AI Decision Quality Lab

A research-oriented project for studying **human decision-making with AI assistance**, with a focus on uncertainty, reliance, trust calibration, and decision quality.

## Project Goal

The project investigates how people make decisions when they receive different forms of AI assistance.

The current prototype compares:

- Human-only decisions
- AI point estimates
- AI estimates with uncertainty information

The long-term goal is to develop an experimental platform for studying **human–AI decision-making and decision quality**.

## Current Prototype

The application is built with:

- Python
- Streamlit
- Pandas
- Experimental decision-making components

The application presents decision scenarios, records decisions, and stores experimental data for later analysis.

## Streamlit App

The current live prototype is available here:

https://ai-decision-quality-lab-101.streamlit.app/ 

## Repository Structure

```text
ai-decision-quality-lab/
├── app/
│   ├── app.py
│   ├── pages/
│   └── components/
├── src/
│   ├── experiment/
│   ├── decisions/
│   ├── ai/
│   ├── analysis/
│   └── visualization/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── tests/
├── requirements.txt
└── README.md