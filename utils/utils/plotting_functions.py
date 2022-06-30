from re import A
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def plot_with_boxplots_two_scales(num_of_figures, reference_sets, absolute_errors, outdir):
    
    fig = plt.figure(figsize=(20, 10))
    fig.set_dpi(100)
    outer = gridspec.GridSpec(2, 3, wspace=0.2, hspace=0.2)

    if num_of_figures == 4: 
        outer = gridspec.GridSpec(2, 2, wspace=0.2, hspace=0.2)


    for reference_set, i in zip(reference_sets, range(num_of_figures)):
            inner = gridspec.GridSpecFromSubplotSpec(1, 2,
                            subplot_spec=outer[i], wspace=0.1, hspace=0.1)
   
            axParent = plt.Subplot(fig, outer[i])
                
            axParent.set_title("{}".format(reference_set.replace("_", " ")), fontweight='bold', pad=5, fontsize = 8)
            axParent.set_xlabel("Simulated abundance",  labelpad=20, fontsize = 8)
            axParent.set_xticks([])
            axParent.set_yticks([])
            axParent.spines["top"].set_visible(False)
            axParent.spines["bottom"].set_visible(False)

            if num_of_figures == 5 and i == 5:
                axParent.set_visible(False)
            if num_of_figures == 5 and i == 3:
               axParent.set_position([0.24+ 0.24/4,0.125,0.228/2,0.343])
            if num_of_figures == 5 and i == 4:
                axParent.set_position([0.55+ 0.24/4,0.125,0.228/2,0.343])

            fig.add_subplot(axParent)

            for j, abundances, scale in zip(range(2), [[1,2,3,4,5,6,7,8,9,10], [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]], [[0, 10], [9, 20]]):
                ax = plt.Subplot(fig, inner[j])
                fig.add_subplot(ax)
                ax.boxplot(list(list(item.values())for item in absolute_errors[reference_set].values())[scale[0]: scale[1]])
                ax.set_xticklabels(abundances)
                ax.grid("white")
                ax.set_yticks((0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100))
                ax.set_ylabel("Absolute prediction error", fontsize = 8)
                ax.set_ylim(0,100)
                ax.tick_params(axis='both', labelsize=6)
                ax.label_outer()

                if num_of_figures == 5 and i == 3 and j == 0:
                    ax.set_position([0.24,0.125,0.228/2,0.343])
                if num_of_figures == 5 and i == 3 and j == 1:
                    ax.set_position([0.24 + 0.24/2,0.125,0.228/2,0.343])
                if num_of_figures == 5 and i == 4 and j == 0:
                    ax.set_position([0.55, 0.125,0.228/2,0.343])
                if num_of_figures == 5 and i == 4 and j == 1:
                    ax.set_position([0.55 + 0.24/2,0.125,0.228/2,0.343])
    # save absolute error as pdf in figures folder
    plt.savefig(outdir + "boxplot_results.pdf", bbox_inches='tight')
            
       
    return 
    