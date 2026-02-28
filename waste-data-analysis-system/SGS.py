import pandas as pd
import os

def add_waste():
    date=input("date in (dd/mm/yy):")
    items=input("item name:")
    category=input("plastic/organic/paper/metal:")
    weight=float(input("weight in kg:"))
    
    new_entry=pd.DataFrame([[date,items,category,weight]],columns=["Date","Items","Category","Weight"])
    if os.path.exists("waste_data.csv"):
        new_entry.to_csv("waste_data.csv",mode="a",header=False,index=False)
    else:
        new_entry.to_csv("waste_data.csv",header=False)
print("waste added\n")

print("choose:\n1.add waste\n2.analyse waste\n3.exit")
choice=int(input("1/2/3:"))
if choice==1:
    add_waste()
elif choice==2:
    df=pd.read_csv("waste_data.csv")
    category_totals=df.groupby("Category")["weight"].sum()
    print("total waste by category:",category_totals)
    print(f"max wastage is of {category_totals.idxmax()}")

    import matplotlib.pyplot as plt
    plt.figure()
    category_totals.plot(kind="bar")
    plt.title("wastage graph")
    plt.xlabel("category")
    plt.ylabel("weight(kg)")
    plt.figure()
    category_totals.plot(kind="pie",autopct="%1.1f%%")
    plt.title("wastage percentage")
    plt.ylabel("")
    plt.show()

    def suggest_reduction(category_totals):
        highest = category_totals.idxmax()

        if highest == "Plastic":
            return "Reduce single-use plastics. Use reusable bags and containers."
        elif highest == "Organic":
            return "Start composting and avoid food waste."
        elif highest == "Paper":
            return "Shift to digital notes and recycle paper."
        elif highest == "Metal":
            return "Sell scrap metal to recycling centers."
        else:
            return "Follow general waste reduction practices."

    print("\nSuggestion:")
    print(suggest_reduction(category_totals))
elif choice==3:
    exit()
else:
    print("invalid choice")

