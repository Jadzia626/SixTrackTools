#!/usr/local/bin/python
# --------------------------------------------
# Series of useful functions to help plotting
# --------------------------------------------

from __future__ import division

import re
import math

import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib import rcParams


class GetData:

    def __init__(self, infile):
        self.infile = infile

    def is_header(self, line):
        """
        Returns True if the line contains any of the symbols: @, #, $, %, &, *
        --> Useful to skip lines that contain any of these symbols at any position.
        --> Used in the data_line function.
        """
        return re.search(r'#|@|%|\$|&', line) is not None
        

    def data_line(self, column=None, regex=None):
        """
        Generator function that returns the lines of a file, skipping the lines
        containing the symbols: @, #, $, %, &, *.
        >> a = get_columns('dump.txt')
        >> a.next()
        --> Useful to read big data files (avoid loading a whole list in memory).
        --> Used in the data_array function.
        """
        with open(self.infile, 'r') as data:  # using with the file is closed automatically
            for line in data:
                if self.is_header(line):
                    continue
                # split on contiguous blank spaces and remove return of line
                line_list = line.strip('\n').split()
                if (column and regex) is not None:
                    if re.match(regex, line_list[column]):
                        yield line_list
                elif (column and regex) is None:
                    yield line_list
                else:
                    print 'Column or regex missing from arguments'

    # def data_column(self, column=None, regex=None, dtype='number'):
    #     """
    #     Returns a dictionary of lists, containing the columns of the data file.
    #     The dictionary keys are the number of the columns.
    #     """
    #     start_line = self.data_line(column, regex).next()
    #     data_dict = {key: [] for key, item in enumerate(
    #         start_line)}  # Create keys and empty lists
    #     for line in self.data_line(column, regex):
    #         for count, item in enumerate(line):
    #             if type(item) is str:
    #                 # Strip needed for MAD-X output
    #                 data_dict[count].append(item.strip('"'))
    #             elif type(item) is int or type(item) is float:
    #                 data_dict[count].append(float(item))  # Fill in the lists
    #             else:
    #                 print ">> Check the type of the data in your column"
    #     return data_dict

    def my_enumerate(self, sequence, keys, start=0):
        n = start
        for elem in sequence:
            yield keys[n], elem
            n += 1

    def data_column(self, column=None, regex=None, dtype='number'):
        """
        Returns a dictionary of lists, containing the columns of the data file.
        The dictionary keys are the number of the columns.
        """
        start_line = self.data_line(column, regex).next()
        data_dict = {key: [] for key, item in enumerate(start_line)}
        for line in self.data_line(column, regex):
            if line[0] == '*':
                line.pop(0)
                keys = line
                data_dict = {key: [] for key, item in self.my_enumerate(line, keys)}
            if 'keys' in locals():
                if line == keys:
                    continue
                for count, item in self.my_enumerate(line, keys):
                    if dtype == 'string':
                        # Strip needed for MAD-X output
                        data_dict[count].append(item.strip('"'))
                    elif dtype == 'number':
                        data_dict[count].append(float(item))  # Fill in the lists
            else:
                for count, item in enumerate(line):
                    if dtype == 'string':
                        # Strip needed for MAD-X output
                        data_dict[count].append(item.strip('"'))
                    elif dtype == 'number':
                        data_dict[count].append(float(item))  # Fill in the lists
        return data_dict


class PlotData(GetData):

    def basic(self, x_coord, y_coord, filename, title=None, x_label=None, y_label=None, x_lim=None, y_lim=None, scatter=False, column=None, regex=None):
        data_dict = PlotData(self.infile).data_column(column, regex)
        x = data_dict[x_coord]
        y = data_dict[y_coord]

        DPI = 300
        textwidth = 6
        font_spec = {"font.family": "serif",  # use as default font
                     # custom serif font
                     "font.serif": ["New Century Schoolbook"],
                     # custom sans-serif font
                     "font.sans-serif": ["helvetica"],
                     "font.size": 12,
                     "font.weight": "bold"}
        rc('text', usetex=True)
        rc('text.latex', preamble=r'\usepackage{cmbright}')
        rcParams['figure.figsize'] = textwidth, textwidth / 1.618
        rcParams.update(font_spec)

        if scatter:
            plt.scatter(x, y)
        else:
            plt.plot(x, y)

        # plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.grid(b=None, which='major')

        if title is not None:
            plt.title(title)

        if x_label is not None:
            plt.xlabel(x_label)

        if y_label is not None:
            plt.ylabel(y_label)

        if x_lim is not None:
            plt.xlim(x_lim)

        if y_lim is not None:
            plt.ylim(y_lim)

        plt.subplots_adjust(left=0.13, bottom=0.14, right=0.94, top=0.93)
        plt.savefig(filename + '.png', dpi=DPI)
        plt.clf()

def check_simplecticity(matrix):
    omega = np.zeros((2, 2))
    omega[0,0] = 0
    omega[0,1] = 1
    omega[1,0] = -1
    omega[1,1] = 0
    new_matrix = np.dot(np.dot(np.transpose(matrix), omega), matrix)
    if np.array_equal(new_matrix, omega) is True:
        print ">> Is symplectic"
    else:
        print ">> Is not symplectic"

def get_sigmas(alpha, beta, emittance, dispersion, spread, beta_rel, gamma_rel):
    """
    Returns the phase space amplitudes from the twiss parameters
    Input is in meters.
    """
    gamma = (1 + alpha**2) / beta
    sigma = np.sqrt((emittance * beta + dispersion**2 *
                     spread**2) / (beta_rel * gamma_rel))
    sigma_p = np.sqrt((emittance * gamma) / (beta_rel * gamma_rel))
    return sigma, sigma_p

def get_sigma_ellipse(sigma_x, sigma_y, offset_x, offset_y, number, alpha, beta):
    """
    Getting and drawing sigma ellipses.
    """
    d = {}
    for n in range(0, number + 1):
        if beta == 0 and alpha == 0:
            d[n] = get_ellipse_coords(a=n*sigma_x, b=n*sigma_y, x=offset_x, y=offset_y, k=1)
        else:
            d[n] = get_ellipse_coords(a=n*sigma_x, b=n*sigma_y, x=offset_x, y=offset_y, angle=math.degrees(math.atan(-alpha/beta)),k=1)
    return d


def get_rel_params(energy, mass=0.938272046e9):
    """
    Returns the relativistic beta and gamma, the momenta and mass used.
    The energy has to be input in [eV] and the particle mass in [eV/c^2].
    If no mass is input, the proton mass will be taken by default.
    """
    c = 2.99792485e8  # m/s
    gamma_rel = energy / mass
    beta_rel = np.sqrt(gamma_rel**2 - 1) / gamma_rel
    p0 = np.sqrt((energy - mass) * (energy + mass))
    return gamma_rel, beta_rel, p0, mass


def get_ip1(x, y):
    """Treats the x and y coordinates already extracted from the data in order to easily plot
    around IP1 (i.e. convert s coordinate of 26900 m to -100 m).
    The function arguments' are the variables x and y that you want to treat, respectively .
    Example:
    var_x, var_y = get_ip1(var_x, var_y)
    """
    zipped = zip(x, y)
    x_temp = []
    y_temp = []
    for e1, e2 in zipped:
        if float(e1) < (26658.8832 / 2):
            x_temp.append(float(e1))
            y_temp.append(float(e2))
        if float(e1) >= (26658.8832 / 2):
            x_temp.append(float(e1) - 26658.8832)
            y_temp.append(float(e2))
    x = []
    y = []
    for e1, e2 in sorted(zip(x_temp, y_temp), key=lambda t: t[0]):
        x.append(e1)
        y.append(e2)
    return x, y


def get_bucket(machine, plot=True, z=0, DELTA=0):
    """ Returns the data needed to plot the RF bucket of LHC.
    Adapted from Kyrre Sjobak.
    Usage: plt.contour(PHIp * 0.1, DELTA_E, H, 40, linewidths=0.3, cmap='terrain_r')
    """
    mp = 0.938272046e9                     # proton mass, eV/c^2
    e  = 1.60217657e-19                    # C, electron charge
    c  = 2.99792485e8                      # m/s, speed of light

    if machine == 'HL_coll' or machine == 'HL_coll_tcp':
        h = 35640                          # RF harmonic number
        omegaRF = 400.8e6 * np.pi * 2      # Hz, omegaRF = h*omega0
        slip = 3.467e-4                    # Slip factor @ collission
        V = 16e6                           # V, RF voltage @ collissions
        phiS = 0.0                         # Radians, synchronous RF phase
        E0 = 7e12                          # Beam energy, eV
        bunch = 0.0755
        limit = 8e-4
    elif machine == 'HL_coll_200' or machine == 'HL_coll_tcp_200':
        h = 17820                          # RF harmonic number
        omegaRF = 200.8e6 * np.pi * 2      # Hz, omegaRF = h*omega0
        slip = 3.467e-4                    # Slip factor @ collission
        V = 16e6                           # V, RF voltage @ collissions
        phiS = 0.0                         # Radians, synchronous RF phase
        E0 = 7e12                          # Beam energy, eV
        bunch = 2*0.0755
        limit = 8e-4
    elif machine == 'SPS_inj':
        h = 4636                           # RF harmonic number
        omegaRF = 200.2644e6 * np.pi * 2   # Hz, omegaRF = h*omega0
        slip = 5.55e-4
        # slip =5.98e-4
        V = 2e6                            # V, RF voltage @ collissions
        phiS = 0.0                         # Radians, synchronous RF phase
        E0 = 26e9                          # Beam energy, eV
        bunch = 0.3
        limit = 6e-3
    else:
        print '>> Please input "HL_coll" or "SPS_inj" as first argument.'

    def get_hamiltonian(DELTA, PHI, omegaRF, E0, slip, p0, beta, h, V, phiS):
        p = p0 * (1.0 + DELTA)  # eV/c
        E = np.sqrt(p ** 2 + mp ** 2)
        DELTA_E = E / E0 - 1
        omega0 = omegaRF / h
        H1 = 0.5 * omegaRF * slip * DELTA ** 2
        H2 = omega0 * V / (2 * np.pi * beta ** 2 * E) * \
            (np.cos(PHI) - np.cos(phiS) + (PHI - phiS) * np.sin(phiS))
        H = H1 + H2  # Given in action-angle variables

        PHIp = np.pi - PHI  # Unstable fixed point (end of bucket)

        return H, PHIp, DELTA_E

    gamma_rel, beta, p0, mass = get_rel_params(E0)

    if plot == True:
        conversion = c / (omegaRF / (np.pi * 2))
        bucket = (np.pi * beta * c) / omegaRF
        print '>> Half bucket length = ', bucket
        print beta
        delta = np.linspace(-limit * conversion, limit * conversion, 300)  # delta p / p
        phi = np.linspace(-3 * np.pi, 3 *np.pi, 300)
        DELTA, PHI   = np.meshgrid(delta, phi)
        H, PHIp, DELTA_E = get_hamiltonian(DELTA, PHI, omegaRF, E0, slip, p0, beta, h, V, phiS)

        return PHIp * ((beta * c) / omegaRF), DELTA_E, H

    elif plot == False:
        PHI = omegaRF * z / (c * beta) - np.pi
        H, PHIp, DELTA_E = get_hamiltonian(DELTA, PHI, omegaRF, E0, slip, p0, beta, h, V, phiS)

        return H

def replace_column(infile, str_in, col_in, str_out, col_out, col_length=20):
    """This function takes a data file organized in columns as input.
    It replaces the data of the selected column following conditions on another column.
    For column number [arg_2], if it matches [arg_1], column [arg_4] will be substituted by
    [arg 3].
    TO DO: set a fixed column length
    """
    outfile = infile.replace('.txt','') + '_modified.txt'
    with open(infile, 'r') as data:
        with open(outfile, 'wt') as out:
            for line in data:
                line_list = line.strip('\n').split()
                if str_in in line_list[col_in]:
                    line_list[col_out] = str_out
                    spacing = '      '
                    out.write(spacing.join( line_list) + '\n')
                else:
                    out.write(line)


def get_ir(ir, s, coord):
    """This function stores the information relevant to the plotting of a specific Interaction Region (IR),
    i.e. the position of the IR in the accelerator and the limit of the vertical coordinate.

    The function arguments' are (in order):
    - Number of the IR (from 1 to 8, both included)
    - Limit in the vertical coordinate

    Example:
    position, ylim = get_ir(2, 0.6)
    """
    t = (0, 3332.436584, 6664.7208, 9997.005016,
         13329.28923, 16661.72582, 19994.1624, 23315.37898)
    zipped = zip(s, coord)
    s_temp = []
    coord_temp = []
    for i, j in zipped:
        s_temp.append(i - t[int(ir) - 1])
        coord_temp.append(j)
    s_new, coord_new = get_ip1(s_temp, coord_temp)
    return s_new, coord_new

def plot_2d_hist(coord_1, coord_2, nbins):
    H, xedges, yedges = np.histogram2d(coord_1, coord_2, bins=nbins)
    H = np.rot90(H)   # H needs to be rotated and flipped
    H = np.flipud(H)
    Hmasked = np.ma.masked_where(H == 0, H)  # Mask pixels with a value of zero (they will appear in white)
    plt.pcolormesh(xedges, yedges, Hmasked, norm=None, vmin=0, vmax=100)

def plot_elem(color, height, bottom, name_in=[], s_in=[], l_in=[], *args):
    """
    >> Input: color, height and bottom of the element, list of all the names, positions and lengths, list of element names
    >> Output: bar plot

    Example:
    plot_elem('red', height, bottom, name_b1_twiss, s_b1_twiss, l_b1_twiss,  'MQXFA', 'MQXFB') # Triplet: Q1, Q3, Q2
    """
    regex_list = list(args)
    name_out = []
    s_out = []
    l_out = []
    for a in regex_list:
        regex = re.compile(a)
        for list_1, list_2, list_3 in zip(name_in, s_in, l_in):
            if regex.match(list_1):
                name_out.append(list_1)
                s_out.append(float(list_2))
                l_out.append(float(list_3))
    for s, element, l in zip(s_out, name_out, l_out):
        f = s - l
        # left, height, width, bottom
        plt.bar(f, height, l, bottom, color=color, alpha=0.7)

def plot_sigma(my_dict, number):
    for n in range(0, number + 1):
        plt.plot(my_dict[n][:,0], my_dict[n][:,1], color='gray', linewidth=0.2)


def load_data_coll(infile, coll_id):
    f = open(infile, 'r')
    s = []
    x = []
    y = []
    for line in f.xreadlines():
        columns = line.strip('\n').split()
        if columns[0] == '#' or columns[0] == '@' or columns[0] == '*' or columns[0] == '$' or columns[0] == '%' or columns[0] == '%1=s' or columns[0] == '%Ind' or columns[0] != coll_id:
            continue
        s.append(float(columns[2]))
        x.append(float(columns[3]))
        y.append(float(columns[5]))
    f.close()
    s_array = np.asarray(s)
    x_array = np.asarray(x)
    y_array = np.asarray(y)
    return s_array, x_array, y_array


def get_ellipse_coords(a=0.0, b=0.0, x=0.0, y=0.0, angle=0.0, k=2):
    """ Draws an ellipse using (360*k + 1) discrete points; based on pseudo code
    given at http://en.wikipedia.org/wiki/Ellipse
    k = 1 means 361 points (degree by degree)
    a = major axis distance,
    b = minor axis distance,
    x = offset along the x-axis
    y = offset along the y-axis
    angle = clockwise rotation [in degrees] of the ellipse;
        * angle=0  : the ellipse is aligned with the positive x-axis
        * angle=30 : rotated 30 degrees clockwise from positive x-axis
    """
    pts = np.zeros((360 * k + 1, 2))

    beta = -angle * np.pi / 180.0
    sin_beta = np.sin(beta)
    cos_beta = np.cos(beta)
    alpha = np.radians(np.r_[0.:360.:1j * (360 * k + 1)])

    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)

    pts[:, 0] = x + (a * cos_alpha * cos_beta - b * sin_alpha * sin_beta)
    pts[:, 1] = y + (a * cos_alpha * sin_beta + b * sin_alpha * cos_beta)

    return pts


def get_madx_columns(infile, *args):
    """
    >> Input: data file to read, list of column headers that you want to extract
    >> Output: a dictionary of lists, key accesible with the name of the header

    Example:
    dict_b1_twiss = get_madx_columns(infile_b1_twiss, 'S', 'L', 'BETX', 'BETY', 'X', 'Y', 'NAME')
    dict_b1_twiss['S']
    """

    f = open(infile, 'r')
    # Skip rows starting with certain symbols
    column_filter = ('#', '@', '*', '$', '%', '%1=s',
                     '%Ind')  # ToDo:function in util.py
    extract_header = ('#', '@', '$', '%', '%1=s', '%Ind')

    # Choose which parameters you want to extract to a list
    my_list = list(args)
    my_dict = {i: [] for i in my_list}

    # Extract the associated column index
    col_idx = []
    col_name = []  # ToDo: convert this to tuple to skip the zip
    for line in f.xreadlines():
        columns = line.strip('\n').split()
        for idx, value in enumerate(columns):
            if columns[0] in extract_header:
                continue
            if value in my_list:  # for item in my_list: /if value == item:
                col_idx.append(idx - 1)
                col_name.append(value)
        for index, name in zip(col_idx, col_name):
            if columns[0] in column_filter:
                continue
            if name != 'NAME':
                my_dict[name].append(float(columns[index]))
            elif name == 'NAME':
                my_dict[name].append(columns[index].strip('"'))
    f.close()
    return my_dict


def plot_twiss_beams(s, coord, energy, norm_em, beta, ip, lim):
    m = 938272046  # eV/c
    gamma_rel = energy / m
    beta_rel = np.sqrt(1 - (1 / gamma_rel**2))
    geom_em = norm_em / (gamma_rel * beta_rel)
    if ip == '1':
        s_final, coord_final = get_ip1(s, coord)
        s_temp, beta_final = get_ip1(s, beta)
    else:
        s_ip, coord_ip = get_ir(ip, s, coord)
        s_temp, beta_ip = get_ir(ip, s, beta)
        s_final, coord_final = get_ip1(s_ip, coord_ip)
        s_temp, beta_final = get_ip1(s_ip, beta_ip)
    # sigma
    sigma = []
    for i in beta_final:
        sigma.append(np.sqrt(geom_em * i))
    one_sigma = []
    for i, j in zip(sigma, coord_final):
        one_sigma.append(j + i)
    m_one_sigma = []
    for i, j in zip(sigma, coord_final):
        m_one_sigma.append(j - i)
    five_sigma = []
    for i, j in zip(sigma, coord_final):
        five_sigma.append(j + 5 * i)
    m_five_sigma = []
    for i, j in zip(sigma, coord_final):
        m_five_sigma.append(j - 5 * i)

    s_final_2 = []
    coord_final_2 = []
    one_sigma_2 = []
    m_one_sigma_2 = []
    five_sigma_2 = []
    m_five_sigma_2 = []
    for e1, e2, e3, e4, e5, e6 in zip(s_final, coord_final, one_sigma, m_one_sigma, five_sigma, m_five_sigma):
        if abs(e1) < float(lim):
            s_final_2.append(e1)
            coord_final_2.append(e2)
            one_sigma_2.append(e3)
            m_one_sigma_2.append(e4)
            five_sigma_2.append(e5)
            m_five_sigma_2.append(e6)

    return s_final_2, coord_final_2, one_sigma_2, m_one_sigma_2, five_sigma_2, m_five_sigma_2


def plot_twiss(s, coord, ip, lim):
    if ip == '1':
        s_final, coord_final = get_ip1(s, coord)
    else:
        s_ip, coord_ip = get_ir(ip, s, coord)
        s_final, coord_final = get_ip1(s_ip, coord_ip)

    s_final_2 = []
    coord_final_2 = []

    for e1, e2 in zip(s_final, coord_final):
        if abs(e1) < float(lim):
            s_final_2.append(e1)
            coord_final_2.append(e2)

    return s_final_2, coord_final_2


def check_twiss(x, xp):
    term_1 = round(
        np.mean(np.multiply(x - np.mean(x), x - np.mean(x))) / em, 3)
    term_2 = round(
        np.mean(np.multiply(x - np.mean(x), xp - np.mean(xp))) / em, 3)
    term_3 = round(
        np.mean(np.multiply(x - np.mean(x), xp - np.mean(xp))) / em, 3)
    term_4 = round(
        np.mean(np.multiply(xp - np.mean(xp), xp - np.mean(xp))) / em, 3)
    return term_1, term_2, term_3, term_4
