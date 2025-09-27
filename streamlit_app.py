import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

# Page Title
st.set_page_config(page_title = "Employee Metrics Dashboard", layout = "wide")

# Load Date
def load_data():
    df = pd.read_csv("personnel.csv")
    df["Start Date"] = pd.to_datetime(df["Start Date"])
    df["Year"] = df["Start Date"].dt.year

    return df

df = load_data()

# Department Selection Dropdown
# st.sidebar.header("Select Departments to Visualize")
st.sidebar.header("Select Department(s)")
departments = df["Duty Description"].unique().tolist()

if "selected_departments" not in st.session_state:
    st.session_state.selected_departments = departments

select_all = st.sidebar.checkbox("Select All Departments", value=True if set(st.session_state.selected_departments) == set(departments) else False)

selected_departments = st.sidebar.multiselect("Choose departments:", departments, default=st.session_state.selected_departments)

if select_all:
    selected_departments = departments
else:
    if selected_departments == departments:
        selected_departments = []

# if "Select All" in selected_departments:
#     selected_departments = df["Duty Description"].unique().tolist()

# Filter Data Based on Year Selected
df_filtered = df[df["Duty Description"].isin(selected_departments)]

# Workforce Growth Trend
workforce_trend = df_filtered.groupby("Year")["Personnel ID"].count()

# Linear Regression Model
X = np.array(workforce_trend.index).reshape(-1,1)
Y = np.array(workforce_trend.values)

if len(X) > 1:
    model = LinearRegression()
    model.fit(X, Y)

    # Predict Future Years
    future_years = np.array(range(int(X[-1])+1, int(X[-1])+6)).reshape(-1,1)
    predictions = model.predict(future_years)

# Employee Distribution by Department
department_trend = df_filtered.groupby("Duty Description")["Personnel ID"].count()

# Layout with two columns
col1, col2, col3 = st.columns([2, 2, 1])

# Workforce Growth Visualization with Linear Regression
with col1:
    st.subheader("Workforce Growth Over Time")

    if len(X)>1:
        fig, ax = plt.subplots(figsize=(8,5))
        ax.scatter(X, Y, color="blue", label="Actual Data")
        ax.plot(X, model.predict(X), color="green", linestyle="--", label="Trend Line")
        ax.plot(future_years, predictions, color="red", linestyle="--", marker="o", label="Predicted Growth")

        for i, txt in enumerate(predictions):
            ax.annotate(f"{int(txt)}", (future_years[i], predictions[i]), textcoords="offset points", xytext=(0,5), ha="center")

        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Employees")
        ax.set_title("Workforce Growth Prediction")
        ax.legend()
        ax.grid()

        st.pyplot(fig)

    else:
        st.warning("Not enough data to perform linear regression.")

# Pie Chart displaying Distribution of Employees over the Departments
with col2:
    st.subheader("Employee Distribution By Department")

    if len(department_trend) > 0:
        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(
            department_trend.values, labels=None, autopct="%1.1f%%", startangle=90
        )
        st.pyplot(fig)
    
    else:
        st.warning("No department data available for the selected range.")

# Pie chart legend
with col3:
    st.subheader("Department Legend")

    if len(department_trend) > 0:
        for label, color in zip(department_trend.index, [w.get_facecolor() for w in wedges]):
            st.markdown(f"<span style='color:rgb({int(color[0]*255)}, {int(color[1]*225)}, {int(color[2]*225)})'> {label}</span>", unsafe_allow_html=True)

# Age Distribution
# st.subheader("Workforce Age Distribution")

# age_distribution = df_filtered["Age"].value_counts().sort_index()

# fig, ax = plt.subplots(figsize=(10, 5))
# ax.bar(age_distribution.index, age_distribution.values, color="skyblue")

# ax.set_xlabel("Age")
# ax.set_ylabel("Number of Employees")
# ax.set_title("Age Distribution of Workforce")
# ax.grid(axis="y", linestyle="--")

# st.pyplot(fig)

# Box and WHisker Plot for Age Distribution
st.subheader("Box and Whisker Plot for Age Distribution")

fig, ax = plt.subplots(figsize=(8,5))

boxplot_data = ax.boxplot(df_filtered["Age"], vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))

stats = df_filtered["Age"].describe()
min_value = stats["min"]
q1 = stats["25%"]
mean = stats["mean"]
q3 = stats["75%"]
max_value = stats["max"]

ax.text(min_value, 1, f"Min: {min_value}", ha="center", va="bottom", fontsize=10, color="black")
ax.text(q1, 1, f"Q1: {q1}", ha="center", va="bottom", fontsize=10, color="black")
ax.text(mean, 1.1, f"Average: {mean}", ha="center", va="bottom", fontsize=12, fontweight="bold", color="red")
ax.text(q3, 1, f"Q3: {q3}", ha="center", va="bottom", fontsize=10, color="black")
ax.text(max_value, 1, f"Max: {max_value}", ha="center", va="bottom", fontsize=10, color="black")

ax.set_xlabel("Age")
ax.set_title("Workforce Age Distribution (Box Plot)")

st.pyplot(fig)

# Employee Lookup Function
st.subheader("Employee Lookup")

search_name = st.text_input("Enter Employee First and Last Name (e.g., John Doe)")
search_id = st.text_input("Enter Personnel ID")

if search_name or search_id:

    # Filter both Name and Personnel ID
    if search_name and search_id:
        name_parts = search_name.strip().lower().split()
        if len(name_parts) == 2:
            first_name, last_name = name_parts
            search_results = df[
                (df["First Name"].str.lower() == first_name) &
                (df["Last Name"].str.lower() == last_name) &
                (df["Personnel ID"].astype(str) == search_id)
            ]

    # Filter by Name
    elif search_name:
        name_parts = search_name.strip().lower().split()
        if len(name_parts) == 2:
            first_name, last_name = name_parts
            search_results = df[
                (df["First Name"].str.lower() == first_name) &
                (df["Last Name"].str.lower() == last_name)    
            ]
        else:
            st.warning("Please enter both first and last names.")
            search_results = pd.DataFrame()
    
    # Filter by Personnel ID
    elif search_id:
        search_results = df[df["Personnel ID"].astype(str)  == search_id]

    if not search_results.empty:
        st.write("Search Results: (" + str(len(search_results)) + ")")
        st.dataframe(search_results)
    else:
        st.warning("No matching employee found...")


# Show Raw Data
st.subheader("Employee Records (Filtered)")
st.dataframe(df_filtered)