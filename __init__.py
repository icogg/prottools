from .vanwarrington import *
from .apparentimpedance import *
from .capbank import *


class PDF(object):
  def __init__(self, pdf, size=(900,600)):
    self.pdf = pdf.replace(' ', '%20')
    self.size = size

  def _repr_html_(self):
    return '<iframe src={0} width={1[0]} height={1[1]}></iframe>'.format(self.pdf, self.size)

  def _repr_latex_(self):
    return r'\includegraphics[width=1.0\textwidth]{{{0}}}'.format(self.pdf)
