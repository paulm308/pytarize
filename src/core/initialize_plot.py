from src.plot.lineplot import LinePlot
from src.plot.scatterplot import ScatterPlot
from src.plot.combinedplot import CombinedPlot
# +-------------------+
# | Add new plottypes |
# +-------------------+
from src.core.configuration_data import PlotType


def run_plots(data, cfg):
    """
    Initializes the plot class with cfg and calls the run method of that class with the loaded zummarys.

    Parameters:
    data (dict[str, pd.DataFrame]): A dictionary of all zummarys that are loaded in pandas DataFrames.
    The key of the dictionary is the name of the folder that contains the zummary.
    cfg: The configuration.
    """
    match cfg.plot_type:
        case PlotType.LinePlot:
            plot = LinePlot(cfg)
        case PlotType.ScatterPlot:
            plot = ScatterPlot(cfg)
        case PlotType.CombinedPlot:
            plot = CombinedPlot(cfg)
        # +-------------------+
        # | Add new plottypes |
        # +-------------------+

    plot.run(data)
