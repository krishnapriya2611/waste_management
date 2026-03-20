import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

def add_waste():
    while True:
        while True:
            date = input("Date (dd/mm/yy): ")
            try:
                datetime.strptime(date, "%d/%m/%y")
                break
            except ValueError:
                print("Invalid date format. Use dd/mm/yy.")
        item = input("Item name: ")
        category = input("Plastic/Organic/Paper/Metal: ")
        weight = float(input("Weight in kg: "))

        new_entry = pd.DataFrame(
            [[date, item, category, weight]],
            columns=["Date", "Item", "Category", "Weight"]
        )

        if os.path.exists("waste_data.csv"):
            new_entry.to_csv("waste_data.csv", mode="a", header=False, index=False)
        else:
            new_entry.to_csv("waste_data.csv", index=False)

        print("Waste added successfully!\n")

        more = input("Add another entry? (continue/stop): ").lower()
        if more == "continue":
            return
        elif more=="stop":
            break
        else:
            print("enter from given options")

def suggest_reduction(category_totals):
    highest = category_totals.idxmax().lower()

    if highest == "plastic":
        return "Reduce single-use plastics. Use reusable bags and containers."
    elif highest == "organic":
        return "Start composting and avoid food waste."
    elif highest == "paper":
        return "Shift to digital notes and recycle paper."
    elif highest == "metal":
        return "Sell scrap metal to recycling centers."
    else:
        return "Follow general waste reduction practices."

while True:
    print("\nChoose:")
    print("1. Add Waste")
    print("2. Analyse Waste")
    print("3. Exit")

    choice = input("Enter 1/2/3: ")

    if choice == "1":
        add_waste()

    elif choice == "2":

        if not os.path.exists("waste_data.csv"):
            print("No data found. Add waste first.")
            continue

        df = pd.read_csv("waste_data.csv")

        df["Category"] = df["Category"].str.strip().str.capitalize()

        category_totals = df.groupby("Category")["Weight"].sum()

        print("\nTotal waste by category:")
        print(category_totals)

        print(f"\nMax wastage is of {category_totals.idxmax()}")

        print("\nSuggestion:")
        print(suggest_reduction(category_totals))

        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors='coerce')
        df["Week"] = df["Date"].dt.isocalendar().week
        weekly = df.groupby("Week")["Weight"].sum().sort_index()
        print("\nWeekly Waste:")
        print("\nWeekly Trends:")
        trend_labels=[]
        trend_values=[]
        weeks = list(weekly.index)
        if len(weekly) >= 2:
            for i in range(1, len(weeks)):
                if weeks[i] - weeks[i-1] == 1:
                    prev = weekly.iloc[i-1]
                    curr = weekly.iloc[i]
                    if prev != 0:
                        change = ((curr - prev) / prev) * 100

                        trend_labels.append(f'Week {weeks[i-1]} → Week {weeks[i]}')
                        trend_values.append(change)
        else:
           print("Not enough data for trend")

        colors=["red" if v>0 else "green" for v in trend_values]
        plt.figure()
        plt.barh(trend_labels,trend_values,color=colors)
        plt.xlabel("percentage change")
        plt.ylabel("weeks")
        plt.title("weekly change")

        for i in range(len(trend_values)):
            plt.text(trend_values[i],i,f"{trend_values[i]:.2f}")


        plt.figure()
        category_totals.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Waste Percentage")
        plt.ylabel("")

        import numpy as np
        from sklearn.linear_model import LinearRegression
        weeks = np.array(weekly.index).reshape(-1, 1)
        values = weekly.values

        model = LinearRegression()
        model.fit(weeks, values)

        next_week = np.array([[weeks[-1][0] + 1]])
        prediction = model.predict(next_week)
        prediction_value = weekly.tail(3).mean()

        print(f"\nPredicted waste for next week: {prediction_value:.2f} kg")

        plt.show()

    elif choice == "3":
        break

    else:
        print("Invalid choice.")
