import numpy as np

from cbx.objectives import snowflake, Rastrigin, Himmelblau, three_hump_camel

from cbx.dynamics import PolarCBO
from cbx.scheduler import multiply

from cbx_visual import vis_cbx_dynamic_history
from plot_snowflake import plot_objective


def create_demo(obj_func,
                initial_particles,
                sigma,
                class_name=PolarCBO,
                extra_info=None):
    name = obj_func.__class__.__name__

    dyn = class_name(obj_func,  # objective function
                     d=2,  # dimension of system,
                     # default None if initial particles are given
                     x=x,  # initial particles, will be reshaped according to d
                     alpha=1.,  # heat
                     # noise='anisotropic',
                     sigma=2.,  # noise
                     kappa=1.5,
                     verbosity=0,
                     track_args={'names': [
                         'x',
                         'consensus',
                         'drift']},
                     batch_args={'size': 50})

    dyn.optimize(sched=multiply(factor=1.02, maximum=1e10))

    vis_cbx_dynamic_history(dyn, box=2,
                            save_gif_path=f"cbo_{name}_sigma_{sigma}.gif")


if __name__ == "__main__":
    np.random.seed(42)

    N = 100
    x = np.random.uniform(-2., 2., (2, N, 2))

    # create_demo(three_hump_camel(), x, "polarized_three_hump_camel")
    # create_demo(Himmelblau(), x, sigma=0)
    create_demo(Himmelblau(), x)
    # create_demo(snowflake(), x, "polarized_snowflake")
    plot_objective(Rastrigin())
