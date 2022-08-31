import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# load dataset
flights = sb.load_dataset('flights')
flights.head()

# set up flights by year dataframe
year_flights = flights.groupby('year').sum().reset_index()
print(year_flights)

# set up average number of passengers by month dataframe
month_flights = flights.groupby('month').agg(
    {'passengers': 'mean'}).reset_index()
print(month_flights)

# plot line graph
sb.set(rc={'figure.figsize': (10, 5)})
ax = sb.lineplot(x='year',
                  y='passengers',
                  data=year_flights,
                  marker='*',
                  color='#965786')
ax.set(title='Total Number of Passengers Yearly')
# label points on the plot
for x, y in zip(year_flights['year'], year_flights['passengers']):
    # the position of the data label relative to the data point can be adjusted by adding/subtracting a value from the x &/ y coordinates
    plt.text(x=x,  # x-coordinate position of data label
             y=y - 150,
             # y-coordinate position of data label, adjusted to be 150 below the data point
             s='{:.0f}'.format(y),  # data label, formatted to ignore decimals
             color='purple')  # set colour of line

    # add set_backgroundcolor('color') after plt.text('…')
    plt.text(x, y - 150, '{:.0f}'.format(y), color='white').set_backgroundcolor(
        '#965786')
plt.show()

# plot histogram
ax = sb.distplot(flights['passengers'], color='#9d94ba', bins=10, kde=False)
ax.set(title='Distribution of Passengers')
# label each bar in histogram
for p in ax.patches:
    height = p.get_height()  # get the height of each bar
    # adding text to each bar
    ax.text(x=p.get_x() + (p.get_width() / 2),
            # x-coordinate position of data label, padded to be in the middle of the bar
            y=height + 0.2,
            # y-coordinate position of data label, padded 0.2 above bar
            s='{: .0f}'.format(height),  # data label, formatted to ignore decimals
            ha='center')  # sets horizontal alignment (ha) to center
plt.show()
