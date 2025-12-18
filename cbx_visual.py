from cbx.plotting import PlotDynamicHistory
from IPython import display
import matplotlib.pyplot as plt


def vis_cbx_dynamic_history(dyn, box=2, step=50, pause_time=0.5):
    fig, ax = plt.subplots(1,)
    pl = PlotDynamicHistory(
        dyn, ax=ax,
        objective_args={'x_min': -box, 'x_max': box, 'cmap': 'Blues'},
        plot_consensus=True,
        plot_drift=True
    )

    for i in range(0, pl.max_it, step):
        pl.plot_at_ind(i)
        pl.decorate_at_ind(i)
        display.display(fig)
        display.clear_output(wait=True)
        plt.pause(pause_time)
