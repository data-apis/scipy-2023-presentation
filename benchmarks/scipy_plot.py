import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(context="paper", font_scale=1.4)
# Keep the y-axis log ticks
sns.set(rc={"ytick.left" : True})

# Define all the data lists
all_data = {
    "NumPy Strict API": [15.710065103136003],
    "NumPy Optimized API": [4.919703705934808, 5.045966051053256, 4.901492156088352, 4.895045991055667, 4.9723517938982695],
    "PyTorch CPU Strict API": [180.73112939088605],
    "PyTorch CPU Optimized API": [1.1638194161932915, 1.120931203942746, 1.0023795650340617, 1.1782302970532328, 1.1800141278654337],
    "PyTorch CUDA Strict API": [281.28290371201],
    "PyTorch CUDA Optimized API": [0.13685095217078924, 0.1785686588846147, 0.17490072012878954, 0.13612257200293243, 0.1353681399486959],
    "CuPy Strict API": [155.41026511299424],
    "CuPy Optimized API": [0.23821475682780147, 0.24966995394788682, 0.24989571701735258, 0.25607424485497177, 0.24746034992858768],
}

# Create the DataFrame
data_list = []
for label, values in all_data.items():
    for value in values:
        data_list.append([label, value])

df = pd.DataFrame(data_list, columns=["API", "Time"])

df['Library'] = df['API'].apply(lambda x: x.split()[0] if 'PyTorch' not in x else ' '.join(x.split()[:2]))
df['API Type'] = df['API'].apply(lambda x: ' '.join(x.split()[-2:]))

# Plot the data
fig = plt.figure(figsize=(12, 6))

# Plot the bars, with hatching for strict APIs
ax = sns.barplot(data=df, x="Library", hue="API Type", y="Time", log=True)

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
