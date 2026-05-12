from src.plot.baseplot import BasePlot
from src.plot.lineplot import LinePlot
from src.plot.scatterplot import ScatterPlot
from src.core.configuration_data import PlotType


def run_plots(data, cfg):
    match cfg.plot_type:
        case PlotType.LinePlot:
            plot = LinePlot()
        case PlotType.ScatterPlot:
            plot = ScatterPlot()
    plot.run(data, cfg)
