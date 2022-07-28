from cProfile import label
from re import A
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from numpy import size

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
                ax.set_ylim(0,110)
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

def plot_with_line_plots_two_scales(continents, ref_sets_dict, absolute_errors, outdir, allele_freqs):
    fig = plt.figure(figsize=(30, 10))
    fig.set_dpi(100)
    outer = gridspec.GridSpec(1, 3, wspace=0.2, hspace=0.2)

    for continent , i in zip(continents, range(3)):
        inner = gridspec.GridSpecFromSubplotSpec(1, 2,
                                subplot_spec=outer[i], wspace=0.1, hspace=0.1)
        axParent = plt.Subplot(fig, outer[i])
        axParent.set_title("{}".format(continent.replace("_", " ")), fontweight='bold', pad=20, fontsize = 8)
        axParent.set_xlabel("Allele frequency threshold",  labelpad=20, fontsize = 8)
        axParent.set_xticks([])
        axParent.set_yticks([])
        axParent.spines["top"].set_visible(False)
        axParent.spines["bottom"].set_visible(False)
        fig.add_subplot(axParent)
        
        for j, scale in zip(range(2), [[0, 10], [9, 20]]):
                ax = plt.Subplot(fig, inner[j])
                if j == 1:
                    range_txt = "one to ten"
                else: 
                    range_txt = "ten to hundred"

                ax.set_title("Abundances in the range of {}".format(range_txt), pad=5, fontsize = 8)
                fig.add_subplot(ax)
                for reference_set in ref_sets_dict[continent]:
                    sums = []
                    for af in allele_freqs:
                        af = str(af)
                        sum_per_af = sum(list(absolute_errors[continent][reference_set][af].values())[scale[0]: scale[1]])/10
                        sums.append(sum_per_af)
                    
                    ax.plot(allele_freqs, sums, label = reference_set.replace("_", " "))  
                    ax.legend()                  
                    ax.grid("white")
                    ax.set_yticks((0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100))
                    ax.set_xticks(allele_freqs)
                    ax.set_ylabel("Average absolute prediction error", fontsize = 8)
                    ax.set_ylim(0,100)
                    ax.tick_params(axis='both', labelsize=6)
                    ax.label_outer()

    # save absolute error as pdf in figures folder
    plt.savefig(outdir + "/lineplots.pdf", bbox_inches='tight')

    return 

def plot_with_scatterplots(abundances, dates, results, dirs_and_refs):

    fig, ax = plt.subplots(3, 2, figsize=(20, 20))
    # fig.set_dpi(2000)

    for bench_dir, i in zip(dirs_and_refs.keys(), range(len(dirs_and_refs.keys()))):
        for ref_set, j in zip(dirs_and_refs[bench_dir], range(len(dirs_and_refs[bench_dir]))):
            for date in dates:
                # create a new figure
                ax[i][j].scatter(abundances, [results[bench_dir][ref_set][date][str(abundance)] for abundance in abundances], label= date.replace("_", " "))
                ax[i][j].set_xlabel("Simulated abundance")
                ax[i][j].set_ylabel("Predicted abundance")
                ax[i][j].set_xscale('log')
                ax[i][j].set_title("Reference set: {} \n Benchmark data sourced in {}".format(ref_set.replace("_", " "), bench_dir), fontweight='bold')
                ax[i][j].grid()
            # plot x=y line black and dashed
            ax[i][j].plot(abundances, abundances, color='black', linestyle='dashed', label = "True abundance")
            ax[i][j].legend()
            ax[i][j].set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80 , 90, 100])
                # save figure as pdf with tight layout
    
    plt.subplots_adjust(hspace=0.3)
    plt.savefig("figures/scatter_plot.pdf", bbox_inches='tight')


    return 
