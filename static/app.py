from flask import Flask, render_template, request
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

def perform_analysis(df):
    try:
        # Perform statistical analysis (example: correlation matrix)
        correlation_matrix = df.corr()

        # Save the correlation matrix plot as an image
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.savefig('static/correlation_matrix.png')

        return True, 'Analysis completed successfully'
    except Exception as e:
        return False, f'Error during analysis: {str(e)}'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get the uploaded file
            uploaded_file = request.files['csvFile']

            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(uploaded_file)
            df = df.dropna()
            # Perform data cleaning (replace non-numeric values with NaN)
            df = df.apply(pd.to_numeric, errors='coerce')

            # Call the function for statistical analysis
            success, message = perform_analysis(df)

            if success:
                return render_template('result.html', correlation_matrix='correlation_matrix.png')
            else:
                return render_template('index.html', error_message=message)
        except Exception as e:
            return render_template('index.html', error_message=f'Error: {str(e)}')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
