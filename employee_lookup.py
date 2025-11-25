import streamlit as st
import pandas as pd

def search_employees(df):

    search_name = st.text_input("Enter Employee First and Last Name (e.g., John Doe)")
    search_id = st.text_input("Enter Personnel ID")

    if search_name or search_id:

        # Filter both Name and Personnel ID
        if search_name and search_id:
            name_parts = search_name.strip().lower().split()
            if len(name_parts) == 2:
                first_name, last_name = name_parts
                search_results = df[
                    (df["First_Name"].str.lower() == first_name) &
                    (df["Last_Name"].str.lower() == last_name) &
                    (df["PID"].astype(str) == search_id)
                ]
            
            else:
                st.warning("Please enter both first and last names.")
                search_results = pd.DataFrame()

        # Filter by Name
        elif search_name:
            name_parts = search_name.strip().lower().split()
            if len(name_parts) == 2:
                first_name, last_name = name_parts
                search_results = df[
                    (df["First_Name"].str.lower() == first_name) &
                    (df["Last_Name"].str.lower() == last_name)    
                ]
            else:
                st.warning("Please enter both first and last names.")
                search_results = pd.DataFrame()
        
        # Filter by Personnel ID
        elif search_id:
            search_results = df[df["PID"].astype(str)  == search_id]

        if not search_results.empty:
            st.write("Search Results: (" + str(len(search_results)) + ")")
            st.dataframe(search_results)
        else:
            st.warning("No matching employee found...")