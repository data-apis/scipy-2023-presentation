import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

scikit_learn_results = pd.read_csv("scikit-learn_timings.csv")

fontsize = 16

repl = {
    "numpy": "NumPy",
    "cupy": "CuPy",
    "torch_cpu": "PyTorch\nCPU",
    "torch_gpu": "PyTorch\nCUDA",
}
scikit_learn_results["Backend"] = scikit_learn_results["Backend"].replace(repl)

means = scikit_learn_results.groupby(["Backend", "Method"]).mean()
# Normalize by the mean for Backend == NumPy
scikit_learn_results["Speedup vs. NumPy"] = scikit_learn_results.apply(lambda row: means.loc[("NumPy", row["Method"]), "Duration"]/row["Duration"], axis=1)
scikit_learn_results = scikit_learn_results[scikit_learn_results["Backend"] != "NumPy"]

# # Omit first (warmup) timing for each method
# for backend in scikit_learn_results["Backend"].unique():
#     for method in scikit_learn_results["Method"].unique():
#         scikit_learn_results = scikit_learn_results.drop(scikit_learn_results[(scikit_learn_results["Backend"] == backend) & (scikit_learn_results["Method"] == method)].index[0])

sns.set_theme(context="paper", font_scale=1.4)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(16, 5), constrained_layout=True)

sns.barplot(y="Speedup vs. NumPy", x="Backend",
            data=scikit_learn_results[scikit_learn_results["Method"] ==
                                      "fit"], ax=ax1, errorbar=None)

y_pos = (0, 20, 40, 60, 80)
ax1.set_title("scikit-learn\nLDA fit", fontsize=fontsize)
ax1.set_ylim(1, 80)
ax1.set_yticks(y_pos)

sns.barplot(y="Speedup vs. NumPy", x="Backend",
            data=scikit_learn_results[scikit_learn_results["Method"] ==
                                      "predict"], ax=ax2, errorbar=None)
ax2.set_title("scikit-learn\nLDA predict", fontsize=fontsize)
ax2.set_ylim(0, 80)
ax2.set_yticks(y_pos)

print("scikit-learn mean durations:")
print(means)
print()
print("scikit-learn speedup over NumPy:")
print(means.loc["NumPy"] / means)

scipy_results = pd.read_csv("scipy_timings.csv")
scipy_results["Backend"] = scipy_results["Backend"].replace(repl)
means = scipy_results.groupby(["Backend", "Strict"]).mean()
scipy_results["Speedup vs. NumPy"] = scipy_results.apply(lambda row: means.loc[("NumPy", row["Strict"]), "Duration"]/row["Duration"], axis=1)
scipy_results = scipy_results[scipy_results["Backend"] != "NumPy"]

sns.barplot(data=scipy_results[~scipy_results["Strict"]], x="Backend",
            y="Speedup vs. NumPy", ax=ax3, errorbar=None)
ax3.set_title("SciPy\nwelch (optimized)", fontsize=fontsize)
ax3.set_ylim(0, 80)
ax3.set_yticks(y_pos)

sns.barplot(data=scipy_results[scipy_results["Strict"]], x="Backend",
            y="Speedup vs. NumPy", ax=ax4, errorbar=None)

ax4.set_title("SciPy\nwelch (strict)", fontsize=fontsize)
ax4.set_ylim(0, 1)

for ax in ax1, ax2, ax3, ax4:
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticklabels([label.get_text().replace(' ', '\n') for label in ax.get_xticklabels()])
    for label in ax.get_xticklabels():
        label.set_fontsize(fontsize)
    for label in ax.get_yticklabels():
        label.set_fontsize(fontsize)

# Add axis labels to the whole plot
fig.supylabel("Speedup vs. NumPy", fontsize=fontsize+4)
# fig.suptitle("scikit-learn and SciPy performance with array API backends", fontsize=fontsize+8)

plt.tight_layout()
fig.savefig("../assets/timings.pdf")
fig.savefig("../assets/timings.svg", format="svg")
