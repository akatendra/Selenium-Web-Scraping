import seaborn as sns
import pandas as pd
import database
import matplotlib.pyplot as plt

data = database.get_item_count_per_day('kvartiry_vtorichka')
data2 = database.get_item_count_per_day2('kvartiry_vtorichka')
df = pd.DataFrame(data, columns=['Date', 'Count'])
df2 = pd.DataFrame(data2, columns=['Date'])
print(df)

# sns.relplot(data=df, x="Date", y="Count", kind="line", height=6, aspect=5)
# plt.figure(figsize=(15,15))
# plt.figure(figsize=(30,6))
# sns.histplot(df, x="Date", y="Count", kde=True) # Plot the density curve too

# sns.countplot(data=df, x="Date", y="Count")
sns.displot(data=df2, x="Date", height=6, aspect=4)
# Rotate x-labels
# plt.xticks(rotation=-45)
plt.show()
print()