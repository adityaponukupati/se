from flask import Flask, render_template, request
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['csvFile']

        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Perform statistical analysis (example: correlation matrix)
        correlation_matrix = df.corr()

        # Save the correlation matrix plot as an image
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.savefig('static/correlation_matrix.png')

        # Render the analysis result page
        return render_template('result.html', correlation_matrix='correlation_matrix.png')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
