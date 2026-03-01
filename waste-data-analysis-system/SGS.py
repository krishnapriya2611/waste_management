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
\
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
        
        plt.figure()
        category_totals.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Waste Percentage")
        plt.ylabel("")

        plt.show()

    elif choice == "3":
        break

    else:
        print("Invalid choice.")