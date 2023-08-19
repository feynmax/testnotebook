import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

class funcplot:

    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        
        self.ax.set_facecolor('lightgray')
        self.ax.grid(color='white', linestyle='-', linewidth=0.5)
        self.ax.autoscale(tight=True)
        self.ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))


    def addaxeslines(self, x=True, y=True, checkrange=True):
        
        if checkrange:
            xmin, xmax = self.ax.get_xlim() 
            ymin, ymax = self.ax.get_ylim()
            x = x and (ymin <= 0 <= ymax)
            y = y and (xmin <= 0 <= xmax)
        if x:
            self.ax.axhline(y=0, color='black', linewidth=1)
        if y:
            self.ax.axvline(x=0, color='black', linewidth=1)


    def addaxesarrows(self, arrowfrac=0.025, overhang=0.6, x=True, y=True, checkrange=True):

        xmin, xmax = self.ax.get_xlim() 
        ymin, ymax = self.ax.get_ylim()
        if checkrange:
            x = x and (ymin <= 0 <= ymax)
            y = y and (xmin <= 0 <= xmax)

        dps = self.fig.dpi_scale_trans.inverted()               # use width/height of axes object
        bbox = self.ax.get_window_extent().transformed(dps)     # to compute len/wid of arrowheads
        width, height = bbox.width, bbox.height

        if x:
            xhw = arrowfrac *(ymax-ymin)                       # wid/len of x axis arrow
            xhl = arrowfrac *(xmax-xmin)
            self.ax.arrow(xmin, 0, xmax-xmin, 0., fc='k', ec='k', lw = 1,       # draw x axis with arrow
                    head_width=xhw, head_length=xhl, overhang=overhang, 
                    length_includes_head= True, clip_on = False)
        if y:
            yhw = arrowfrac *(xmax-xmin)* height/width         # wid/len of y axis arrow, scaled to match size
            yhl = arrowfrac *(ymax-ymin)* width/height
            self.ax.arrow(0, ymin, 0., ymax-ymin, fc='k', ec='k', lw = 1,       # draw y axis with arrow
                    head_width=yhw, head_length=yhl, overhang=overhang, 
                    length_includes_head= True, clip_on = False)
        if x or y:
            self.ax.set_xlim([xmin, xmax])                                      # restore former axes limits
            self.ax.set_ylim([ymin, ymax])


    def onlyoriginaxes(self, zerotol=1e-4):
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['top'].set_color('none')
                
        newxticks = [i for i in self.ax.get_xticks() if not math.isclose(i, 0, abs_tol=zerotol)]
        newyticks = [i for i in self.ax.get_yticks() if not math.isclose(i, 0, abs_tol=zerotol)]
        self.ax.plot(1, 0, ">k", transform=self.ax.get_yaxis_transform(), clip_on=False)
        self.ax.plot(0, 1, "^k", transform=self.ax.get_xaxis_transform(), clip_on=False)
        self.ax.set_xticks(newxticks, minor=True)
        self.ax.set_yticks(newyticks, minor=True)


    def unitticks(self, dx=1, dy=1):
        if dx is not None:
            if dx==0:
                self.ax.set_xticks([])
            else:
                xlimits = self.ax.get_xlim()
                self.ax.set_xticks(np.arange(dx * math.ceil(xlimits[0]/dx),
                                             dx * math.floor(xlimits[1]/dx) + dx, step=dx))
        if dy is not None:
            if dy==0:
                self.ax.set_yticks([])
            else:
                ylimits = self.ax.get_ylim()
                self.ax.set_yticks(np.arange(dy * math.ceil(ylimits[0]/dy),
                                             dy * math.floor(ylimits[1]/dy) + dy, step=dy))

    def addplot(self, x_vals, y_vals, function_label=None, color='blue', linewidth=2):
        self.ax.plot(x_vals, y_vals, label=function_label, color=color, linewidth=linewidth)

    
    def addpoint(self, x, y, draw='red', fill='mistyrose', lw=2, marker="o", size=9):
        self.ax.plot(x, y, marker=marker, markersize=size, markeredgecolor=draw, markeredgewidth=lw, markerfacecolor=fill)
    

    def addlabel(self, text, coords, pos=None, color='red', fontsize='x-large', textcoords='offset points', xytext=(0,0), ha='center'):
        # coords = coordinates of point, textcoords = offset method, xytext = offset in points, ha = horizontal alignment ('left','right')

        posdict = {'above': ((0,10),  'center'),    'above left':((0,10),  'right'),    'above right':((0,10),  'left'),
                   'here':  ((0,-5),   'center'),   'left':      ((-10,-5),  'right'),  'right':      ((10,-5),  'left'),
                   'below': ((0,-20), 'center'),    'below left':((0,-20), 'right'),    'below right':((0,-20), 'left'),
                }
        if pos is not None and pos in posdict:
            posvals = posdict[pos]
            textcoords = 'offset points'
            xytext = posvals[0]
            ha = posvals[1]
        
        self.ax.annotate(text, coords, textcoords=textcoords, xytext=xytext, ha=ha, color=color, fontsize=fontsize)
    

    def show(self, showlabels=False):
        if showlabels:
            self.ax.legend()
        plt.show()

