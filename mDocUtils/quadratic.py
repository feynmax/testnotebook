import math
from fractions import Fraction
from .numbers import *

class QuadraticTerm:
    solutiontext = ["keine reelle Lösung.", "1 Lösung:", "2 Lösungen:"]
    signmath = ["< 0", "= 0", "> 0"]

    def __init__(self, a, b, c, outputForm=None, pqForm=False):
        
        self.F = outputForm if outputForm is not None else OutputFormatter()
        self.ispqForm = pqForm

        if pqForm:
            a = 1
        self.a = a
        self.b = b
        self.c = c
        self.xvertex = rationalDiv(-b, 2*a)
        
        ############################################## Discriminant

        if pqForm:
            self.D1 = self.xvertex * self.xvertex
            self.D2 = -c
        else:
            self.D1 = b*b
            self.D2 = -4*a*c
        
        self.D = self.D1 + self.D2
        if math.isclose(self.D, 0, abs_tol=1e-9):
            self.D = 0
        self.num_sol = (self.D > 0) - (self.D < 0) + 1

        ############################################## Step-by-step solutions

        if self.num_sol == 0:
            self.sol = []
        elif self.num_sol == 1:
            self.sol = [ self.xvertex ]
        else:
            if self.ispqForm:
                self.pmsign = r"\pm"
                self.rootVal, self.rootForm = self.rational_root(self.D)
                self.sol = [ self.xvertex - self.rootVal, self.xvertex + self.rootVal ]
            else:
                self.denom_2a = abs(2*a)
                self.num_b = -b * ( (a>0) - (a<0) )         # -b * sgn(a)
                self.pmsign = r"\pm" if a>0 else r"\mp"
                self.rootVal, self.rootForm = self.rational_root(self.D)
                self.sol = [ rationalDiv(self.num_b - self.rootVal, self.denom_2a),
                             rationalDiv(self.num_b + self.rootVal, self.denom_2a) ]
        
    
    def format(self, num):
        return self.F.numFormat(num)
        
    def D_and_sign(self, color=None):
        out = rf'\; = {self.format(self.D)} \;' if self.D else '\;'
        return out + self.F.colortext(self.signmath[self.num_sol], color=color)
    
    def solutioninfo(self):
        return f'D {self.signmath[self.num_sol]},' + '&nbsp;'*3 + f'also gibt es {self.solutiontext[self.num_sol]}'
    
    def termFormat(self):
        term  = self.F.termPM(self.a, appendstr='x^2', midterm=False)
        term += self.F.termPM(self.b, appendstr='x', midterm=True)
        return term + self.F.termPM(self.c, midterm=True)
    
    def coeffList(self, separator=r'\,,\quad ', finalsep='', color=None):
        if self.ispqForm:
            coefflist = ['q=' + self.format(self.c), 'p=' + self.format(self.b), r'\Rightarrow\;\frac{p}2=' + self.format(-self.xvertex), ]
        else:
            coefflist = ['a=' + self.format(self.a), 'b=' + self.format(self.b), 'c=' + self.format(self.c)]
        return self.F.colortext(separator.join(coefflist) + finalsep, color=color)
    
    def get_plot_xrange(self):
        if self.num_sol > 1:
            dx = self.sol[1] - self.sol[0]
        else:
            dy = 4/abs(self.a) if (self.num_sol > 0) else max(4/abs(self.a), abs(self.c/self.a/4))
            dx = math.sqrt(dy)
        return self.xvertex - dx, self.xvertex + dx
    
    def expand_plot_yrange(self, ymin, ymax):
        if self.a>0:                            # Bei Lösungen 25% nach unten, sonst unten 20% vom Range oben
            ymin = ymin - 0.25*(ymax-ymin) if self.num_sol > 0 else -0.2*ymax
        else:                                   # Wenn a<0 -> umgekehrt, nach oben
            ymax = ymax + 0.25*(ymax-ymin) if self.num_sol > 0 else -0.2*ymin
        return ymin, ymax
    
    def formelD(self, prefix='D = '):
        return prefix + (r'\left(\dfrac{p}2\right)^2 - q' if self.ispqForm else r'b^2-4\,a\,c')

    def formelTemplate(self, bp2='-b', pmsign=r'\pm', root=r'\sqrt{D}', denom=r'2\cdot a'):
        outstr = f'{bp2} {pmsign} {root}'
        return outstr if self.ispqForm else rf'\dfrac{{{outstr}}}{{{denom}}}'


    def rational_root(self, D):
        
        if isinstance(D, int):
            rootVal = math.sqrt(D)
            if rootVal == int(rootVal):
                return int(rootVal), str(int(rootVal))
            return rootVal, self.F.sqrt_of(self.format(D))
        
        if isinstance(D, Fraction):
            rootn = math.sqrt(D.numerator)
            if rootn == int(rootn):
                rootd = math.sqrt(D.denominator)
                if rootd == int(rootd):
                    rootVal = Fraction(int(rootn), int(rootd))
                    return rootVal, self.format(rootVal)
            return math.sqrt(D), self.F.sqrt_of(self.format(D))
        
        if isinstance(D, float):
            rootVal = math.sqrt(D)
            return rootVal, self.format(rootVal)

