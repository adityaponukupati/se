from flask import Flask, render_template, request
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
import math

app = Flask(__name__)

def perform_analysis(df):
    try:
        correlation_matrix = df.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.savefig('static/correlation_matrix.png')
        describe_info = df.describe().to_html()
        
        plt.figure(figsize=(8, 6))
        df.mean().plot(kind='bar', color='skyblue')
        plt.title('Mean Values of Columns')
        plt.xlabel('Columns')
        plt.ylabel('Mean Value')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/bar_chart.png')

        plt.figure(figsize=(8, 6))
        df.boxplot()
        plt.title('Box Plot of Columns')
        plt.xlabel('Columns')
        plt.ylabel('Values')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/box_plot.png')
        
        python_array = []
        arr = []
        arr_2 = []
        
        for i in df.describe():
            if df.describe()[i].dtype != "object":
                arr.append(df.describe()[i])
        
        for l in df.describe():
            arr_2.append(l)

        sno = [1, 4, 5, 6, 7]
        sna = ["Mean", "Standar Deviation", "25th Percentile", "50th Percentile", "75th Percentile", "Max"]
        for l, k in zip(range(0, len(arr)), arr_2):
            for i, j in zip(sno, sna):
                python_array.append("The "+ j+ " of "+ k+ " is "+ str(math.floor(arr[l][i])))

        python_array_2 = " ".join(python_array)
        return True, 'Analysis completed successfully', describe_info, python_array_2
    except Exception as e:
        return False, f'Error during analysis: {str(e)}', None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            uploaded_file = request.files['csvFile']
            df = pd.read_csv(uploaded_file)
            df = df.apply(pd.to_numeric, errors='coerce')
            success, message, describe_info, python_array = perform_analysis(df)

            if success:
                return render_template('result.html', correlation_matrix='correlation_matrix.png', bar_chart='bar_chart.png', box_plot='box_plot.png', describe_info=describe_info, python_array=python_array)
            else:
                return render_template('index.html', error_message=message)
        except Exception as e:
            return render_template('index.html', error_message=f'Error: {str(e)}')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
