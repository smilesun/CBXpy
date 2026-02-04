import numpy as np

from cbx.objectives import snowflake, Rastrigin, Himmelblau, three_hump_camel, Himmelblau32

from cbx.dynamics import CBO, PolarCBO
from cbx.scheduler import multiply

from cbx_visual import vis_cbx_dynamic_history
from plot_snowflake import plot_objective


def create_demo(obj_func,
                initial_particles,
                sigma,
                class_name=CBO,
                extra_info=None):
    name = obj_func.__class__.__name__

    init_kwargs = dict(
        alpha=1.,  # heat
        # noise='anisotropic',
        sigma=2.,  # noise
        verbosity=0,
        track_args={'names': [
            'x',
            'consensus',
            'drift']},
        batch_args={'size': 50},
    )

    if class_name is PolarCBO:
        init_kwargs["kappa"] = 1.5

    dyn = class_name(obj_func,  # objective function
                     d=2,  # dimension of system,
                     # default None if initial particles are given
                     x=initial_particles,  # initial particles, will be reshaped according to d
                     **init_kwargs)

    dyn.optimize(sched=multiply(factor=1.02, maximum=1e10))

    box = float(np.max(np.abs(initial_particles)))
    vis_cbx_dynamic_history(dyn, box=box,
                            save_gif_path=f"cbo_{name}_sigma_{sigma}.gif")


if __name__ == "__main__":
    np.random.seed(42)

    N = 100
    # x = np.random.uniform(low=-2., high=2., size=(2, N, 2))
    initial_particles = np.random.uniform(low=-6., high=6., size=(2, N, 2))

    # create_demo(three_hump_camel(), x, "polarized_three_hump_camel")
    # create_demo(Himmelblau(), x, sigma=0)
    create_demo(Himmelblau32(),
                initial_particles=initial_particles,
                sigma=0.1)
    # create_demo(snowflake(), x, "polarized_snowflake")
    plot_objective(Rastrigin())
