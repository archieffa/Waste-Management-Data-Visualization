from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import numpy as np

app = Flask(__name__)

def load_data():
    df = pd.read_excel('dataset.xlsx')
    df = df[['Year', 'Province', 'Annual Waste']]
    
    # Convert columns to appropriate data types
    df['Year'] = df['Year'].astype(int)
    df['Province'] = df['Province'].astype(str)
    df['Annual Waste'] = df['Annual Waste'].astype(float)

    # Handle missing values (if any)
    df = df.dropna()
    
    return df

data = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/total-annual-waste')
def total_annual_waste():
    # Process data for total annual waste generation in each province each year
    total_waste = data.groupby(['Year', 'Province'])['Annual Waste'].sum().reset_index()
    fig = px.line(total_waste, x='Year', y='Annual Waste', color='Province', title='Total Annual Waste Generation by Province')
    graph = fig.to_html(full_html=False)
    return render_template('graph.html', graph=graph)

@app.route('/average-annual-waste')
def average_annual_waste():
    # Process data for average annual waste generation
    avg_waste = data.groupby('Province')['Annual Waste'].mean().reset_index()
    fig = px.bar(avg_waste, x='Province', y='Annual Waste', title='Average Annual Waste Generation by Province')
    graph = fig.to_html(full_html=False)
    return render_template('graph.html', graph=graph)

@app.route('/waste-categorization')
def waste_categorization():
    # Categorize provinces based on average waste generation
    avg_waste = data.groupby('Province')['Annual Waste'].mean().reset_index()
    conditions = [
        (avg_waste['Annual Waste'] <= 100000),
        (avg_waste['Annual Waste'] > 100000) & (avg_waste['Annual Waste'] <= 700000),
        (avg_waste['Annual Waste'] > 700000)
    ]
    categories = ['Green', 'Orange', 'Red']
    avg_waste['Category'] = np.select(conditions, categories)

    # Assign colors based on categories
    color_discrete_map = {
        'Green': 'green',
        'Orange': 'orange',
        'Red': 'red'
    }

    fig = px.bar(avg_waste, x='Province', y='Annual Waste', color='Category', 
                 title='Annual Waste Categorization by Province', 
                 color_discrete_map=color_discrete_map)
    
    graph = fig.to_html(full_html=False)
    return render_template('graph.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
