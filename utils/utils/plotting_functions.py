import matplotlib.pyplot as plt


def plot_with_boxplots(num_of_figures, reference_sets, absolute_errors, outdir):
    if num_of_figures == 5 :
        fig, ax = plt.subplots(2,3, figsize=(20,10))
        plot_coordinates = [(0,0), (0,1), (0, 2), (1, 0), (1, 1), (1, 2)]
        ax[1][2].set_visible(False)
        fig.subplots_adjust(hspace=0.5)
        ax[1][0].set_position([0.24,0.125,0.228,0.343])
        ax[1][1].set_position([0.55,0.125,0.228,0.343])
    if num_of_figures == 4 :
        fig, ax = plt.subplots(2,2, figsize=(20,10))
        plot_coordinates = [(0,0), (0,1), (1, 0), (1, 1)]
        fig.subplots_adjust(hspace=0.5)


    for reference_set, (i,j) in zip(reference_sets, plot_coordinates):
            ax[i][j].boxplot(list(list(item.values())for item in absolute_errors[reference_set].values()))
            ax[i][j].set_xticklabels(list(absolute_errors[reference_set].keys()))
            ax[i][j].set_title("{}".format(reference_set.replace("_", " ")), fontweight='bold')
            ax[i][j].set_xlabel("Simulated abundance")
            ax[i][j].set_ylabel("Absolute prediction error")
            ax[i][j].set_yticks((0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100))
            ax[i][j].grid("white")
            ax[i][j].set_ylim(0,100)

    # save absolute error as pdf in figures folder
    plt.savefig(outdir + "boxplot_results.pdf", bbox_inches='tight')

    