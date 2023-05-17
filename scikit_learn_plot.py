import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

results = pd.read_csv("scikit_learn_timings.csv")

sns.set_theme(context="paper", font_scale=1.4)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), constrained_layout=True, sharey=True)
sns.barplot(y="backend", x="duration", data=results[results["method"] == "fit"], ax=ax1)
ax1.set_xlabel("duration (sec)")
ax1.set_title("fit")

sns.barplot(y="backend", x="duration", data=results[results["method"] == "predict"], ax=ax2)
ax2.set_ylabel("")
ax2.set_xlabel("duration (sec)")
ax2.set_title("predict")

fig.suptitle("LinearDiscriminantAnalysis")
fig.savefig("scikit_learn_timings.pdf")
