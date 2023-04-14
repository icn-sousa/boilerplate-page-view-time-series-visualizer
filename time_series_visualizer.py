import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = 'date')

# Clean data
top = df['value'].quantile(0.025)
bottom = df['value'].quantile(0.975)

df = df[(df['value'] <= bottom) & (df['value'] >= top)]
df.index = pd.to_datetime(df.index, format="%Y-%m-%d")

def draw_line_plot():
    
    # Copy and modify data for line plot
    df_line_plot = df.copy()
    
    # Draw line plot
    date = df_line_plot.index
    page_views = df_line_plot.values
    
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(date, page_views, '-r')
    ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019');

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Months'] = df_bar.index.strftime('%B')
    df_bar['Years'] = df_bar.index.year
    df_bar = df_bar.groupby(['Months','Years']).mean().reset_index()
    
    # Draw bar plot
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    df_bar['Months'] = pd.Categorical(df_bar['Months'], categories=months, ordered=True)
    
    df_bar = df_bar.pivot(index='Years', columns='Months', values='value')
    
    fig, ax = plt.subplots()
    ax = df_bar.plot(kind='bar', ax=ax);
    ax.set(xlabel='Years', ylabel='Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15,5))
    
    left_plot = sns.boxplot(x=df_box['year'], y=df_box['value'], ax=ax1).set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    right_plot = sns.boxplot(x=df_box['month'], y=df_box['value'], order=months, ax=ax2).set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
