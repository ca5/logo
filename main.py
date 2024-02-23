
import xml.etree.ElementTree as ET
from cairosvg import svg2png
import functions_framework
import flask
from tempfile import NamedTemporaryFile

RAW_LOGO_SVG = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%" height="100%" viewBox="0 0 500 500" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(1.2285,0,0,1.15741,-65.1106,-59.0278)">
        <g id="background">
            <rect x="53" y="51" width="407" height="432"/>
        </g>
    </g>
    <g id="Layer-1" serif:id="Layer 1">
        <g id="path4443" transform="matrix(1.55447,0,0,1.54851,56.7831,23.4663)">
            <path d="M92.096,202.545L92.096,163.974L131.382,163.974L131.382,124.688L40.668,124.688L40.668,112.545L156.382,112.545L156.382,202.545L92.096,202.545ZM131.382,189.688L131.382,176.831L117.811,176.831L117.811,189.688L131.382,189.688Z" style="fill:rgb(255,255,254);fill-rule:nonzero;"/>
        </g>
        <g id="path4445" transform="matrix(1.55447,0,0,1.54851,56.7831,23.4663)">
            <path d="M40.668,228.26L40.668,138.26L117.811,138.26L117.811,151.117L79.239,151.117L79.239,215.402L117.811,215.402L117.811,228.26L40.668,228.26Z" style="fill:rgb(255,255,254);fill-rule:nonzero;"/>
        </g>
        <g id="path4466" transform="matrix(1.55556,0,0,1.54851,56.3667,23.4663)">
            <path d="M131.621,228.259L131.621,215.402L170.193,215.402L170.193,98.974L40.907,98.974L40.907,60.402L208.05,60.402L208.05,73.259L78.764,73.259L78.764,86.831L208.05,86.831L208.05,228.259L131.621,228.259Z" style="fill:rgb(255,255,254);fill-rule:nonzero;"/>
        </g>
    </g>
</svg>
'''

def set_svg_background_color(xml_tree, color):
    background_rect = xml_tree.find(
        '{http://www.w3.org/2000/svg}g'
    ).find(
        '{http://www.w3.org/2000/svg}g'
    ).find(
        '{http://www.w3.org/2000/svg}rect'
    )

    background_rect.set('fill', color)
    return xml_tree
    
def set_svg_foreground_color(xml_tree, index, color):
    foreground_path = xml_tree.findall(
        '{http://www.w3.org/2000/svg}g'
    )[1].findall(
        '{http://www.w3.org/2000/svg}g'
    )[index].find(
        '{http://www.w3.org/2000/svg}path'
    )

    foreground_path.set('style', f"fill:{color};fill-rule:nonzero;")
    return xml_tree

def save_as_png(root, output_path, width, height):
    svg_data = ET.tostring(root, encoding='utf-8', method='xml')
    svg2png(bytestring=svg_data, write_to=output_path, output_width=width, output_height=height)

@functions_framework.http
def main(request: flask.Request) -> flask.typing.ResponseReturnValue:
    output_png_path = 'ca5logo.png'

    # default setting
    output_width = 500# 
    background_color = '296A01'
    c_color = 'FFFFFF'
    a_color = 'FFFFFF'
    five_color = 'FFFFFF'

    request_args = request.args
    output_width = int(request_args.get('w', output_width))
    background_color = request_args.get('bg', background_color)
    c_color = request_args.get('c', c_color)
    a_color = request_args.get('a', a_color)
    five_color = request_args.get('5', five_color)

    tree = ET.fromstring(RAW_LOGO_SVG)
    tree = set_svg_background_color(tree, "#" + background_color)
    tree = set_svg_foreground_color(tree, 0, "#" + c_color)
    tree = set_svg_foreground_color(tree, 1, "#" + a_color)
    tree = set_svg_foreground_color(tree, 2, "#" + five_color)

    with NamedTemporaryFile() as tmpf:
        save_as_png(tree, tmpf.name, output_width, output_width)
        return flask.send_file(
            tmpf.name,
            as_attachment=False,
            download_name="ca5logo.png")
