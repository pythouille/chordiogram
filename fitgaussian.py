import matplotlib.pyplot as plt
import numpy as np

from globals import notes, degrees, discr_deg

#inspired by https://gist.github.com/andrewgiessel/6122739
def gaussian(height, center_x, center_y, width_x, width_y, rotation):
    """
    Returns a gaussian function with the given parameters
    'rotation' is given in radian
    """
    center_x = center_x*np.cos(rotation) - center_y*np.sin(rotation)
    center_y = center_x*np.sin(rotation) + center_y*np.cos(rotation)
    
    def rotgauss(x,y):
        xp = x*np.cos(rotation) - y*np.sin(rotation)
        yp = x*np.sin(rotation) + y*np.cos(rotation)
        g = height*np.exp(
            -(((center_x-xp)/width_x)**2+
              ((center_y-yp)/width_y)**2)/2.)
        return g
    return rotgauss


def cov_gaussian(width_x, width_y, rotation):
    """
    Returns the covariance matrix for a gaussian distribution
    with given parameters ;
    see https://www.visiondummy.com/2014/04/geometric-interpretation-covariance-matrix/
    for more information
    """
    m_cov = np.array([[width_x**2, 0],
                      [0, width_y**2]])
    m_rot = np.array([[np.cos(rotation),-np.sin(rotation)],
                      [np.sin(rotation), np.cos(rotation)]])
    m_cov = np.dot(m_rot,m_cov)
    m_cov = np.dot(m_cov, np.transpose(m_rot))
    return m_cov


def fitgaussian(data):
    """
    Returns parameters of the 2D gaussian
    fitting the data
    """
    x = np.mean(data[0])
    y = np.mean(data[1])
    covariance = np.cov(data)
    w, v = np.linalg.eig(covariance)
    width_x = np.sqrt(w[0])
    width_y = np.sqrt(w[1])
    acos = np.arccos(v[0][0])
    asin = np.arcsin(v[0][1])
    #resole the equations : { arcsos(rot) = a
    #                         arcsin(rot) = b }
    if acos-asin < 1e-5 or acos-np.pi+asin < 1e-5:
        rotation = acos
    else:
        rotation = -acos
    return x, y, width_x, width_y, rotation


def plot_gaussian(height, center_x, center_y, width_x, width_y, rotation):
    """Plot a 2D gaussian with given parameters"""
    width = 2*max(width_x,width_y)
    x = np.linspace(center_x - 2*width, center_x + 2*width, 4*width)
    y = np.linspace(center_y - 2*width, center_y + 2*width, 4*width)
    x, y = np.meshgrid(x,y)

    G = gaussian(height, center_x, center_y,
                 width_x, width_y, rotation)(x, y)
    plt.figure()
    plt.imshow(G)
    plt.colorbar()
    plt.show()


def xy2simplex(x, y):
    """
    Returns c1, c2, c3 such as x=log2(c2/c1), y=log2(c3/c1) and Sum(c_i)=1
    """
    c1 = 1 / (1+2**x+2**y)
    c2 = (2**x) / (1+2**x+2**y)
    c3 = (2**y) / (1+2**x+2**y)
    return c1, c2, c3


def simplex2xy(c1, c2, c3):
    """
    Returns the transformation of a dot from a 2-simplex to |R²
    """
    return np.log2((c2+1e-10)/(c1+1e-10)),np.log2((c3+1e-10)/(c1+1e-10))


def gauss_predict(chroma_vector, fit_model):
    """
    Returns an ordered list of 60 chord classes, with their score, from
    the most probable to the least, according to the given model
    """
    rep_q = {}
    for r in range(12): #each note as first degree / possible root
        root_name = notes[r]
        c1 = chroma_vector[r]
        for chd in range(5): #each jazz5 chord
            pb = 1
            for ter in range(6): #each ternary plot
                c2 = chroma_vector[(r+degrees.index(discr_deg[ter]))%12]
                c3 = chroma_vector[(r+degrees.index(discr_deg[(ter+1)%6]))%12]
                xc, yc = simplex2xy(c1, c2, c3)
                pb *= gaussian(1,
                             fit_model[chd][ter][0],
                             fit_model[chd][ter][1],
                             fit_model[chd][ter][2],
                             fit_model[chd][ter][3],
                             fit_model[chd][ter][4])(xc, yc)
            #save the final probability
            rep_q[root_name + ' ' + name_jazz5[chd]] = pb
    #order the list
    lst_q = [[k, v] for k, v in rep_q.items()]
    lst_q.sort(key=lambda e: e[1], reverse = True)
    return lst_q