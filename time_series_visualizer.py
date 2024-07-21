import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=True, index_col="date")


# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
    # Draw line plot

    plt.figure(figsize=(16,5))
    plt.plot(df.index, df['value'], ls="-", color="r")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    fig = plt.gcf()
    plt.close()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["Years"] = df_bar.index.year
    df_bar["Months"] = df_bar.index.month
    df_bar = df_bar.groupby(["Years", "Months"])["value"].mean().round().astype(int)
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig = df_bar.plot.bar(legend=True, figsize=(7,7), xlabel="Years", ylabel="Average Page Views").figure
    plt.legend(["January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December"])

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
    fig, axes = plt.subplots(1,2, figsize = (15,6))
    order_lst = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    p1 = sns.boxplot(data = df_box, x = 'year', y = 'value', hue = 'year', ax = axes[0], palette = "tab10", legend = False)
    p1.set(title = 'Year-wise Box Plot (Trend)', xlabel = 'Year', ylabel = 'Page Views')
    p2 = sns.boxplot(data = df_box, x = 'month', y = 'value', hue = 'month', order = order_lst, ax = axes[1])
    p2.set(title = 'Month-wise Box Plot (Seasonality)', xlabel = 'Month', ylabel = 'Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
