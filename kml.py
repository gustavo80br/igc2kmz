import coord
import datetime


class Element:
  "KML element base class."

  def name(self):
    "Return name."
    return self.__class__.__name__

  def id(self):
    "Return a unique id."
    return '%x' % id(self)

  def url(self):
    "Return a URL referring to self."
    return '#%s' % self.id()
  
  def write(self, file):
    "Write self to file."
    file.write(str(self))


class SimpleElement(Element):
  "A KML element with no children."

  def __init__(self, text=None, **kwargs):
    self.text = None if text is None else str(text)
    self.attrs = kwargs

  def __str__(self):
    "Return the KML representation of self."
    attrs = '' if len(self.attrs) == 0 else ''.join([' %s="%s"' % pair for pair in self.attrs.items()])
    if self.text is None:
      return '<%s%s/>' % (self.name(), attrs)
    else:
      return '<%s%s>%s</%s>' % (self.name(), attrs, self.text, self.name())


class CompoundElement(Element):
  "A KML element with children."

  def __init__(self, *args, **kwargs):
    self.attrs = {}
    self.children = []
    self.add(*args, **kwargs)

  def add_attrs(self, **kwargs):
    "Add attributes."
    self.attrs.update(kwargs)

  def add(self, *args, **kwargs):
    "Add children."
    self.children.extend(list(args))
    for key, value in kwargs.items():
      self.children.append(globals()[key](value))

  def write(self, file):
    "Write self to file."
    attrs = '' if len(self.attrs) == 0 else ''.join([' %s="%s"' % pair for pair in self.attrs.items()])
    if len(self.children) == 0:
      file.write('<%s%s/>' % (self.name(), attrs))
    else:
      file.write('<%s%s>' % (self.name(), attrs))
      for child in self.children:
        child.write(file)
      file.write('</%s>' % self.name())

  def __str__(self):
    "Return the KML representation of self."
    attrs = '' if len(self.attrs) == 0 else ''.join([' %s="%s"' % pair for pair in self.attrs.items()])
    if len(self.children) == 0:
      return '<%s%s/>' % (self.name(), attrs)
    else:
      return '<%s%s>%s</%s>' % (self.name(), attrs, ''.join(map(str, self.children)), self.name())


class CDATA:
  "A KML CDATA."

  def __init__(self, value):
    self.value = value

  def __str__(self):
    "Return the KML representation of self."
    return '<![CDATA[%s]]>' % self.value


class dateTime:
  "A KML dateTime."

  def __init__(self, value):
    self.value = value

  def __str__(self):
    "Return the KML representation of self."
    return self.value.strftime('%Y-%m-%dT%H:%M:%SZ')


class altitude(SimpleElement): pass
class altitudeMode(SimpleElement): pass
class begin(SimpleElement): pass
class color(SimpleElement): pass


class coordinates(SimpleElement):

  def __init__(self, coords):
    SimpleElement.__init__(self, ' '.join(['%f,%f,%d' % (coord.lon, coord.lat, coord.ele) for coord in coords]))


class description(SimpleElement): pass
class Document(CompoundElement): pass
class end(SimpleElement): pass
class extrude(SimpleElement): pass
class Folder(CompoundElement): pass
class href(SimpleElement): pass
class Icon(CompoundElement): pass
class IconStyle(CompoundElement): pass


class kml(CompoundElement):

  def __init__(self, version, *args, **kwargs):
    CompoundElement.__init__(self, *args, **kwargs)
    self.add_attrs(xmlns='http://earth.google.com/kml/%s' % version)

  def write(self, file):
    "Write self to file."
    file.write('<?xml version="1.0" encoding="UTF-8"?>')
    CompoundElement.write(self, file)


class LineString(CompoundElement): pass
class LineStyle(CompoundElement): pass
class ListStyle(CompoundElement): pass
class listItemType(SimpleElement): pass
class name(SimpleElement): pass
class open(SimpleElement): pass
class overlayXY(SimpleElement): pass
class Placemark(CompoundElement): pass
class Point(CompoundElement): pass
class PolyStyle(CompoundElement): pass
class scale(SimpleElement): pass
class ScreenOverlay(CompoundElement): pass
class screenXY(SimpleElement): pass
class size(SimpleElement): pass
class Snippet(SimpleElement): pass


class Style(CompoundElement):

  def __init__(self, *args, **kwargs):
    CompoundElement.__init__(self, *args, **kwargs)
    self.add_attrs(id=self.id())


class styleUrl(SimpleElement): pass
class TimeSpan(CompoundElement): pass
class visibility(SimpleElement): pass
class when(SimpleElement): pass
class width(SimpleElement): pass
