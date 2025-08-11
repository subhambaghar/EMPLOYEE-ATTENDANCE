import pandas as pd

path = "employee_attendance_july_2025_named.csv" #File Path

def employeedata():
    try:
        start = pd.to_datetime(input("Enter start data (YYYY-MM-DD): "))
        end = pd.to_datetime(input("Enter end date (YYYY-MM-DD): "))
        status = input("Enter status (All / Present / Absent / Leave): ").strip()

        dataframe = pd.read_csv(path)
        dataframe['Date'] = pd.to_datetime(dataframe['Date'])

        mask = (dataframe['Date'] >= start) & (dataframe['Date'] <= end)
        filterdata = dataframe.loc[mask] #To access rows by boolean values

        if status.lower() != "all":
            filterdata = filterdata[filterdata['Attendance_Status'].str.lower() == status.lower()]
            
        if filterdata.empty:
            print("\nNo data found for the given criteria.")
        else:
            print("\nFiletered Data: ")
            print(filterdata)
        return filterdata
    except Exception as e:
        print(f"Error while fetching data: {e}")
        return pd.DataFrame()
def exportToExcel(filterdata):
    if filterdata.empty:
        print("No data to print.")
        return
    try:
        filename = input("Enter the file name to save (e.g., output.xlsx): ").strip()
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"
        filterdata.to_excel(filename, index=False)
        print(f"File exported successfully to {filename}")
    except Exception as e:
        print(f"Export Failed: {e}")

if __name__ == "__main__":
    filterdata = employeedata()
    if not filterdata.empty:
        savechoice = input("Do you want to export the filtered data to Excel? (Y/N): ").strip().lower()
        if savechoice == "y":
            exportToExcel(filterdata)
