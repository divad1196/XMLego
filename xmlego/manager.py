# Link resolver and loader together
# import igraph as ig

from .resolver import DefaultResolver
from .utils import copy_element, apply_xpath

class DefaultManager:
    """
        Simpliest Manager:
        - Store all nodes
        - Parent nodes must be loaded first
    """
    def __init__(self, resolver=DefaultResolver()):
        super(DefaultManager, self).__init__()
        self._resolver = resolver

    def add_template(self, xml):
        xmlid = xml.attrib["id"]
        inherits = xml.attrib.get("inherits")
        self._templates[xmlid] = xml
        self._resolver.add_template(xmlid, inherits)

    def load(self, xmlid):
        base, *children = self._resolver.resolve(xmlid)
        base = copy_element(self._templates[base])
        for c in children:
            xml = self._templates[c]
            for xpath in xml.xpath("xpath"):
                apply_xpath(base, xpath)
