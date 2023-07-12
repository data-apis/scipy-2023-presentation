import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

fontsize = 16


def plot(plot_type):
    repl = {
        "numpy": "NumPy",
        "cupy": "CuPy",
        "torch_cpu": "PyTorch\nCPU",
        "torch_gpu": "PyTorch\nGPU",
    }

    sns_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(context="paper", font_scale=1.4, style="ticks", rc=sns_params)

    if plot_type == "both":
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(16, 5), constrained_layout=True)
    elif plot_type == "scikit-learn":
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), constrained_layout=True)
    elif plot_type == "scipy":
        fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(8, 5), constrained_layout=True)

    y_min = 0
    y_max = 55
    y_pos = (0, 10, 20, 30, 40, 50, 60)

    if plot_type in ["both", "scikit-learn"]:
        scikit_learn_results = pd.read_csv("scikit-learn_timings.csv")

        scikit_learn_results["Backend"] = scikit_learn_results["Backend"].replace(repl)

        means = scikit_learn_results.groupby(["Backend", "Method"]).mean()
        # Normalize by the mean for Backend == NumPy
        scikit_learn_results["Speedup vs. NumPy"] = scikit_learn_results.apply(lambda row: means.loc[("NumPy", row["Method"]), "Duration"]/row["Duration"], axis=1)
        scikit_learn_results = scikit_learn_results[scikit_learn_results["Backend"] != "NumPy"]

        sns.barplot(y="Speedup vs. NumPy", x="Backend",
                    data=scikit_learn_results[scikit_learn_results["Method"] ==
                                              "fit"], ax=ax1, errorbar=None)

        ax1.set_title("scikit-learn\nLDA fit", fontsize=fontsize)
        ax1.set_title("a", loc='left', y=1.07, x=-0.12, weight='bold', fontsize=fontsize+2)
        ax1.set_ylim(y_min, y_max)
        ax1.set_yticks(y_pos)
        ax1.bar_label(ax1.containers[0], fmt=r'$%.1f\times$')

        sns.barplot(y="Speedup vs. NumPy", x="Backend",
                    data=scikit_learn_results[scikit_learn_results["Method"] ==
                                              "predict"], ax=ax2, errorbar=None)
        ax2.set_title("scikit-learn\nLDA predict", fontsize=fontsize)
        ax2.set_title("b", loc='left', y=1.07, x=-0.12, weight='bold', fontsize=fontsize+2)
        ax2.set_ylim(y_min, y_max)
        ax2.set_yticks(y_pos)
        ax2.bar_label(ax2.containers[0], fmt='%.1f')

        for ax in ax1, ax2:
            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.set_xticklabels([label.get_text().replace(' ', '\n') for label in ax.get_xticklabels()])
            for label in ax.get_xticklabels():
                label.set_fontsize(fontsize)
            for label in ax.get_yticklabels():
                label.set_fontsize(fontsize)

        print("scikit-learn mean durations:")
        print(means)
        print()
        print("scikit-learn speedup over NumPy:")
        print(means.loc["NumPy"] / means)

    if plot_type in ["both", "scipy"]:
        scipy_results = pd.read_csv("scipy_timings.csv")
        scipy_results["Backend"] = scipy_results["Backend"].replace(repl)
        means = scipy_results.groupby(["Backend", "Strict"]).mean()
        scipy_results["Speedup vs. NumPy"] = scipy_results.apply(lambda row: means.loc[("NumPy", row["Strict"]), "Duration"]/row["Duration"], axis=1)
        scipy_results = scipy_results[scipy_results["Backend"] != "NumPy"]

        sns.barplot(data=scipy_results[~scipy_results["Strict"]], x="Backend",
                    y="Speedup vs. NumPy", ax=ax3, errorbar=None)
        ax3.set_title("SciPy\nwelch (optimized)", fontsize=fontsize)
        ax3.set_title("c", loc='left', y=1.07, x=-0.12, weight='bold', fontsize=fontsize+2)
        ax3.set_ylim(y_min, y_max)
        ax3.set_yticks(y_pos)
        ax3.bar_label(ax3.containers[0], fmt='%.1f')

        sns.barplot(data=scipy_results[scipy_results["Strict"]], x="Backend",
                    y="Speedup vs. NumPy", ax=ax4, errorbar=None)

        ax4.set_title("SciPy\nwelch (strict)", fontsize=fontsize)
        ax4.set_title("d", loc='left', y=1.07, x=-0.12, weight='bold', fontsize=fontsize+2)
        ax4.set_ylim(0, 1)
        ax4.bar_label(ax4.containers[0], fmt='%.2f')

        for ax in ax3, ax4:
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

    return fig

def main():
    if len(sys.argv) == 1:
        plot_type = "both"
    elif sys.argv[1] == "both":
        plot_type = "both"
    elif sys.argv[1] == "scipy":
        plot_type = "scipy"
    elif sys.argv[1] == "scikit-learn":
        plot_type = "scikit-learn"
    else:
        raise ValueError("Unknown plot type")

    if plot_type == "both":
        fig = plot("both")
        fig.savefig("../paper/assets/timings.pdf")
        fig.savefig("../paper/assets/timings.svg", format="svg")
    if plot_type == "scikit-learn":
        fig = plot("scikit-learn")
        fig.savefig("../paper/assets/scikit-learn_timings.pdf")
        fig.savefig("../paper/assets/scikit-learn_timings.svg", format="svg")
    if plot_type == "scipy":
        fig = plot("scipy")
        fig.savefig("../paper/assets/scipy_timings.pdf")
        fig.savefig("../paper/assets/scipy_timings.svg", format="svg")

if __name__ == "__main__":
    main()
