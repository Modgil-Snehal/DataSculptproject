import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("EVIndia.csv")  # hypothetical filename

# Clean data
df.dropna(inplace=True)
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

# Basic exploration
print(df.info())
print(df.describe())

# Visualization
sns.lineplot(x='Year', y='EV_Sales', data=df)
plt.title("EV Sales Over Time in India")
plt.show()