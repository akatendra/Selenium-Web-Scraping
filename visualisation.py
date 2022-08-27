import seaborn as sb
import pandas as pd
import database
import matplotlib.pyplot as plt

import logging.config


def cm_to_inch(value):
    return value / 2.54


def show_bar_values(obj):
    for ax in obj.axes.ravel():
        # add annotations
        for bar_container in ax.containers:
            labels = [bar.get_height() for bar in bar_container]
            ax.bar_label(bar_container,
                         labels=labels,
                         label_type='edge',
                         fontsize=20,
                         # rotation=90,
                         padding=2)
        ax.margins(y=0.2)

# Set up logging
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
# Remove matplotlib.font_manager from logging
# logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
# Remove all matplotlib from logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

# Style of plot
sb.set_style("whitegrid",
             {"grid.color": ".6",
              "grid.linestyle": ":"
              })

# Количество новых объявлений по дням
data2 = database.get_item_count_per_day2('kvartiry_vtorichka')
df2 = pd.DataFrame(data2, columns=['Дата'])
df2.sort_values(by=['Дата'],
                axis=0,
                inplace=True,
                ascending=True)
print(df2)
histogram = sb.displot(data=df2,
                       x="Дата",
                       kind='hist',
                       height=6,
                       aspect=5)
histogram.set(ylabel='Кол-во новых объявлений в день')
histogram.set(title='Кол-во новых объявлений по дням')

show_bar_values(histogram)
# Fix problem seaborn function 'displot' does not show up a part of the title
# https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
plt.tight_layout()

plt.show()

# Средняя стоимость квадратного метра по дням
data4 = database.get_item_date_price_area_average('kvartiry_vtorichka')
df4 = pd.DataFrame(data4, columns=['Дата', 'Средняя стоимость за м2, руб.'])
df4.sort_values(by=['Дата'],
                axis=0,
                inplace=True,
                ascending=True)
print(df4)
ax = sb.relplot(data=df4, x="Дата", y='Средняя стоимость за м2, руб.',
                kind="line", height=6, aspect=5)
ax.set(title='Средняя стоимость за м2, руб. по дням')
for x, y in zip(df4['Дата'], df4['Средняя стоимость за м2, руб.']):
    # the position of the data label relative to the data point can be adjusted by adding/subtracting a value from the x &/ y coordinates
    plt.text(x=x,  # x-coordinate position of data label
             y=y + 150,
             # y-coordinate position of data label, adjusted to be 150 below the data point
             s='{:.0f}'.format(y),  # data label, formatted to ignore decimals
             color='purple')  # set colour of line

    # add set_backgroundcolor('color') after plt.text('…')
    plt.text(x, y - 150, '{:.0f}'.format(y), color='white').set_backgroundcolor(
        '#1f77b4')
# Fix problem seaborn function 'displot' does not show up a part of the title
# https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
plt.tight_layout()
plt.show()

# Количество новых объявлений по городам из ТОП10 ГОРОДОВ по количеству объявлений
data5 = database.get_top10_cities('kvartiry_vtorichka')
order_vector = data5[0]
print('order_vector', order_vector)
df5 = pd.DataFrame(data5[1], columns=['Города'])
df5['Города'] = pd.Categorical(df5['Города'], categories=order_vector)
print(df5)

histogram_city = sb.displot(data=df5,
                            x='Города',
                            kind='hist',
                            height=6,
                            aspect=5
                            )
histogram_city.set(ylabel='Кол-во объявлений за все время')
histogram_city.set(
    title='Количество новых объявлений по городам из ТОП10 ГОРОДОВ по количеству объявлений')

# sb.set(rc={"figure.figsize": (30, 6)}) #width=30, #height=6
show_bar_values(histogram_city)
# Fix problem seaborn function 'displot' does not show up a part of the title
# https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
plt.tight_layout()
plt.show()

# Количество новых объявлений по Севастополю по дням
data6 = database.get_item_count_sevastopol_simple('kvartiry_vtorichka')
df6 = pd.DataFrame(data6, columns=['Дата'])
df6.sort_values(by=['Дата'],
                axis=0,
                inplace=True,
                ascending=True)

print(df6)

histogram_sevastopol = sb.displot(data=df6,
                                  x='Дата',
                                  kind='hist',
                                  height=6,
                                  aspect=5
                                  )
histogram_sevastopol.set(ylabel='Кол-во объявлений')
histogram_sevastopol.set(
    title='Количество новых объявлений по Севастополю по дням')

show_bar_values(histogram_sevastopol)

# Fix problem seaborn function 'displot' does not show up a part of the title
# https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
plt.tight_layout()
plt.show()
