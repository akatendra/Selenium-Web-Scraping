from datetime import datetime

import seaborn as sb
import pandas as pd
import database
import matplotlib.pyplot as plt

import logging.config


def cm_to_inch(value):
    return value / 2.54

def px_to_inch(px, dpi=72):
    return px / dpi


def show_bar_values(obj):
    for ax in obj.axes.ravel():
        # add annotations
        for bar_container in ax.containers:
            labels = [bar.get_height() for bar in bar_container]
            ax.bar_label(bar_container,
                         labels=labels,
                         label_type='edge',
                         fontsize=16,
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

output_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# Plot style
sb.set_style("whitegrid",
             {"grid.color": ".6",
              "grid.linestyle": ":"
              })

# 1. Количество новых объявлений по дням
data1 = database.get_item_count_per_day2('kvartiry_vtorichka')
df1 = pd.DataFrame(data1, columns=['Дата'])
df1.sort_values(by=['Дата'],
                axis=0,
                inplace=True,
                ascending=True)
print(df1)
histogram = sb.displot(data=df1,
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

# 2. Средняя стоимость квадратного метра по дням
data2 = database.get_item_date_price_area_average_union()
df2 = pd.DataFrame(data2, columns=['Дата', 'Средняя стоимость за м2, руб.',
                                   'Тип недвижимости'])
print(df2)
# df2.sort_values(by=['Дата'],
#                 axis=0,
#                 inplace=True,
#                 ascending=True)
# print(df2)
av_price = sb.relplot(data=df2,
                      x="Дата",
                      y='Средняя стоимость за м2, руб.',
                      kind="line",
                      hue='Тип недвижимости',
                      height=6,
                      aspect=5)
av_price.set(title='Средняя стоимость квартир за м2, руб. по дням')

# Shift legend to another position
# https://stackoverflow.com/questions/39803385/what-does-a-4-element-tuple-argument-for-bbox-to-anchor-mean-in-matplotlib/39806180#39806180
legend = av_price._legend
legend.set_bbox_to_anchor([1, 0.9])
#  Add annotations with average price
for x, y, item_type in zip(df2['Дата'], df2['Средняя стоимость за м2, руб.'],
                           df2['Тип недвижимости']):
    # the position of the data label relative to the data point can be
    # adjusted by adding/subtracting a value from the x / y coordinates

    # Simple text
    # plt.text(x=x,  # x-coordinate position of data label
    #          # y-coordinate position of data label, adjusted to be 150 below the data point
    #          y=y + 150,
    #          s='{:.0f}'.format(y),  # data label, formatted to ignore decimals
    #          color='#1f77b4')  # set colour of line

    # text with background
    if item_type == 'квартиры-вторичка':
        plt.text(x, y - 150, '{:.0f}'.format(y),
                 color='white').set_backgroundcolor(
            '#1f77b4')
    else:
        plt.text(x, y - 150, '{:.0f}'.format(y),
                 color='white').set_backgroundcolor(
            '#ff7f0e')

# Fix problem seaborn function 'displot' does not show up a part of the title
# https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
plt.tight_layout()
# 2.1 Средняя стоимость квадратного метра по дням квартир новострой

plt.show()

# 3. Количество новых объявлений по городам из ТОП10 ГОРОДОВ по количеству объявлений
data3 = database.get_top10_cities('kvartiry_vtorichka')
order_vector = data3[0]
print('order_vector', order_vector)
df3 = pd.DataFrame(data3[1], columns=['Города'])
df3['Города'] = pd.Categorical(df3['Города'], categories=order_vector)
print(df3)

histogram_city = sb.displot(data=df3,
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

# 4. Количество новых объявлений по Севастополю по дням
data4 = database.get_item_count_sevastopol_simple('kvartiry_vtorichka')
df4 = pd.DataFrame(data4, columns=['Дата'])
df4.sort_values(by=['Дата'],
                axis=0,
                inplace=True,
                ascending=True)

print(df4)

histogram_sevastopol = sb.displot(data=df4,
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
fig = plt.gcf()
fig.savefig(f'image_out/histogram_sevastopol_{output_timestamp}.png', format='png', dpi=72)
plt.show()

