import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

scikit_learn_results = pd.read_csv("scikit_learn_timings.csv")

repl = {
    "numpy": "NumPy",
    "cupy": "CuPy",
    "torch_cpu": "PyTorch CPU",
    "torch_gpu": "PyTorch CUDA",
}
scikit_learn_results["Backend"] = scikit_learn_results["Backend"].replace(repl)

# # Omit first (warmup) timing for each method
# for backend in scikit_learn_results["Backend"].unique():
#     for method in scikit_learn_results["Method"].unique():
#         scikit_learn_results = scikit_learn_results.drop(scikit_learn_results[(scikit_learn_results["Backend"] == backend) & (scikit_learn_results["Method"] == method)].index[0])

sns.set_theme(context="paper", font_scale=1.4)
# Keep the y-axis log ticks
sns.set(rc={"ytick.left": True})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), constrained_layout=True)

sns.barplot(y="Duration", x="Backend", data=scikit_learn_results[scikit_learn_results["Method"] == "fit"], ax=ax1, log=True)
ax1.set_title("fit()")

sns.barplot(y="Duration", x="Backend", data=scikit_learn_results[scikit_learn_results["Method"] == "predict"], ax=ax2, log=True)
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

means = scikit_learn_results.groupby(["Backend", "Method"]).mean()
print("scikit-learn mean durations:")
print(means)
print()
print("scikit-learn speedup over NumPy:")
print(means.loc["NumPy"] / means)

plt.tight_layout()
fig.savefig("../assets/timings.pdf")

scipy_results = pd.read_csv("scipy_timings.csv")
scipy_results["Backend"] = scipy_results["Backend"].replace(repl)

# Plot the data
fig = plt.figure(figsize=(12, 6))

# Plot the bars, with hatching for strict APIs
ax = sns.barplot(data=scipy_results, x="Backend", hue="Strict", y="Duration",
                 log=True)


# Set colors based on the library and add hatches for Optimized API (note these
# colors match the colors used in the scikit-learn plot)
default_colors = sns.color_palette()

# The bars are ordered first by API Type then Library, even though they are
# plotted in the other order, like
# 0 4  1 5  2 6  3 7
for i, thisbar in enumerate(ax.patches):
    # Get the default edge color
    edge_color = thisbar.get_edgecolor()
    thisbar.set_color(default_colors[i%4])
    # Add a hatch to the second bar in thisbar
    if i >= 4:
        thisbar.set_hatch('//')
        thisbar.set_edgecolor(edge_color)


ax.set_ylabel("")
ax.set_xlabel("")
fig.supylabel("Duration (sec)")
fig.supxlabel("Library")
ax.set_yticks([0.1, 1, 10, 100])
ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())
plt.xticks()
fig.suptitle("SciPy welch() performance with array API backends")

# Add a legend
handles = [plt.Rectangle((0, 0), 1, 1, facecolor='gray'),
           plt.Rectangle((0, 0), 1, 1, facecolor='gray', hatch='//')]
labels = ['Strict API', 'Optimized API']
plt.legend(handles, labels, loc='upper left')

# Save the figure
plt.tight_layout()
plt.savefig("../assets/scipy_timings.pdf")
