import numpy as np

from cbx.objectives import snowflake
from cbx.dynamics import PolarCBO
from cbx.scheduler import multiply

from cbx_visual import vis_cbx_dynamic_history


np.random.seed(42)
f = snowflake()
N = 100
x = np.random.uniform(-2., 2., (2, N, 2))

dyn = PolarCBO(f,  # objective function
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


vis_cbx_dynamic_history(dyn, box=2)
