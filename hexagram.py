import numpy as np
import matplotlib.pyplot as plt

from globals import degrees, discr_deg, root_subst


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
        subplt.text(x*1.06-0.06, y*1.05-0.04, discr_deg[i], fontweight='bold')
        x_r, y_r = rotation_sixth(x, y)
        subplt.plot([0, x, x_r], [0, y, y_r], color='black')
        x, y = x_r, y_r
    subplt.text(-0.01, 0.02, 'I', fontweight='bold')


def plot_chord(ax, chroma_vector, root='C', color='r', normalized=False):
    if root != 'N':
        decal = root_subst[root]
        x = []
        y = []
        for ternary in range(6):
            d2 = degrees.index(discr_deg[ternary])
            d3 = degrees.index(discr_deg[(ternary+1)%6])
            c1 = chroma_vector[decal]
            c2 = chroma_vector[(d2+decal) % 12]
            c3 = chroma_vector[(d3+decal) % 12]
            if not normalized:
                tot = c1+c2+c3
                if tot > 1e-6:
                    c1 /= tot
                    c2 /= tot
                    c3 /= tot

            xc = (c3-c2) / np.sqrt(3)
            yc = 1 - c1
            xc, yc = rotation_sixth(xc, yc, ternary)
            x.append(xc)
            y.append(yc)
        
        ax.scatter(x, y, s=200, alpha=0.3, c=color, edgecolors=None)

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(5,4))
    init_hexagram(ax, 'Test hexagram')
    #C major 7th (maj)
    plot_chord(ax,
               [1, 0.2, 0.1, 0.3, 1, 0.2, 0.3, 1, 0.2, 0.3, 0.2, 1],
               'C', 'r')
    #Eb minor 7th (min)
    plot_chord(ax,
               [0.2, 1, 0.3, 1, 0.2, 0.2, 1, 0.2, 0.1, 0.1, 1, 0.2],
               'Eb', 'b')
    #Db half-diminished 7th (hdim7)
    plot_chord(ax,
               [0.2, 1, 0.2, 0.2, 1, 0.3, 0.2, 1, 0.2, 0.1, 0.3, 1],
               'Db', 'g')
    plt.show()