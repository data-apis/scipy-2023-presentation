import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

scikit_learn_results = pd.read_csv("scikit_learn_timings.csv")

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
# Keep the y-axis log ticks
sns.set(rc={"ytick.left": True})

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(16, 5), constrained_layout=True)

sns.barplot(y="Speedup vs. NumPy", x="Backend",
            data=scikit_learn_results[scikit_learn_results["Method"] ==
                                      "fit"], ax=ax1, ci=None)
ax1.set_title("scikit-learn LinearDiscriminantAnalysis.fit()")

sns.barplot(y="Speedup vs. NumPy", x="Backend",
            data=scikit_learn_results[scikit_learn_results["Method"] ==
                                      "predict"], ax=ax2, ci=None)
ax2.set_title("scikit-learn LinearDiscriminantAnalysis.predict()")

for ax in ax1, ax2:
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticklabels([label.get_text().replace(' ', '\n') for label in ax.get_xticklabels()])

fig.suptitle("scikit-learn and SciPy performance with array API backends")

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

sns.barplot(data=scipy_results[scipy_results["Strict"]], x="Backend",
            y="Speedup vs. NumPy", ax=ax3, ci=None)

ax3.set_ylabel("")
ax3.set_xlabel("")
ax3.set_title("SciPy welch() (strict array API)")

sns.barplot(data=scipy_results[~scipy_results["Strict"]], x="Backend",
            y="Speedup vs. NumPy", ax=ax4, ci=None)
ax4.set_ylabel("")
ax4.set_xlabel("")
ax4.set_title("SciPy welch() (optimized)")

# Add axis labels to the whole plot
fig.supylabel("Speedup vs. NumPy")
fig.supxlabel("Library")

plt.tight_layout()
fig.savefig("../assets/timings.pdf")
