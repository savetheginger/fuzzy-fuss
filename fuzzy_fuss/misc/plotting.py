import matplotlib.pyplot as plt


def setup():
    plt.rc('axes', grid=True)
    plt.rc('grid', color='lightgray')
    plt.rc('legend', fancybox=True, framealpha=0.5)


setup()


def refine_plot(show_default=False):
    def decorator(func):
        def wrapper(*args, ax=None, **kwargs):
            show = kwargs.pop('show', show_default)

            if ax is None:
                fig, ax = plt.subplots()

                for i, item in enumerate(args):
                    if isinstance(item, plt.Axes):
                        ax = item
                        args = args[:i] + args[i+1:]
                        break

            # setup axis
            ax.axhline(0, color='darkgray', zorder=1, lw=3)
            ax.axhline(1, color='dimgray', zorder=1, lw=1)

            default_xlabel = 'x values'

            label = getattr(args[0], 'variable_name', None) or getattr(args[0], 'name', None)

            x = ax.get_xlabel()
            if not x and x != default_xlabel:
                ax.set_xlabel(label or default_xlabel)

            if not ax.get_title() and label:
                val = getattr(args[0], 'value_name', None)
                ax.set_title(f"{label}{': ' if val else ''}{val or ''}")

            func(*args, ax=ax, **kwargs)

            if show:
                plt.show()

        return wrapper

    return decorator


def refine_multiplot(func):
    def wrapper(*args, show=True, **kwargs):
        func(*args, **kwargs)

        if show:
            plt.show()

    return wrapper


