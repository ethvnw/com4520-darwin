import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

walk_type_mapping = {
    "limitedselfloop": "Limited Self-Loop",
    "randomwithreset": "Random With Reset",
    "statistical": "Statistical",
    "random": "Random",
}

df = pd.read_csv("results/20250327_224435.csv")
df = df[df["Walk Length"] != -1]
df["Walk Type"] = df["Walk Type"].map(walk_type_mapping)

sns.set_theme(style="whitegrid", palette="muted")


palette = {
    "Random": "#4C72B0",  # Muted blue
    "Random With Reset": "#DD8452",  # Soft orange-brown
    "Limited Self-Loop": "#55A868",  # Muted green
    "Statistical": "#C44E52",  # Muted red
}


g = sns.FacetGrid(df, col="Walk Type", col_wrap=2, height=4, sharex=False, sharey=False)

# Map scatter and trend line per type
for ax, (walk_type, subdata) in zip(g.axes.flatten(), df.groupby("Walk Type")):
    color = palette.get(walk_type, "black")
    sns.scatterplot(
        data=subdata,
        x="Walk Length",
        y="HSI Suite Length",
        ax=ax,
        color=color,
        s=40,
        alpha=0.7,
    )
    sns.regplot(
        data=subdata,
        x="Walk Length",
        y="HSI Suite Length",
        ax=ax,
        scatter=False,
        color=color,
        ci=None,  # no grey shadow
        line_kws={"linestyle": "--", "linewidth": 2},
    )
    ax.set_title(walk_type)

g.set_axis_labels("Walk Length", "HSI Suite Length")

plt.subplots_adjust(top=0.9)
g.figure.suptitle("Walk Length vs HSI Suite Length", fontsize=16)

g.savefig("facetgrid_walklengths_colored.svg", dpi=300)
plt.show()
