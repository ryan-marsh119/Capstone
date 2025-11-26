# Employee Metrics Dashboard📊

A simple web-based dashboard built with Streamlit for viewing high-level workforce metrics, such as employee growth trends, department distribution, and age statistics. It also includes basic employee search and the ability to add new employees. This project uses sample data from a CSV file to demonstrate data loading, filtering, visualization, and form-based data entry. It's designed as a portfolio piece to showcase basic data handling and UI development skills in Python.

## Description

This dashboard provides an overview of an organization's workforce:
- Visualizes employee growth over time with a linear regression model for predicting future trends.
- Shows employee distribution by department using a pie chart.
- Displays age distribution with a box-and-whisker plot.
- Allows searching for employees by name or ID.
- Enables adding new employees via a form, which appends data to the CSV file.
- Filters data by selected departments using a sidebar multiselect.

The app loads data from `personnel_updated.csv`, processes it with Pandas, and generates plots using Matplotlib and Scikit-learn for the regression model. It's meant for quick insights into workforce trends to help with hiring planning.

Note: This is a basic prototype using a CSV file for persistence, not a production-ready database. Data additions are appended to the file, but there's no update or delete functionality.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ryan-marsh119/Capstone.git
   cd Capstone
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the app locally:
```
streamlit run streamlit_app.py
```

- Open your browser to the provided URL (usually http://localhost:8501).
- Use the sidebar to select departments for filtering.
- View the visualizations for trends and distributions.
- Use the "Employee Lookup" section to search by name or ID.
- Expand the "Add Employee" section to submit a new employee's details.

## Features

- **Department Filtering**: Multiselect dropdown in the sidebar to filter data by department, with a "Select All" checkbox.
- **Workforce Growth Trend**: Line chart showing employee count by year, with a linear regression line and 5-year predictions.
- **Department Distribution**: Pie chart showing the percentage of employees per department, with a separate legend.
- **Age Distribution**: Box-and-whisker plot highlighting min, Q1, mean, Q3, and max ages.
- **Employee Search**: Text inputs for name (first and last) or personnel ID, displaying matching results in a table.
- **Add Employee**: Form to input new employee details, generating a unique ID and appending to the CSV file.
- **Raw Data Table**: Displays the filtered employee records.

## Technologies Used

- **Python 3**: Core language.
- **Streamlit**: For the web interface and interactive elements.
- **Pandas**: Data loading, filtering, and manipulation.
- **Matplotlib**: Generating charts (line, pie, box plot).
- **Scikit-learn**: Linear regression for growth predictions.
- **UUID**: For generating unique employee IDs.
- Other libraries as listed in `requirements.txt` (e.g., NumPy for arrays).

## Project Structure

- `streamlit_app.py`: Main app file handling UI layout, filters, and integration.
- `utils.py`: Helper functions for loading data, filtering by department, and adding new employees.
- `visuals.py`: Functions for generating and displaying charts.
- `employee_lookup.py`: Function for searching employees.
- `personnel_updated.csv`: Sample dataset with employee records.
- `requirements.txt`: List of dependencies.

## Limitations

- Data is stored in a CSV file, so it's not suitable for concurrent users or large-scale data.
- Predictions are based on simple linear regression and assume historical trends continue.
- No authentication or data validation beyond basic form checks.
- The app is designed for local use; deployment (e.g., to Streamlit Cloud) would require additional setup.

## License

This project is licensed under the **Apache License 2.0**.

You can view the full license text here: [LICENSE](LICENSE)  
or visit http://www.apache.org/licenses/LICENSE-2.0
