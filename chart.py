import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D

walk_type_mapping = {
    "limitedselfloop": "Limited Self-Loop",
    "randomwithreset": "Random with Reset",
    "statistical": "Statistical",
    "random": "Random",
}

df = pd.read_csv("results/data.csv")
df = df[df["Walk Length"] != -1]
df["Walk Type"] = df["Walk Type"].map(walk_type_mapping)

sns.set_theme(style="whitegrid", palette="muted")


palette = {
    "Random": "#4C72B0",
    "Random with Reset": "#DD8452",
    "Limited Self-Loop": "#55A868",
    "Statistical": "#C44E52",
}

df["State Size"] = df["State Size"].astype(str)

g = sns.FacetGrid(
    df,
    row="State Size",
    col="Walk Type",
    height=3,
    margin_titles=True,
    sharex=False,
    sharey=False,
)

for (walk_type, state_size), subdata in df.groupby(["Walk Type", "State Size"]):
    ax = g.axes[
        int(df["State Size"].unique().tolist().index(state_size)),
        int(df["Walk Type"].unique().tolist().index(walk_type)),
    ]
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
        ci=None,
        line_kws={"linestyle": "--", "linewidth": 2},
    )

g.set_titles(row_template="", col_template=r"$\bf{{{col_name}}}$")

for j, walk_type in enumerate(df["Walk Type"].unique()):
    ax = g.axes[0, j]
    ax.set_title(walk_type, fontweight="bold")

row_labels = df["State Size"].unique().tolist()
n_rows = len(row_labels)
n_cols = len(df["Walk Type"].unique())


dotted_line = Line2D(
    [0],
    [0],
    color="black",
    linestyle="--",
    linewidth=2,
    label="Trend Line (Linear Fit)",
)
g.figure.legend(
    handles=[dotted_line],
    loc="upper right",
    bbox_to_anchor=(0.98, 1.05),
    ncol=1,
    frameon=True,
)

plt.subplots_adjust(top=0.985, hspace=0.5, wspace=0.4)

for i, state_size in enumerate(row_labels):
    ax = g.axes[i, 0]
    pos = ax.get_position()
    x = pos.x0

    if i == 0:
        y = pos.y1 + 0.03
    else:
        y = pos.y1 + 0.01
    g.figure.text(
        x,
        y,
        f"{state_size} STATES",
        ha="left",
        va="bottom",
        fontsize=14,
        fontweight="bold",
    )

g.savefig("facetgrid_walklengths_by_statesize.svg", dpi=300)
plt.show()
