from xml.dom import minidom

from typing import List, Tuple, Optional

class ParseError(Exception):
    """SVG 'generate_outline' parse error"""

def generate_outline(file: str) -> List[Tuple[float, float]]:
    with minidom.parse(file) as doc:

        views = doc.getElementsByTagName("g")

        if len(views) != 1:
            raise ParseError("Does not seem to have a <g> tag (?)")
        
        view = views[0]
        pathnodes = view.getElementsByTagName("path")

        if len(pathnodes) != 1:
            print(pathnodes)
            raise ParseError("No or more than one path node found (?)")

        transform = view.getAttribute("transform")
        path = pathnodes[0].getAttribute("d")
    
    return (transform, path)

def _main():
    print(generate_outline("example/pi.svg"))

if __name__ == "__main__":
    _main()