import functools

from matplotlib import pyplot as plt


def save_or_show(filepath=None):
    if filepath is not None:
        plt.savefig(filepath)
        plt.clf()
    else:
        plt.show()


def plotting_style(matplotlib_style):
    """Decorater to wrap a plotting function with a style."""
    def style_decorator(plot_func):

        @functools.wraps(plot_func)
        def plot_with_style(*args, **kwargs):
            with plt.style.context(matplotlib_style):
                plot_func(*args, **kwargs)

        return plot_with_style
    return style_decorator


@plotting_style('default')
def plot_roc_curve(fpr, tpr, roc_auc, save=None):
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    save_or_show(save)