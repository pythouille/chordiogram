import numpy as np
import matplotlib.pyplot as plt

from globals import discr_deg


def rotation_sixth(x, y, n=1):
    """
    rotate n times the point (x,y) clockwise by 60°
    """
    x_r = np.cos(n*np.pi/3)*x + np.sin(n*np.pi/3)*y
    y_r = np.cos(n*np.pi/3)*y - np.sin(n*np.pi/3)*x
    return(x_r, y_r)


def init_hexagram(subplt, title=None):
    """
    plot the structure of the hexagram
    """
    subplt.set_title(title)
    subplt.get_xaxis().set_visible(False)
    subplt.get_yaxis().set_visible(False)
    x, y = -1/np.sqrt(3), 1
    for i in range(6):
        subplt.text(x*1.1-0.1, y*1.1-0.03, discr_deg[i], fontweight='bold')
        x_r, y_r = rotation_sixth(x, y)
        subplt.plot([0, x, x_r], [0, y, y_r], color='black')
        x, y = x_r, y_r
    subplt.text(-0.01, 0.02, 'I', fontweight='bold')




