from django.shortcuts import render
import pandas as pd
from collections import defaultdict


# Helper function for file type validation
def validate_file_type(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(uploaded_file)
    else:
        return None

# Helper function for column validation
def validate_columns(df, required_columns):
    for col in required_columns:
        if col not in df.columns:
            return False
    return True

# Helper function for data aggregation
def aggregate_data(df):
    summary = defaultdict(lambda: defaultdict(int))
    for index, row in df.iterrows():
        cust_state = row['Cust State']
        cust_pin = row['Cust Pin']
        summary[cust_state][cust_pin] += 1
    
    # Create summary list for rendering
    summary_list = [{'Cust_State': state, 'Cust_Pin': pin, 'DPD': count} 
                    for state, pins in summary.items() 
                    for pin, count in pins.items()]
    return summary_list

def upload_file(request):
    """Handles file upload, validates file type, and generates a summary report."""
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        # Validate file type
        df = validate_file_type(uploaded_file)
        if df is None:
            return render(request, 'upload.html', {'error': 'Please upload a valid CSV or Excel file.'})

        # Validate required columns
        required_columns = ['Cust State', 'Cust Pin']
        if not validate_columns(df, required_columns):
            return render(request, 'upload.html', {'error': 'File must contain "Cust State" and "Cust Pin" columns.'})

        # Aggregate data
        summary_list = aggregate_data(df)

        # Render success page with summary data
        return render(request, 'success.html', {'summary': summary_list})

    # GET request - render the upload page
    return render(request, 'upload.html')
