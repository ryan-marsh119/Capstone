import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def workforce_growth(df_filtered):
     # Workforce Growth Trend
    workforce_trend = df_filtered.groupby("Year")["PID"].count()

    # Linear Regression Model
    X = np.array(workforce_trend.index).reshape(-1,1)
    Y = np.array(workforce_trend.values)

    if len(X) > 1:
        model = LinearRegression()
        model.fit(X, Y)

        # Predict Future Years
        future_years = np.array(range(int(X[-1])+1, int(X[-1])+6)).reshape(-1,1)
        predictions = model.predict(future_years)


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

def pie(df_filtered):
    # Employee Distribution by Department
    department_trend = df_filtered.groupby("Department")["PID"].count()

    if len(department_trend) > 0:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                department_trend.values, labels=None, autopct="%1.1f%%", startangle=90
            )
            st.pyplot(fig)
        
    else:
        st.warning("No department data available for the selected range.")

def pie_legend(df_filtered):
    department_trend = df_filtered.groupby("Department")["PID"].count()

    if len(department_trend) > 0:
        _, ax = plt.subplots(figsize= (6, 6))
        wedges, _, _ = ax.pie(
             department_trend.values, labels=None, autopct="%1.1f%%", startangle=90
        )    

        for label, color in zip(department_trend.index, [w.get_facecolor() for w in wedges]):
            st.markdown(f"<span style='color:rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)})'> {label}</span>", unsafe_allow_html=True)

def box_and_whisker(df_filtered):
    fig, ax = plt.subplots(figsize=(8,5))

    ax.boxplot(df_filtered["Age"], vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))

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