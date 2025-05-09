import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Student Appeal Dashboard", layout="wide")
st.title("📊 Student Appeal Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("Upload student data CSV", type="csv")

# Define custom colors for grade levels
grade_colors = {
    9: "#1f77b4",   # blue
    10: "#ff7f0e",  # green
    11: "#2ca02c",  # orange
    12: "#d62728"   # red
}

# Display name mapping
display_names = {
    "Math PSAT9F": "PSAT 9 (Fall)",
    "Math PSAT9S": "PSAT 9 (Spring)",
    "Math PSAT10F": "PSAT 10 (Fall)",
    "Math PSAT10S": "PSAT 10 (Spring)",
    "Math PSAT11F": "PSAT 11 (Fall)",
    "Cum GPA": "Cumulative GPA",
    "Fab 5 GPA": "Fab 5 GPA"
}

# Function to get axis limits from full dataset
def get_axis_limits(df, x_field, y_field, padding_x=20, padding_y=0.2):
    df[x_field] = pd.to_numeric(df[x_field], errors="coerce")
    df[y_field] = pd.to_numeric(df[y_field], errors="coerce")
    x_min = df[x_field].min()
    x_max = df[x_field].max()
    y_min = df[y_field].min()
    y_max = df[y_field].max()
    return [x_min - padding_x, x_max + padding_x], [y_min - padding_y, y_max + padding_y]

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Preprocessing
    df["Grade Level"] = df["Grade Level"].astype(str)
    df["Class Desired"] = df['I do not meet the grade prerequisite for'].astype(str)
    df['Full Name'] = df['Last Name'] + ", " + df['First Name']

    st.sidebar.header("Filter Options")

    # Dropdown options for x and y
    x_options = ["Math PSAT9F", "Math PSAT9S", "Math PSAT10F", "Math PSAT10S", "Math PSAT11F"]
    y_options = ["Cum GPA", "Fab 5 GPA"]

    x_field = st.sidebar.selectbox("X-Axis", x_options, index=0)
    y_field = st.sidebar.selectbox("Y-Axis", y_options, index=1)

    # Grade filter
    all_grades = sorted(df["Grade Level"].unique())
    selected_grades = st.sidebar.radio("Select Grade Level", options=["All"] + all_grades, index=0)

    # Desired course filter
    all_courses = sorted(df["Class Desired"].unique())
    selected_courses = st.sidebar.radio("Select Desired Course", options=["All"] + all_courses, index=0)

    # Apply filters
    filtered_df = df.copy()
    if selected_grades != "All":
        filtered_df = filtered_df[filtered_df["Grade Level"] == selected_grades]
    if selected_courses != "All":
        filtered_df = filtered_df[filtered_df["Class Desired"] == selected_courses]

    # Compute axis limits from full dataset
    x_range, y_range = get_axis_limits(df, x_field, y_field)

    # Check for required columns
    required_cols = {
        'First Name', 'Last Name', 'Grade Level', 'I do not meet the grade prerequisite for',
        'Department Notes', 'Cum GPA', 'Fab 5 GPA',
        'Math PSAT9F', 'Math PSAT9S', 'Math PSAT10F', 'Math PSAT10S', 'Math PSAT11F'
    }
    # Mapping from grade number to label
    grade_labels = {
        "9": "freshmen",
        "10": "sophomores",
        "11": "juniors",
        "12": "seniors"
    }

    # Count students per grade
    grade_counts = filtered_df["Grade Level"].value_counts().sort_index()

    # Format breakdown
    breakdown = ", ".join(
        f"{grade_counts.get(grade, 0)} {label}"
        for grade, label in grade_labels.items()
        if grade in grade_counts
    )

    plot_title = f"{display_names.get(x_field, x_field)} vs {display_names.get(y_field, y_field)} \n"
    plot_title += f"(\n{len(filtered_df)} total students: {breakdown})"
    filtered_df[x_field] = pd.to_numeric(filtered_df[x_field], errors="coerce")
    filtered_df[y_field] = pd.to_numeric(filtered_df[y_field], errors="coerce")
    filtered_df = filtered_df.dropna(subset=[x_field, y_field])

    if not required_cols.issubset(df.columns):
        st.error(f"CSV is missing required columns: {required_cols - set(df.columns)}")

    else:
        # Plot
        fig = px.scatter(
            filtered_df,
            x=x_field,
            y=y_field,
            color="Grade Level",
            color_discrete_map={str(k): v for k, v in grade_colors.items()},
            hover_name="Full Name",
            # hover_data=["Class Desired", "and have registered for", "Department Notes"],
            title=plot_title,
            width=700,
            height=700,
            range_x=x_range,
            range_y=y_range
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Filtered Data Table")
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Please upload a CSV file to get started.")
