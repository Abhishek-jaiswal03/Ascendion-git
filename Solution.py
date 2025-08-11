
import numpy as np 
import pandas as pd

# =========================
# File paths
# =========================
filepath_emp = "C:/Users/Ascendion/Desktop/Employee_attendance_Analysis/Data/employees.csv"
filepath_atten = "C:/Users/Ascendion/Desktop/Employee_attendance_Analysis/Data/attendence.csv"


# =========================
# Data Loading Functions
# =========================
def load_employees(file_path):
    df_employees = pd.read_csv(file_path)
    df_employees.columns = df_employees.columns.str.strip()
    print("\nEmployees Data (columns):", df_employees.columns.tolist())
    print(df_employees.head())
    return df_employees


def load_attendance(file_path):
    df_attendance = pd.read_csv(file_path)
    df_attendance.columns = df_attendance.columns.str.strip()
    print("\nAttendance Data (columns):", df_attendance.columns.tolist())
    print(df_attendance.head())
    return df_attendance


# =========================
# Merge Data
# =========================
def merge_employees_attendance(employees_df, attendance_df):
    if 'EmployeeID' not in employees_df.columns or 'EmployeeID' not in attendance_df.columns:
        raise ValueError("❌ 'EmployeeID' column missing from one of the DataFrames.")
    merged_df = pd.merge(employees_df, attendance_df, on='EmployeeID')
    print("\nMerged Data:")
    print(merged_df.head())
    return merged_df


# =========================
# Analysis Functions
# =========================
def total_hours_per_department(merged_df):
    return merged_df.groupby('Department')['HoursWorked'].sum().reset_index()


def attendance_rate(merged_df):
    merged_df['AttendanceRate'] = (merged_df['DaysPresent'] / merged_df['WorkingDays']) * 100
    return merged_df[['EmployeeID', 'Name', 'DaysPresent', 'WorkingDays', 'AttendanceRate']]


def hours_agg_per_employee(merged_df):
    return merged_df.groupby(['EmployeeID', 'Name'])['HoursWorked'].agg(['mean', 'max', 'min']).reset_index()


def avg_age_by_role(employees_df):
    return employees_df.groupby('JobRole')['Age'].mean().reset_index()


def total_attendance_entries(attendance_df):
    if 'EmployeeID' not in attendance_df.columns:
        raise ValueError(f"❌ 'EmployeeID' column not found. Columns: {attendance_df.columns.tolist()}")
    result = (
        attendance_df['EmployeeID']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'EmployeeID', 'EmployeeID': 'EntryCount'})
    )
    return result


def top_performers(merged_df):
    return merged_df.groupby(['EmployeeID', 'Name'])['HoursWorked'].sum().reset_index().sort_values('HoursWorked', ascending=False).head(3)


def avg_attendance_rate_per_department(merged_df):
    merged_df['AttendanceRate'] = (merged_df['DaysPresent'] / merged_df['WorkingDays']) * 100
    return merged_df.groupby('Department')['AttendanceRate'].mean().reset_index()


def late_arrival_ratio(merged_df):
    total_days = merged_df.groupby('EmployeeID').size()
    late_days = merged_df.groupby('EmployeeID')['Late'].sum()
    return (late_days / total_days).reset_index(name='LateArrivalRatio')


# =========================
# Run the Analysis
# =========================
df_employees = load_employees(filepath_emp)
df_attendance = load_attendance(filepath_atten)
merged_df = merge_employees_attendance(df_employees, df_attendance)

print("\nTotal Hours per Department:")
print(total_hours_per_department(merged_df))

print("\nAttendance Rate per Employee:")
print(attendance_rate(merged_df))

print("\nHours Aggregation per Employee:")
print(hours_agg_per_employee(merged_df))

print("\nAverage Age by Job Role:")
print(avg_age_by_role(df_employees))

print("\nTotal Attendance Entries:")
print(total_attendance_entries(df_attendance))

print("\nTop Performers:")
print(top_performers(merged_df))

print("\nAverage Attendance Rate per Department:")
print(avg_attendance_rate_per_department(merged_df))

print("\nLate Arrival Ratio per Employee:")
print(late_arrival_ratio(merged_df))

