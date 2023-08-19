import re
import math
from fractions import Fraction
from IPython.display import display, Markdown

class OutputFormatter:
    
    fractypes = {
            'frac':  r'\frac{#1}{#2}',
            'tfrac': r'\tfrac{#1}{#2}',
            'dfrac': r'\dfrac{#1}{#2}',
            'sfrac': r'\mbox{\large$\frac{#1}{#2}$}',
            'mfrac': r'\mbox{\footnotesize$\displaystyle\frac{#1}{#2}$}',
            'lfrac': r'\mbox{\small$\displaystyle\frac{#1}{#2}$}',
            }
    
    def __init__(self, fractype='tfrac'):
        self.defaultfrac = self.fractypes[fractype]
    

    def numFormat(self, n, nachkomma=5, fractype=None, klammer=0):
        # Formatiere Zahl n für LaTeX output, je nach Typ (int, Fraction, float)
        # fractype = dfrac, mfrac, tfrac etc,       nachkomma = Stellen bei floats
        # klammer = 0: keine Klammer drum rum, 1: nur bei negativem n, 2: auch um Brüche, für ^2 etc.
        #
        if isinstance(n, Fraction) and n.denominator==1:
            n = int(n.numerator)
        
        if isinstance(n, int):
            out = f'{n}'
        elif isinstance(n, Fraction):
            formatstr = self.fractypes.get(fractype, self.defaultfrac)
            out= formatstr.replace('#1', str(abs(n.numerator))).replace('#2', str(abs(n.denominator)))
            if n<0:
                out = f'-{out}'
        elif isinstance(n, float):
            out = ("{:." + str(nachkomma) + "f}").format(n).rstrip('0').rstrip('.')     #.replace('.', ',')
        else:
            out = str(n)
        
        klammerdrum = (klammer and n<0) or (klammer>=2 and isinstance(n, Fraction))
        return f'\\left({out}\\right)' if klammerdrum else out


    def termPM(self, num, appendstr='', midterm=False, before0=None, addgap=True, fractype=None):
        
        if len(appendstr)>0:                                            # variable after number?
            if num==1:
                return '+' + appendstr if midterm else appendstr        # if so, suppress coefficient +1...
            elif len(appendstr)>0 and num==-1:
                return '-' + appendstr                                  # ...and -1, just display signs
            elif addgap:
                appendstr = r'\,' + appendstr                           # if gap, add LaTeX space \,
        
        if math.isclose(num, 0, abs_tol=1e-9):                          # treat zero terms according to before0
            return '' if before0 is None else before0 + '0' + appendstr
        
        formatted_term = self.numFormat(num, fractype=fractype)
        if midterm and num>0:
            formatted_term = '+' + formatted_term                       # if in the middle of a term, add + sign when appropriate
        return formatted_term + appendstr

        
    def colortext(self, text, color):
        return r"{\color{" + color + "}{" + text + "}}"
    
    def sqrt_of(self, text, finspace=False):
        space = r"\," if finspace else ''
        return rf" \sqrt{{{text}{space}}} "

    def alert_num_problems(self, numdict):
        issues = []
        for k, v in numdict.items():
            if v is None:
                issues.append(k)
        if len(issues)>0:
            message = "In den Feldern &nbsp;<i>" if len(issues)>1 else "Im Feld &nbsp;<i>"
            message += ' & '.join(issues) + "</i> &nbsp; wurde keine Zahl erkannt.<br> "
            message += '&nbsp;'*20 + 'Bitte korrigiere deine Eingabe!'
            self.infoBox(boldtext='FEHLER: ', text=message, color='red')
            return True
        else:
            return False


    def headerLine(self, text, ruleBefore = False):
        if ruleBefore:
            display(Markdown('***'))
        display(Markdown('### ' + text))


    def infoBox(self, text, boldtext='', color='blue'):
        boxtypes = {'blue': 'info', 'green': 'success', 'yellow': 'warning', 'red': 'danger'}
        boxtype = boxtypes.get(color, 'info')
        infotext = f'<div class="alert alert-block alert-{boxtype}">'+ f'<b>{boldtext}</b>&nbsp; ' + text + ' </div>'
        display(Markdown(infotext))
    

    def numberInputInfo(self):
        self.infoBox("""<b>Gib oben die Koeffizienten ein,</b> dann klicke auf &nbsp; <span style="background-color:white">&nbsp;Berechnen! </span> &nbsp;&nbsp;&rarr;&nbsp; Es erscheint der komplette Lösungsweg.
        <ul>
        <li>Du kannst auch <b><i>Brüche</i></b> eingeben, z.B. als 7/4 oder&nbsp; -1/3 &nbsp;
        (aber <i>keine gemischten Zahlen</i> wie&nbsp; 1 1/2). <br>
        Solange du nur ganze Zahlen oder Brüche eingibst, wird möglichst mit Brüchen gerechnet (und richtig gekürzt). </li>
        <li>Zahlen mit <b><i>Dezimalkomma</i></b> kannst du wie 0.25 oder 0,25 eingeben. Dann wird dezimal gerechnet.</li>
        <li>Alle Leerzeichen werden ignoriert.</li>
        </ul>""")


def rationalDiv(num, den):
    return Fraction(num, den) if isinstance(num, int) and isinstance(den, int) else num/den


def parse_num_input(input_str, defaultval=None):
    # Convert text input into a number, using the appropriate type
    # defaultval=0 or other can be set for empty input
    #
    input_str = input_str.replace(' ','').replace(',','.')      # Remove space and replace decimal point
    try:
        if re.match(r'^[-+]?\d+/\d+$', input_str):              # Detect if input is a rational number
            return Fraction(input_str)
        elif re.match(r'^[-+]?\d+$', input_str):                # Detect if input is an integer
            return int(input_str)
        else:                                                   # Default to float if none of the above
            return float(input_str)
    except ValueError:
        return defaultval if input_str=='' else None


