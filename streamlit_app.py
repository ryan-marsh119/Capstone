import streamlit as st
import pandas as pd  
from utils import load_data, select_dept, add_data
from employee_lookup import search_employees
from visuals import workforce_growth, pie, pie_legend, box_and_whisker

# Page Title
st.set_page_config(page_title = "Employee Metrics Dashboard", layout = "wide")

try:
    df = load_data()

    # Department Selection Dropdown
    st.sidebar.header("Select Department(s)")
    departments = df["Department"].unique().tolist()
    locations = df["Location"].unique().tolist()
    paygrades = df["Pay_Grade"].unique().tolist()

    if "selected_departments" not in st.session_state:
        st.session_state["selected_departments"] = departments

    if "checked_all" not in st.session_state:
        st.session_state["checked_all"] = True

    # Functions below are for the multiselect option when selecting departments to analyze.
    def handle_checkbox():
        if st.session_state["checked_all"]:
            st.session_state["selected_departments"] = departments

        else:
            st.session_state["selected_departments"] = []

    def handle_multiselect():
        st.session_state["checked_all"] = set(st.session_state["selected_departments"]) == set(departments)

    st.sidebar.multiselect(
        label="Select a Department",
        options=departments,
        key="selected_departments",
        on_change=handle_multiselect
    )

    st.sidebar.checkbox(
        label="Select All",
        key="checked_all",
        on_change=handle_checkbox
    )
     
    # Filter Data Based on Year Selected
    df_filtered = select_dept(df, st.session_state['selected_departments'])

    # Layout with two columns
    col1, col2, col3 = st.columns([2, 2, 1])

    # Workforce Growth Visualization with Linear Regression
    with col1:
        st.subheader("Workforce Growth Over Time")

        workforce_growth(df_filtered)

    # Pie Chart displaying Distribution of Employees over the Departments
    with col2:
        st.subheader("Employee Distribution By Department")

        pie(df_filtered)

    # Pie chart legend
    with col3:
        st.subheader("Department Legend")

        pie_legend(df_filtered)

    # Box and WHisker Plot for Age Distribution
    st.subheader("Box and Whisker Plot for Age Distribution")

    box_and_whisker(df_filtered)

    # Employee Lookup Function
    st.subheader("Employee Lookup")

    search_employees(df)

    # Show Raw Data
    st.subheader("Employee Records (Filtered)")
    employee_table = st.dataframe(df_filtered, hide_index=True)

    # add_employee = st.button(label="Add Employee")

    # if add_employee:
    with st.expander("Add Employee"):
        with st.form(key="add_employee_form", clear_on_submit=True, enter_to_submit=False):
            # Store form entries into values
            employee_form = {
                'First_Name': None,
                'Last_Name': None,
                'Gender': None,
                'Age': None,
                'Department': None,
                'Location': None,
                'Employee_Status': None,
                'Pay_Grade': None,
                'Start_Date': None
            }

            # Form to add new employee to the database.
            st.write("Enter the new employee's information below:")

            employee_form['First_Name'] = st.text_input("First Name")
            employee_form['Last_Name'] = st.text_input("Last Name")
            employee_form['Gender'] = st.selectbox("Gender", ['Male', 'Female', 'Unknown'])
            employee_form['Age'] = st.number_input("Age", format='%i')
            employee_form['Department'] = st.selectbox("Department", departments)
            employee_form['Location'] = st.selectbox("Location", locations)
            employee_form['Employee_Status'] = st.selectbox("Employee Status", [1, 2, 3, 4])
            employee_form['Pay_Grade'] = st.selectbox("Paygrade", paygrades)
            employee_form['Start_Date'] = st.date_input("Start Date", format="YYYY/MM/DD")

            submit_button = st.form_submit_button(label="Submit")
            
            if submit_button:
                print("Submit button hit")
                if not all(employee_form.values()):
                    st.warning("Please fill in all information for the new employee.")

                else:
                    df = add_data(employee_form)
                    df_filtered = select_dept(df, st.session_state['selected_departments'])
                    st.success("Employee added successfully!")

except pd.errors.EmptyDataError:
    st.subheader("No employees! Time to hire!")

except FileNotFoundError:
    st.subheader("No employees! Time to hire!")