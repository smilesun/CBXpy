from cbx.plotting import PlotDynamicHistory
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from contextlib import ExitStack
from pathlib import Path
import shutil

try:
    from IPython import display as ipy_display
except ImportError:  # pragma: no cover
    ipy_display = None


def vis_cbx_dynamic_history(
    dyn,
    box,
    step=50,
    pause_time=0.5,
    *,
    save_gif_path=None,
    save_mp4_path=None,
    fps=None,
    dpi=120,
    show=True,
):
    fig, ax = plt.subplots(1,)
    pl = PlotDynamicHistory(
        dyn, ax=ax,
        objective_args={'x_min': -box, 'x_max': box, 'cmap': 'Blues'},
        plot_consensus=True,
        plot_drift=True
    )

    if fps is None:
        fps = int(round(1 / pause_time)) if pause_time else 10

    writer_specs = []
    if save_gif_path is not None:
        save_gif_path = str(save_gif_path)
        Path(save_gif_path).parent.mkdir(parents=True, exist_ok=True)
        writer_specs.append(
            animation.PillowWriter(fps=fps).saving(fig, save_gif_path, dpi))

    if save_mp4_path is not None:
        if shutil.which("ffmpeg") is None:
            raise RuntimeError(
                "Saving mp4 requires ffmpeg to be installed and on PATH. "
                "Either install ffmpeg or use save_gif_path."
            )
        save_mp4_path = str(save_mp4_path)
        Path(save_mp4_path).parent.mkdir(parents=True, exist_ok=True)
        writer_specs.append(
            animation.FFMpegWriter(fps=fps).saving(fig, save_mp4_path, dpi))

    with ExitStack() as stack:
        writers = [stack.enter_context(ctx) for ctx in writer_specs]

        for i in range(0, pl.max_it, step):
            pl.plot_at_ind(i)
            pl.decorate_at_ind(i)

            if writers:
                fig.canvas.draw()
                for w in writers:
                    w.grab_frame()

            if show:
                if ipy_display is None:
                    raise RuntimeError(
                        "show=True requires IPython; \
                        set show=False to save without displaying.")
                ipy_display.display(fig)
                ipy_display.clear_output(wait=True)
                plt.pause(pause_time)
