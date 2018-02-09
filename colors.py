#!/usr/bin/python3
import sys

base16 = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

def convertToDecimal(hex):
    digits = hex.lower()
    if len(digits) == 1:
        digits += digits
    digitSequence = reversed(list(digits))
    decimal = 0
    for index, value in enumerate(digitSequence):
        number = 0
        if value in base16:
            number = base16[value]
        else:
            number = int(value)
        decimal += number * (16 ** index)
    return decimal

def hexToRGB(rgbString):
    colors = {}
    if len(rgbString) == 3:
        colors['r'] = convertToDecimal(rgbString[0])
        colors['g'] = convertToDecimal(rgbString[1])
        colors['b'] = convertToDecimal(rgbString[2])
    elif len(rgbString) == 6:
        colors['r'] = convertToDecimal(rgbString[0:2])
        colors['g'] = convertToDecimal(rgbString[2:4])
        colors['b'] = convertToDecimal(rgbString[4:6])
    return colors

def calculateLuminance(min, max):
    return (min + max) / 2

def calculateSaturation(R, G, B):
    minimum = min(R, G, B)
    maximum = max(R, G, B)
    luminance = calculateLuminance(minimum, maximum)

    if luminance < 0.5:
        saturation = (maximum - minimum) / (maximum + minimum)
    elif luminance > 0.5:
        saturation = (maximum - minimum) / (2.0 - maximum - minimum)
    elif luminance == 0.5 and minimum != maximum:
        saturation = 1.0
    else:
        saturation = 0

    return saturation



def calculateHue(R, G, B):
    minimum = min(R, G, B)
    maximum = max(R, G, B)

    if R == maximum:
        hue = (G - B) / (maximum - minimum)
    elif G == maximum:
        hue = 2.0 + ((B - R) / (maximum - minimum))
    elif B == maximum:
        hue = 4.0 + ((R - G) / (maximum - minimum))
    # Convert to degrees 
    hue *= 60

    if hue < 0:
        hue += 360

    return hue

def RGBtoHSL(rgb):
    hsl = {}
    R = rgb['r'] / 255.0
    G = rgb['g'] / 255.0
    B = rgb['b'] / 255.0
    minimum = min(R, G, B)
    maximum = max(R, G, B)
    if minimum != maximum:
        hue = calculateHue(R, G, B)
        saturation = calculateSaturation(R, G, B) 
    else:
        hue = 0
        saturation = 0

    hsl['h'] = hue
    hsl['s'] = saturation
    hsl['l'] = calculateLuminance(minimum, maximum)

    return hsl

def HSLtoRGB(hsl):
    chroma = (1 - abs(2 * hsl['l'] - 1)) * hsl['s']
    hue = hsl['h'] / 60
    x = chroma * (1 - abs((hue % 2) - 1))
    intermediateRGB = {}
    if 0 <= hue and hue <= 1:
        intermediateRGB = {'r': chroma, 'g': x, 'b': 0}
    elif 1 <= hue and hue <= 2:
        intermediateRGB = {'r': x, 'g': chroma, 'b': 0}
    elif 2 <= hue and hue <= 3:
        intermediateRGB = {'r': 0, 'g': chroma, 'b': x}
    elif 3 <= hue and hue <= 4:
        intermediateRGB = {'r': 0, 'g': x, 'b': chroma}
    elif 4 <= hue and hue <= 5:
        intermediateRGB = {'r': x, 'g': 0, 'b': chroma}
    elif 5 <= hue and hue <= 6:
        intermediateRGB = {'r': chroma, 'g': 0, 'b': x}
    else:
        print('Something went very, very wrong')
        print('value of "hue": ' + hue)
        exit(1)

    m = hsl['l'] - 0.5 * chroma
    rgb = {'r': 255 * (intermediateRGB['r'] + m), 'g': 255 * (intermediateRGB['g'] + m), 'b': 255 * (intermediateRGB['b'] + m)}
    return rgb

try:
    hex_color = sys.argv[1]
except:
    print('Please provide a hex color as an argument. If you did, and are seeing this message, try removing the "#".')
    exit()
if len(hex_color) != 3 and len(hex_color) != 6:
    print('Error: Malformed color.')
    exit()
rgb = hexToRGB(hex_color)
print("Hex Color: #%s" % hex_color)
print("RGB representation: %s" % rgb)
print("HSL representation: %s" % RGBtoHSL(rgb))
print("RGB as converted from HSL: %s" % HSLtoRGB(RGBtoHSL(rgb)))

