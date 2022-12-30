
def property(prop, value):
    return f'{prop}: {value};'




def css(css_values):
    for selector, properties in css_values.items():
        print(selector + '{')
        for prp, vl in properties.items():
            print('    ', property(prp, vl))
        print('}')

values = {
    '#sheep1': {'top': str(round(100 * 700/1920, 4)) + '%',
                'left': str(round(100 * 450/1920, 4)) + '%',
                'width': str(round(100 * 150/1920, 4)) + '%'},
    '#sheep2': {'top': str(round(100 * 375/1920, 4)) + '%',
                'left': str(round(100 * 450/1920, 4)) + '%',
                'width': str(round(100 * 150/1920, 4)) + '%'},
    '#shop': {'top': str(round(100 * 560/1920, 4)) + '%',
                'left': str(round(100 * 1260/1920, 4)) + '%',
                'width': str(round(100 * 400/1920, 4)) + '%'},
    '#game': {'top': str(round(100 * 850/1920, 4)) + '%',
                'left': str(round(100 * 375/1920, 4)) + '%',
                'width': str(round(100 * 140/1920, 4)) + '%'},
    '#nanimoshitakunai': {'top': str(round(100 * 240/1920, 4)) + '%',
                'left': str(round(100 * 610/1920, 4)) + '%',
                'width': str(round(100 * 504/1920, 4)) + '%'},
}

css(values)

