import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

results = pd.read_csv("scikit_learn_timings.csv")

sns.set_theme(context="paper", font_scale=1.4)
# Keep the y-axis log ticks
sns.set(rc={"ytick.left" : True})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), constrained_layout=True)
sns.barplot(y="Duration", x="Backend", data=results[results["Method"] == "fit"], ax=ax1, log=True)
ax1.set_title("fit()")

sns.barplot(y="Duration", x="Backend", data=results[results["Method"] == "predict"], ax=ax2, log=True)
ax2.set_title("predict()")

for ax in ax1, ax2:
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticklabels([label.get_text().replace(' ', '\n') for label in ax.get_xticklabels()])

ax1.set_yticks([0.1, 1, 10])
ax1.get_yaxis().set_major_formatter(plt.ScalarFormatter())
ax2.set_yticks([0.01, 0.1])
ax2.get_yaxis().set_major_formatter(plt.ScalarFormatter())

# Add X-axis label to the whole plot
fig.supxlabel("Backend")
fig.supylabel("Duration (sec)")

fig.suptitle("scikit-learn LinearDiscriminantAnalysis performance with array API backends")

plt.tight_layout()
fig.savefig("../assets/scikit_learn_timings.pdf")

means = results.groupby(["Backend", "Method"]).mean()
print("Mean durations:")
print(means)
print()
print("Speedup over NumPy:")
print(means.loc["NumPy"] / means)
