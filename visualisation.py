import seaborn as sb
import pandas as pd
import database
import matplotlib.pyplot as plt

data = database.get_item_count_per_day('kvartiry_vtorichka')
data2 = database.get_item_count_per_day2('kvartiry_vtorichka')
data3 = database.get_item_date_price_area('kvartiry_vtorichka')
data4 = database.get_item_date_price_area_average('kvartiry_vtorichka')


df = pd.DataFrame(data, columns=['Date', 'Count'])
df2 = pd.DataFrame(data2, columns=['Дата'])
df3 = pd.DataFrame(data3, columns=['Date', 'Price', 'Area'])
df3['Average price per square meter'] = df3['Price'] / df3['Area']

df4 = pd.DataFrame(data4, columns=['Дата', 'Средняя стоимость за м2, руб.'])

df2.sort_values(by=['Дата'],
                axis=0,
                inplace=True,
                ascending=True)

df3.sort_values(by=['Date'],
                axis=0,
                inplace=True,
                ascending=True)

df4.sort_values(by=['Дата'],
                axis=0,
                inplace=True,
                ascending=True)

print(df)
print(df2)
print(df3)
print(df4)

# Style of plot
sb.set_style("whitegrid",
             {"grid.color": ".6",
              "grid.linestyle": ":"
              })

plt.figure(figsize=(30, 6))  # width=30, #height=6

histogram = sb.histplot(data=df2,
            x="Дата")

# histogram = sb.histplot(data=df3,
#             x="Дата")

histogram.set(ylabel='Кол-во новых объявлений в день')
plt.show()
sb.relplot(data=df4, x="Дата", y='Средняя стоимость за м2, руб.', kind="line", height=6, aspect=5)
# sb.countplot(data=df2, x="Date")
# sb.displot(data=df2, x="Date", kde=False, height=6, aspect=4)
# sb.barplot(data=df2, x="Date", height=6, aspect=4)
# Rotate x-labels
# plt.xticks(rotation=-45)

plt.show()
