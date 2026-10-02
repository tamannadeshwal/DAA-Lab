import matplotlib.pyplot as plt

def generate_trend_plots(dataframe, output_dir="graphs/"):
    """Creates clear operational charts plotting performance dynamics."""
    plt.style.use('default')
    
    # Chart 1: Time Plot
    fig1, ax1 = plt.subplots(figsize=(10, 5.5))
    for label in dataframe["Algorithm"].unique():
        partition = dataframe[dataframe["Algorithm"] == label]
        ax1.plot(partition["Input Dimension"], partition["Runtime (Sec)"], marker="o", linewidth=2, label=label)
    
    ax1.set_xlabel("Problem Scale (N)", fontsize=11)
    ax1.set_ylabel("Execution Duration (Seconds)", fontsize=11)
    ax1.set_title("Operational Runtime Scale Evaluation", fontsize=13, fontweight='bold')
    ax1.legend(loc="upper left")
    plt.tight_layout()
    fig1.savefig(f"{output_dir}runtime_scaling.png", dpi=200)
    plt.close(fig1)

    # Chart 2: Memory Plot
    fig2, ax2 = plt.subplots(figsize=(10, 5.5))
    for label in dataframe["Algorithm"].unique():
        partition = dataframe[dataframe["Algorithm"] == label]
        ax2.plot(partition["Input Dimension"], partition["Peak Memory (KB)"], marker="D", linestyle="--", label=label)
    
    ax2.set_xlabel("Problem Scale (N)", fontsize=11)
    ax2.set_ylabel("Peak RAM Allocation (KB)", fontsize=11)
    ax2.set_title("Memory Allocation Profiling", fontsize=13, fontweight='bold')
    ax2.legend(loc="upper left")
    plt.tight_layout()
    fig2.savefig(f"{output_dir}memory_footprint.png", dpi=200)
    plt.close(fig2)
