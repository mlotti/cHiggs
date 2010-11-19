import ROOT

class Style:
    def __init__(self, style, color):
        self.style = 22 + style
        self.color = color

    def apply(self, h):
        h.SetLineWidth(2)
        h.SetLineColor(self.color)
        h.SetMarkerColor(self.color)
        h.SetMarkerStyle(self.style)
        h.SetMarkerSize(1)
	h.SetFillColor(0)

    def __call__(self, h):
        self.apply(h)

class StyleFill:
    def __init__(self, style):
        self.style = style

    def apply(self, h):
        self.style.apply(h)
        h.SetFillColor(self.style.color)
        h.SetFillStyle(3002)

    def __call__(self, h):
        self.apply(h)

dataStyle = Style(-2, ROOT.kBlack)

styles = [
    Style(4, ROOT.kBlue),
    Style(5, ROOT.kRed),
    Style(1, ROOT.kGreen+2),
    Style(2, ROOT.kMagenta),
    Style(6, ROOT.kCyan),
    Style(7, ROOT.kYellow+2),
    Style(8, ROOT.kOrange+9),
    Style(9, ROOT.kOrange+3),
    Style(10, ROOT.kMagenta+3),
    Style(11, ROOT.kGray+2),
    Style(12, ROOT.kBlue+3),
    Style(13, ROOT.kOrange+1),
    Style(14, ROOT.kCyan-5),
    Style(0, ROOT.kBlue),
    Style(3, ROOT.kBlack)
    ]


def applyStyle(h, ind):
    styles[ind].apply(h)

def getDataStyle():
    return dataStyle

def getStyles():
    return styles

def getStylesFill():
    return [StyleFill(s) for s in styles]

class Generator:
    def __init__(self, styles):
        self.styles = styles
        self.index = 0

    def reset(self):
        self.index = 0

    def reorder(self, indices):
        self.styles = [self.styles[i] for i in indices]

    def next(self):
        self.index = (self.index+1) % len(self.styles)

    def __call__(self, h):
        self.styles[self.index](h)
        self.next()

def generator(fill=False):
    if fill:
        return Generator(getStylesFill())
    else:
        return Generator(getStyles())
