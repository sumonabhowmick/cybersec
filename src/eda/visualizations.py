"""Small Plotly chart helpers."""
import plotly.express as px

def distribution_chart(frame, column):
    counts = frame[column].fillna("Unknown").value_counts().rename_axis(column).reset_index(name="count")
    return px.bar(counts, x=column, y="count", title=f"Distribution of {column}")
