import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Water Quality Dataset", page_icon="💧")
st.title("💧 Water Quality Dataset")
st.write(
    """
    This app visualizes data on water quality parameters. It shows various chemical parameters 
    present in water samples. Just click on the widgets below to explore!
    """
)

# Load the data from a CSV. We're caching this so it doesn't reload every time the app reruns.
@st.cache_data
def load_data():
    df = pd.read_csv("data/waterQuality1.csv")
    return df

df = load_data()

# Show a multiselect widget with the chemical parameters using `st.multiselect`.
parameters = st.multiselect(
    "Parameters",
    df.columns[3:],  # Exclude the first three columns (Tanggal, Periode, Lokasi)
    ["PH", "BOD (mg/L)", "COD (mg/L)", "TSS (mg/L)", "DO (mg/L)"]
)

# Show a slider widget with the rows (for demonstration purposes).
rows = st.slider("Rows", 1, len(df), (1, 10))

# Filter the dataframe based on the widget input.
df_filtered = df.iloc[rows[0]-1:rows[1], :]

# Display the data as a table using `st.dataframe`.
st.dataframe(df_filtered[parameters], use_container_width=True)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_filtered.reset_index(), id_vars="index", value_vars=parameters, var_name="parameter", value_name="value"
)
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("index:N", title="Sample Index"),
        y=alt.Y("value:Q", title="Parameter Value"),
        color="parameter:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
