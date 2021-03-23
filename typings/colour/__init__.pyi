"""
This type stub file was generated by pyright.
"""

import hashlib
import re
import sys
from __future__ import print_function, with_statement

"""Color Library

.. :doctest:

This module defines several color formats that can be converted to one or
another.

Formats
-------

HSL:
    3-uple of Hue, Saturation, Lightness all between 0.0 and 1.0

RGB:
    3-uple of Red, Green, Blue all between 0.0 and 1.0

HEX:
    string object beginning with '#' and with red, green, blue value.
    This format accept color in 3 or 6 value ex: '#fff' or '#ffffff'

WEB:
    string object that defaults to HEX representation or human if possible

Usage
-----

Several function exists to convert from one format to another. But all
function are not written. So the best way is to use the object Color.

Please see the documentation of this object for more information.

.. note:: Some constants are defined for convenience in HSL, RGB, HEX

"""
FLOAT_ERROR = 5e-7
RGB_TO_COLOR_NAMES = { (0, 0, 0): ['Black'],(0, 0, 128): ['Navy', 'NavyBlue'],(0, 0, 139): ['DarkBlue'],(0, 0, 205): ['MediumBlue'],(0, 0, 255): ['Blue'],(0, 100, 0): ['DarkGreen'],(0, 128, 0): ['Green'],(0, 139, 139): ['DarkCyan'],(0, 191, 255): ['DeepSkyBlue'],(0, 206, 209): ['DarkTurquoise'],(0, 250, 154): ['MediumSpringGreen'],(0, 255, 0): ['Lime'],(0, 255, 127): ['SpringGreen'],(0, 255, 255): ['Cyan', 'Aqua'],(25, 25, 112): ['MidnightBlue'],(30, 144, 255): ['DodgerBlue'],(32, 178, 170): ['LightSeaGreen'],(34, 139, 34): ['ForestGreen'],(46, 139, 87): ['SeaGreen'],(47, 79, 79): ['DarkSlateGray', 'DarkSlateGrey'],(50, 205, 50): ['LimeGreen'],(60, 179, 113): ['MediumSeaGreen'],(64, 224, 208): ['Turquoise'],(65, 105, 225): ['RoyalBlue'],(70, 130, 180): ['SteelBlue'],(72, 61, 139): ['DarkSlateBlue'],(72, 209, 204): ['MediumTurquoise'],(75, 0, 130): ['Indigo'],(85, 107, 47): ['DarkOliveGreen'],(95, 158, 160): ['CadetBlue'],(100, 149, 237): ['CornflowerBlue'],(102, 205, 170): ['MediumAquamarine'],(105, 105, 105): ['DimGray', 'DimGrey'],(106, 90, 205): ['SlateBlue'],(107, 142, 35): ['OliveDrab'],(112, 128, 144): ['SlateGray', 'SlateGrey'],(119, 136, 153): ['LightSlateGray', 'LightSlateGrey'],(123, 104, 238): ['MediumSlateBlue'],(124, 252, 0): ['LawnGreen'],(127, 255, 0): ['Chartreuse'],(127, 255, 212): ['Aquamarine'],(128, 0, 0): ['Maroon'],(128, 0, 128): ['Purple'],(128, 128, 0): ['Olive'],(128, 128, 128): ['Gray', 'Grey'],(132, 112, 255): ['LightSlateBlue'],(135, 206, 235): ['SkyBlue'],(135, 206, 250): ['LightSkyBlue'],(138, 43, 226): ['BlueViolet'],(139, 0, 0): ['DarkRed'],(139, 0, 139): ['DarkMagenta'],(139, 69, 19): ['SaddleBrown'],(143, 188, 143): ['DarkSeaGreen'],(144, 238, 144): ['LightGreen'],(147, 112, 219): ['MediumPurple'],(148, 0, 211): ['DarkViolet'],(152, 251, 152): ['PaleGreen'],(153, 50, 204): ['DarkOrchid'],(154, 205, 50): ['YellowGreen'],(160, 82, 45): ['Sienna'],(165, 42, 42): ['Brown'],(169, 169, 169): ['DarkGray', 'DarkGrey'],(173, 216, 230): ['LightBlue'],(173, 255, 47): ['GreenYellow'],(175, 238, 238): ['PaleTurquoise'],(176, 196, 222): ['LightSteelBlue'],(176, 224, 230): ['PowderBlue'],(178, 34, 34): ['Firebrick'],(184, 134, 11): ['DarkGoldenrod'],(186, 85, 211): ['MediumOrchid'],(188, 143, 143): ['RosyBrown'],(189, 183, 107): ['DarkKhaki'],(192, 192, 192): ['Silver'],(199, 21, 133): ['MediumVioletRed'],(205, 92, 92): ['IndianRed'],(205, 133, 63): ['Peru'],(208, 32, 144): ['VioletRed'],(210, 105, 30): ['Chocolate'],(210, 180, 140): ['Tan'],(211, 211, 211): ['LightGray', 'LightGrey'],(216, 191, 216): ['Thistle'],(218, 112, 214): ['Orchid'],(218, 165, 32): ['Goldenrod'],(219, 112, 147): ['PaleVioletRed'],(220, 20, 60): ['Crimson'],(220, 220, 220): ['Gainsboro'],(221, 160, 221): ['Plum'],(222, 184, 135): ['Burlywood'],(224, 255, 255): ['LightCyan'],(230, 230, 250): ['Lavender'],(233, 150, 122): ['DarkSalmon'],(238, 130, 238): ['Violet'],(238, 221, 130): ['LightGoldenrod'],(238, 232, 170): ['PaleGoldenrod'],(240, 128, 128): ['LightCoral'],(240, 230, 140): ['Khaki'],(240, 248, 255): ['AliceBlue'],(240, 255, 240): ['Honeydew'],(240, 255, 255): ['Azure'],(244, 164, 96): ['SandyBrown'],(245, 222, 179): ['Wheat'],(245, 245, 220): ['Beige'],(245, 245, 245): ['WhiteSmoke'],(245, 255, 250): ['MintCream'],(248, 248, 255): ['GhostWhite'],(250, 128, 114): ['Salmon'],(250, 235, 215): ['AntiqueWhite'],(250, 240, 230): ['Linen'],(250, 250, 210): ['LightGoldenrodYellow'],(253, 245, 230): ['OldLace'],(255, 0, 0): ['Red'],(255, 0, 255): ['Magenta', 'Fuchsia'],(255, 20, 147): ['DeepPink'],(255, 69, 0): ['OrangeRed'],(255, 99, 71): ['Tomato'],(255, 105, 180): ['HotPink'],(255, 127, 80): ['Coral'],(255, 140, 0): ['DarkOrange'],(255, 160, 122): ['LightSalmon'],(255, 165, 0): ['Orange'],(255, 182, 193): ['LightPink'],(255, 192, 203): ['Pink'],(255, 215, 0): ['Gold'],(255, 218, 185): ['PeachPuff'],(255, 222, 173): ['NavajoWhite'],(255, 228, 181): ['Moccasin'],(255, 228, 196): ['Bisque'],(255, 228, 225): ['MistyRose'],(255, 235, 205): ['BlanchedAlmond'],(255, 239, 213): ['PapayaWhip'],(255, 240, 245): ['LavenderBlush'],(255, 245, 238): ['Seashell'],(255, 248, 220): ['Cornsilk'],(255, 250, 205): ['LemonChiffon'],(255, 250, 240): ['FloralWhite'],(255, 250, 250): ['Snow'],(255, 255, 0): ['Yellow'],(255, 255, 224): ['LightYellow'],(255, 255, 240): ['Ivory'],(255, 255, 255): ['White'] }
COLOR_NAME_TO_RGB = dict((name.lower(), rgb) for (rgb, names) in RGB_TO_COLOR_NAMES.items() for name in names)
LONG_HEX_COLOR = re.compile(r'^#[0-9a-fA-F]{6}$')
SHORT_HEX_COLOR = re.compile(r'^#[0-9a-fA-F]{3}$')
class C_HSL:
    def __getattr__(self, value):
        ...
    


HSL = C_HSL()
class C_RGB:
    """RGB colors container

    Provides a quick color access.

    >>> from colour import RGB

    >>> RGB.WHITE
    (1.0, 1.0, 1.0)
    >>> RGB.BLUE
    (0.0, 0.0, 1.0)

    >>> RGB.DONOTEXISTS  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: ... has no attribute 'DONOTEXISTS'

    """
    def __getattr__(self, value):
        ...
    


class C_HEX:
    """RGB colors container

    Provides a quick color access.

    >>> from colour import HEX

    >>> HEX.WHITE
    '#fff'
    >>> HEX.BLUE
    '#00f'

    >>> HEX.DONOTEXISTS  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: ... has no attribute 'DONOTEXISTS'

    """
    def __getattr__(self, value):
        ...
    


RGB = C_RGB()
HEX = C_HEX()
def hsl2rgb(hsl):
    """Convert HSL representation towards RGB

    :param h: Hue, position around the chromatic circle (h=1 equiv h=0)
    :param s: Saturation, color saturation (0=full gray, 1=full color)
    :param l: Ligthness, Overhaul lightness (0=full black, 1=full white)
    :rtype: 3-uple for RGB values in float between 0 and 1

    Hue, Saturation, Range from Lightness is a float between 0 and 1

    Note that Hue can be set to any value but as it is a rotation
    around the chromatic circle, any value above 1 or below 0 can
    be expressed by a value between 0 and 1 (Note that h=0 is equiv
    to h=1).

    This algorithm came from:
    http://www.easyrgb.com/index.php?X=MATH&H=19#text19

    Here are some quick notion of HSL to RGB conversion:

    >>> from colour import hsl2rgb

    With a lightness put at 0, RGB is always rgbblack

    >>> hsl2rgb((0.0, 0.0, 0.0))
    (0.0, 0.0, 0.0)
    >>> hsl2rgb((0.5, 0.0, 0.0))
    (0.0, 0.0, 0.0)
    >>> hsl2rgb((0.5, 0.5, 0.0))
    (0.0, 0.0, 0.0)

    Same for lightness put at 1, RGB is always rgbwhite

    >>> hsl2rgb((0.0, 0.0, 1.0))
    (1.0, 1.0, 1.0)
    >>> hsl2rgb((0.5, 0.0, 1.0))
    (1.0, 1.0, 1.0)
    >>> hsl2rgb((0.5, 0.5, 1.0))
    (1.0, 1.0, 1.0)

    With saturation put at 0, the RGB should be equal to Lightness:

    >>> hsl2rgb((0.0, 0.0, 0.25))
    (0.25, 0.25, 0.25)
    >>> hsl2rgb((0.5, 0.0, 0.5))
    (0.5, 0.5, 0.5)
    >>> hsl2rgb((0.5, 0.0, 0.75))
    (0.75, 0.75, 0.75)

    With saturation put at 1, and lightness put to 0.5, we can find
    normal full red, green, blue colors:

    >>> hsl2rgb((0 , 1.0, 0.5))
    (1.0, 0.0, 0.0)
    >>> hsl2rgb((1 , 1.0, 0.5))
    (1.0, 0.0, 0.0)
    >>> hsl2rgb((1.0/3 , 1.0, 0.5))
    (0.0, 1.0, 0.0)
    >>> hsl2rgb((2.0/3 , 1.0, 0.5))
    (0.0, 0.0, 1.0)

    Of course:
    >>> hsl2rgb((0.0, 2.0, 0.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Saturation must be between 0 and 1.

    And:
    >>> hsl2rgb((0.0, 0.0, 1.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Lightness must be between 0 and 1.

    """
    ...

def rgb2hsl(rgb):
    """Convert RGB representation towards HSL

    :param r: Red amount (float between 0 and 1)
    :param g: Green amount (float between 0 and 1)
    :param b: Blue amount (float between 0 and 1)
    :rtype: 3-uple for HSL values in float between 0 and 1

    This algorithm came from:
    http://www.easyrgb.com/index.php?X=MATH&H=19#text19

    Here are some quick notion of RGB to HSL conversion:

    >>> from colour import rgb2hsl

    Note that if red amount is equal to green and blue, then you
    should have a gray value (from black to white).


    >>> rgb2hsl((1.0, 1.0, 1.0))  # doctest: +ELLIPSIS
    (..., 0.0, 1.0)
    >>> rgb2hsl((0.5, 0.5, 0.5))  # doctest: +ELLIPSIS
    (..., 0.0, 0.5)
    >>> rgb2hsl((0.0, 0.0, 0.0))  # doctest: +ELLIPSIS
    (..., 0.0, 0.0)

    If only one color is different from the others, it defines the
    direct Hue:

    >>> rgb2hsl((0.5, 0.5, 1.0))  # doctest: +ELLIPSIS
    (0.66..., 1.0, 0.75)
    >>> rgb2hsl((0.2, 0.1, 0.1))  # doctest: +ELLIPSIS
    (0.0, 0.33..., 0.15...)

    Having only one value set, you can check that:

    >>> rgb2hsl((1.0, 0.0, 0.0))
    (0.0, 1.0, 0.5)
    >>> rgb2hsl((0.0, 1.0, 0.0))  # doctest: +ELLIPSIS
    (0.33..., 1.0, 0.5)
    >>> rgb2hsl((0.0, 0.0, 1.0))  # doctest: +ELLIPSIS
    (0.66..., 1.0, 0.5)

    Regression check upon very close values in every component of
    red, green and blue:

    >>> rgb2hsl((0.9999999999999999, 1.0, 0.9999999999999994))
    (0.0, 0.0, 0.999...)

    Of course:

    >>> rgb2hsl((0.0, 2.0, 0.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Green must be between 0 and 1. You provided 2.0.

    And:
    >>> rgb2hsl((0.0, 0.0, 1.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Blue must be between 0 and 1. You provided 1.5.

    """
    ...

def rgb2hex(rgb, force_long=...):
    """Transform RGB tuple to hex RGB representation

    :param rgb: RGB 3-uple of float between 0 and 1
    :rtype: 3 hex char or 6 hex char string representation

    Usage
    -----

    >>> from colour import rgb2hex

    >>> rgb2hex((0.0,1.0,0.0))
    '#0f0'

    Rounding try to be as natural as possible:

    >>> rgb2hex((0.0,0.999999,1.0))
    '#0ff'

    And if not possible, the 6 hex char representation is used:

    >>> rgb2hex((0.23,1.0,1.0))
    '#3bffff'

    >>> rgb2hex((0.0,0.999999,1.0), force_long=True)
    '#00ffff'

    """
    ...

def hex2rgb(str_rgb):
    """Transform hex RGB representation to RGB tuple

    :param str_rgb: 3 hex char or 6 hex char string representation
    :rtype: RGB 3-uple of float between 0 and 1

    >>> from colour import hex2rgb

    >>> hex2rgb('#00ff00')
    (0.0, 1.0, 0.0)

    >>> hex2rgb('#0f0')
    (0.0, 1.0, 0.0)

    >>> hex2rgb('#aaa')  # doctest: +ELLIPSIS
    (0.66..., 0.66..., 0.66...)

    >>> hex2rgb('#aa')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Invalid value '#aa' provided for rgb color.

    """
    ...

def hex2web(hex):
    """Converts HEX representation to WEB

    :param rgb: 3 hex char or 6 hex char string representation
    :rtype: web string representation (human readable if possible)

    WEB representation uses X11 rgb.txt to define conversion
    between RGB and english color names.

    Usage
    =====

    >>> from colour import hex2web

    >>> hex2web('#ff0000')
    'red'

    >>> hex2web('#aaaaaa')
    '#aaa'

    >>> hex2web('#abc')
    '#abc'

    >>> hex2web('#acacac')
    '#acacac'

    """
    ...

def web2hex(web, force_long=...):
    """Converts WEB representation to HEX

    :param rgb: web string representation (human readable if possible)
    :rtype: 3 hex char or 6 hex char string representation

    WEB representation uses X11 rgb.txt to define conversion
    between RGB and english color names.

    Usage
    =====

    >>> from colour import web2hex

    >>> web2hex('red')
    '#f00'

    >>> web2hex('#aaa')
    '#aaa'

    >>> web2hex('#foo')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: '#foo' is not in web format. Need 3 or 6 hex digit.

    >>> web2hex('#aaa', force_long=True)
    '#aaaaaa'

    >>> web2hex('#aaaaaa')
    '#aaaaaa'

    >>> web2hex('#aaaa')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: '#aaaa' is not in web format. Need 3 or 6 hex digit.

    >>> web2hex('pinky')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: 'pinky' is not a recognized color.

    And color names are case insensitive:

    >>> Color('RED')
    <Color red>

    """
    ...

hsl2hex = lambda x: rgb2hex(hsl2rgb(x))
hex2hsl = lambda x: rgb2hsl(hex2rgb(x))
rgb2web = lambda x: hex2web(rgb2hex(x))
web2rgb = lambda x: hex2rgb(web2hex(x))
web2hsl = lambda x: rgb2hsl(web2rgb(x))
hsl2web = lambda x: rgb2web(hsl2rgb(x))
def color_scale(begin_hsl, end_hsl, nb):
    """Returns a list of nb color HSL tuples between begin_hsl and end_hsl

    >>> from colour import color_scale

    >>> [rgb2hex(hsl2rgb(hsl)) for hsl in color_scale((0, 1, 0.5),
    ...                                               (1, 1, 0.5), 3)]
    ['#f00', '#0f0', '#00f', '#f00']

    >>> [rgb2hex(hsl2rgb(hsl))
    ...  for hsl in color_scale((0, 0, 0),
    ...                         (0, 0, 1),
    ...                         15)]  # doctest: +ELLIPSIS
    ['#000', '#111', '#222', ..., '#ccc', '#ddd', '#eee', '#fff']

    Of course, asking for negative values is not supported:

    >>> color_scale((0, 1, 0.5), (1, 1, 0.5), -2)
    Traceback (most recent call last):
    ...
    ValueError: Unsupported negative number of colors (nb=-2).

    """
    ...

def RGB_color_picker(obj):
    """Build a color representation from the string representation of an object

    This allows to quickly get a color from some data, with the
    additional benefit that the color will be the same as long as the
    (string representation of the) data is the same::

        >>> from colour import RGB_color_picker, Color

    Same inputs produce the same result::

        >>> RGB_color_picker("Something") == RGB_color_picker("Something")
        True

    ... but different inputs produce different colors::

        >>> RGB_color_picker("Something") != RGB_color_picker("Something else")
        True

    In any case, we still get a ``Color`` object::

        >>> isinstance(RGB_color_picker("Something"), Color)
        True

    """
    ...

def hash_or_str(obj):
    ...

class Color(object):
    """Abstraction of a color object

    Color object keeps information of a color. It can input/output to different
    format (HSL, RGB, HEX, WEB) and their partial representation.

        >>> from colour import Color, HSL

        >>> b = Color()
        >>> b.hsl = HSL.BLUE

    Access values
    -------------

        >>> b.hue  # doctest: +ELLIPSIS
        0.66...
        >>> b.saturation
        1.0
        >>> b.luminance
        0.5

        >>> b.red
        0.0
        >>> b.blue
        1.0
        >>> b.green
        0.0

        >>> b.rgb
        (0.0, 0.0, 1.0)
        >>> b.hsl  # doctest: +ELLIPSIS
        (0.66..., 1.0, 0.5)
        >>> b.hex
        '#00f'

    Change values
    -------------

    Let's change Hue toward red tint:

        >>> b.hue = 0.0
        >>> b.hex
        '#f00'

        >>> b.hue = 2.0/3
        >>> b.hex
        '#00f'

    In the other way round:

        >>> b.hex = '#f00'
        >>> b.hsl
        (0.0, 1.0, 0.5)

    Long hex can be accessed directly:

        >>> b.hex_l = '#123456'
        >>> b.hex_l
        '#123456'
        >>> b.hex
        '#123456'

        >>> b.hex_l = '#ff0000'
        >>> b.hex_l
        '#ff0000'
        >>> b.hex
        '#f00'

    Convenience
    -----------

        >>> c = Color('blue')
        >>> c
        <Color blue>
        >>> c.hue = 0
        >>> c
        <Color red>

        >>> c.saturation = 0.0
        >>> c.hsl  # doctest: +ELLIPSIS
        (..., 0.0, 0.5)
        >>> c.rgb
        (0.5, 0.5, 0.5)
        >>> c.hex
        '#7f7f7f'
        >>> c
        <Color #7f7f7f>

        >>> c.luminance = 0.0
        >>> c
        <Color black>

        >>> c.hex
        '#000'

        >>> c.green = 1.0
        >>> c.blue = 1.0
        >>> c.hex
        '#0ff'
        >>> c
        <Color cyan>

        >>> c = Color('blue', luminance=0.75)
        >>> c
        <Color #7f7fff>

        >>> c = Color('red', red=0.5)
        >>> c
        <Color #7f0000>

        >>> print(c)
        #7f0000

    You can try to query unexisting attributes:

        >>> c.lightness  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: 'lightness' not found

    TODO: could add HSV, CMYK, YUV conversion.

#     >>> b.hsv
#     >>> b.value
#     >>> b.cyan
#     >>> b.magenta
#     >>> b.yellow
#     >>> b.key
#     >>> b.cmyk


    Recursive init
    --------------

    To support blind conversion of web strings (or already converted object),
    the Color object supports instantiation with another Color object.

        >>> Color(Color(Color('red')))
        <Color red>

    Equality support
    ----------------

    Default equality is RGB hex comparison:

        >>> Color('red') == Color('blue')
        False
        >>> Color('red') == Color('red')
        True
        >>> Color('red') != Color('blue')
        True
        >>> Color('red') != Color('red')
        False

    But this can be changed:

        >>> saturation_equality = lambda c1, c2: c1.luminance == c2.luminance
        >>> Color('red', equality=saturation_equality) == Color('blue')
        True


    Subclassing support
    -------------------

    You should be able to subclass ``Color`` object without any issues::

        >>> class Tint(Color):
        ...     pass

    And keep the internal API working::

        >>> Tint("red").hsl
        (0.0, 1.0, 0.5)

    """
    _hsl = ...
    def __init__(self, color=..., pick_for=..., picker=..., pick_key=..., **kwargs) -> None:
        ...
    
    def __getattr__(self, label):
        ...
    
    def __setattr__(self, label, value):
        ...
    
    def get_hsl(self):
        ...
    
    def get_hex(self):
        ...
    
    def get_hex_l(self):
        ...
    
    def get_rgb(self):
        ...
    
    def get_hue(self):
        ...
    
    def get_saturation(self):
        ...
    
    def get_luminance(self):
        ...
    
    def get_red(self):
        ...
    
    def get_green(self):
        ...
    
    def get_blue(self):
        ...
    
    def get_web(self):
        ...
    
    def set_hsl(self, value):
        ...
    
    def set_rgb(self, value):
        ...
    
    def set_hue(self, value):
        ...
    
    def set_saturation(self, value):
        ...
    
    def set_luminance(self, value):
        ...
    
    def set_red(self, value):
        ...
    
    def set_green(self, value):
        ...
    
    def set_blue(self, value):
        ...
    
    def set_hex(self, value):
        ...
    
    set_hex_l = ...
    def set_web(self, value):
        ...
    
    def range_to(self, value, steps):
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self):
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    if sys.version_info[0] == 2:
        ...


RGB_equivalence = lambda c1, c2: c1.hex_l == c2.hex_l
HSL_equivalence = lambda c1, c2: c1._hsl == c2._hsl
def make_color_factory(**kwargs_defaults):
    ...
