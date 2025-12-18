import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


def plot_objective(obj_func, name=None, box=2.5, num_pts_landscape=100):
    if name is None:
        name = obj_func.__class__.__name__
    fig = plt.figure(figsize=(15, 5))
    x_min = -box
    x_max = box
    y_min = -box
    y_max = box
    xx = np.linspace(x_min, x_max, num_pts_landscape)
    yy = np.linspace(y_min, y_max, num_pts_landscape)
    XX, YY = np.meshgrid(xx, yy)
    XXYY = np.stack((XX.T, YY.T)).T
    Z = np.zeros((num_pts_landscape, num_pts_landscape, 2))
    Z[:, :, 0:2] = XXYY
    ZZ = obj_func(Z)

    ax0 = fig.add_subplot(121)
    ax1 = fig.add_subplot(122, projection='3d')
    cs = ax0.contourf(XX, YY, ZZ, 20, cmap=cm.get_cmap('Blues'))

    ax0.contour(cs, colors='white', alpha=0.2)
    if hasattr(obj_func, 'minima'):
        ax0.scatter(obj_func.minima[:, 0], obj_func.minima[:, 1],
                    color='blue', marker='x', s=20)

    ax1.plot_surface(XX, YY, ZZ, cmap=cm.get_cmap('Blues'))
    ax0.set_title('Contour plot')
    ax1.set_title('Surface plot')
    plt.savefig(f'{name}_objective.pdf')
    plt.show()
