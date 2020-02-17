import matplotlib.pyplot as plt


def setup():
    plt.rc('axes', grid=True)
    plt.rc('grid', color='lightgray')
    plt.rc('legend', fancybox=True, framealpha=0.5)


setup()


def refine(show_default=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            show = kwargs.pop('show', show_default)

            func(*args, **kwargs)

            if show:
                plt.show()

        return wrapper
    return decorator

