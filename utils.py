import pandas as pd
import uuid

# Read data from CSV to be returned. Parsing out year from start date.
def load_data():
    df = pd.read_csv("personnel_updated.csv")
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], format="%Y-%m-%d")
    df["Year"] = df["Start_Date"].dt.year
    df["Start_Date"] = df["Start_Date"].dt.date

    return df

# Helper function used to display only the selected departments in visuals.
def select_dept(data, departments):
    data_filtered = data[data["Department"].isin(departments)]

    return data_filtered

# Add employee to the database via the form from streamlit_app.py. new_id generated via uuid4() function.
def add_data(employee_data):    
    df = pd.read_csv('personnel_updated.csv')
    
    new_id = str(uuid.uuid4())
    new_index = len(df)

    data = {    '': new_index,
                'PID': new_id,
                'First_Name': employee_data['First_Name'],
                'Last_Name': employee_data['Last_Name'], 
                'Gender': employee_data['Gender'], 
                'Age': employee_data['Age'], 
                'Department': employee_data['Department'], 
                'Location': employee_data['Location'], 
                'Employee_Status': employee_data['Employee_Status'], 
                'Pay_Grade': employee_data['Pay_Grade'], 
                'Start_Date': employee_data['Start_Date']
    }

    new_row = pd.DataFrame([data])

    new_row.to_csv('personnel_updated.csv', mode='a', index=False, header=False)
    
    return load_data()