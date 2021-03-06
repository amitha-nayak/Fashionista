from __future__ import division

import numpy as np


def voc_colormap(labels):
    """Color map used in PASCAL VOC

    Args:
        labels (iterable of ints): Class ids.

    Returns:
        numpy.ndarray: Colors in RGB order. The shape is :math:`(N, 3)`,
        where :math:`N` is the size of :obj:`labels`. The range of the values
        is :math:`[0, 255]`.

    """
    colors = []
    for label in labels:
        r, g, b = 0, 0, 0
        i = label
        for j in range(8):
            if i & (1 << 0):
                r |= 1 << (7 - j)
            if i & (1 << 1):
                g |= 1 << (7 - j)
            if i & (1 << 2):
                b |= 1 << (7 - j)
            i >>= 3
        colors.append((r, g, b))
    return np.array(colors, dtype=np.float32)


def vis_image(img, ax=None):
    """Visualize a color image.

    Args:
        img (~numpy.ndarray): See the table below.
            If this is :obj:`None`, no image is displayed.
        ax (matplotlib.axes.Axis): The visualization is displayed on this
            axis. If this is :obj:`None` (default), a new axis is created.

    .. csv-table::
        :header: name, shape, dtype, format

        :obj:`img`, ":math:`(3, H, W)`", :obj:`float32`, \
        "RGB, :math:`[0, 255]`"

    Returns:
        ~matploblib.axes.Axes:
        Returns the Axes object with the plot for further tweaking.

    """
    from matplotlib import pyplot as plot

    if ax is None:
        fig = plot.figure()
        ax = fig.add_subplot(1, 1, 1)
    if img is not None:
        ax.imshow(img)
    return ax


def vis_segmap(
    img,
    label,
    label_names=None,
    label_colors=None,
    ignore_label_color=(255, 255, 255),
    alpha=0.6,
    all_label_names_in_legend=False,
    ax=None,
):
    """Visualize a semantic segmentation.

    Args:
        img (~numpy.ndarray): See the table below. If this is :obj:`None`,
            no image is displayed.
        label (~numpy.ndarray): See the table below.
        label_names (iterable of strings): Name of labels ordered according
            to label ids.
        label_colors: (iterable of tuple): An iterable of colors for regular
            labels.
            Each color is RGB format and the range of its values is
            :math:`[0, 255]`.
            If :obj:`colors` is :obj:`None`, the default color map is used.
        ignore_label_color (tuple): Color for ignored label.
            This is RGB format and the range of its values is :math:`[0, 255]`.
            The default value is :obj:`(0, 0, 0)`.
        alpha (float): The value which determines transparency of the figure.
            The range of this value is :math:`[0, 1]`. If this
            value is :obj:`0`, the figure will be completely transparent.
            The default value is :obj:`1`. This option is useful for
            overlaying the label on the source image.
        all_label_names_in_legend (bool): Determines whether to include
            all label names in a legend. If this is :obj:`False`,
            the legend does not contain the names of unused labels.
            An unused label is defined as a label that does not appear in
            :obj:`label`.
            The default value is :obj:`False`.
        ax (matplotlib.axes.Axis): The visualization is displayed on this
            axis. If this is :obj:`None` (default), a new axis is created.

    .. csv-table::
        :header: name, shape, dtype, format

        :obj:`img`, ":math:`(3, H, W)`", :obj:`float32`, \
        "RGB, :math:`[0, 255]`"
        :obj:`label`, ":math:`(H, W)`", :obj:`int32`, \
        ":math:`[-1, \#class - 1]`"

    Returns:
        matploblib.axes.Axes and list of matplotlib.patches.Patch:
        Returns :obj:`ax` and :obj:`legend_handles`.
        :obj:`ax` is an :class:`matploblib.axes.Axes` with the plot.
        It can be used for further tweaking.
        :obj:`legend_handles` is a list of legends. It can be passed
        :func:`matploblib.pyplot.legend` to show a legend.

    """
    import matplotlib
    from matplotlib.patches import Patch

    if label_names is not None:
        n_class = len(label_names)
    elif label_colors is not None:
        n_class = len(label_colors)
    else:
        n_class = label.max() + 1

    if label_colors is not None and not len(label_colors) == n_class:
        raise ValueError(
            "The size of label_colors is not same as the number of classes"
        )
    if label.max() >= n_class:
        raise ValueError("The values of label exceed the number of classes")

    # Returns newly instantiated matplotlib.axes.Axes object if ax is None
    ax = vis_image(img, ax=ax)

    if label_names is None:
        label_names = [str(l) for l in range(label.max() + 1)]

    if label_colors is None:
        label_colors = voc_colormap(list(range(n_class)))
    # [0, 255] -> [0, 1]
    label_colors = np.array(label_colors) / 255
    cmap = matplotlib.colors.ListedColormap(label_colors)

    canvas_img = cmap(label / (n_class - 1), alpha=alpha)

    # [0, 255] -> [0, 1]
    ignore_label_color = (np.array(ignore_label_color) / 255,)
    canvas_img[label < 0, :3] = ignore_label_color

    ax.imshow(canvas_img)

    legend_handles = []
    if not all_label_names_in_legend:
        legend_labels = [l for l in np.unique(label) if l >= 0]
    else:
        legend_labels = range(n_class)
    for l in legend_labels:
        legend_handles.append(
            Patch(color=cmap(l / (n_class - 1)), label=label_names[l])
        )

    return ax, legend_handles
