from matplotlib import pyplot as plt
from cbx.dynamics import CBXDynamic
from cbx.plotting import PlotDynamic, PlotDynamicHistory
dyn = CBXDynamic(lambda x: x**2, d=1)
dyn.optimize()
plotter = PlotDynamicHistory(dyn)
plotter.init_plot()
plt.show()

