import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=Warning)

pd.set_option("display.max_rows", 100)

df = pd.read_excel("bank_data_clean.xlsx")

df.head()

# group by month and sum the quantities
df.groupby(by="month")["quantity"].sum()
expenses=df[df["quantity"]<0]
expenses["quantity"] = expenses["quantity"] * -1 #change of sign
expenses["day"] = expenses["date"].map(lambda x: x.day) #new column 'day'

exp_by_month = expenses.groupby(by="month")["quantity"].sum().reset_index()
expenses_by_day = expenses.groupby(by=["month", "day"])["quantity"].sum().reset_index() #group by day

# Overall month comparison
exp_by_month.plot(x="month", y="quantity", kind="bar", title="expenses by month")
plt.show()


months = exp_by_month["month"].unique().tolist()
for month in months: 
    # 1. filter data by month
    filtered_month = exp_by_month[exp_by_month["month"]==month]
    # 2. calculate total expenses
    monthly_exp  = filtered_month["quantity"].sum()
    # 3. Print result
    print(f"total expenses for month {month}: {monthly_exp} €")


def monthly_table(month_number: int, data: pd.DataFrame = expenses) -> pd.DataFrame:
    month_filter = data["month"] == month_number
    month_data = data[month_filter]
    return month_data

def monthly_graph(month_number: int):
    filter3 = expenses_by_day["month"] == month_number
    data = expenses_by_day[filter3]
    data.plot(x="day", y="quantity", kind = "bar", title="monthly expenses")
    plt.show()

# here just set number of month to see expense table and expense graph
monthly_table(1)
monthly_graph(1)
