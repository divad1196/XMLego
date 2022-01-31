
# 1. I want to be able to keep track on templates lazily:
#    Don't load them when not needed => use Template loader
#    Nb: Template may be loaded using different loader

class BaseTemplateLoader:
    def load(xmlid):
        raise Exception("Undefined Loading")

class DefaultTemplateLoader:
    def __init__(self):
        super(XMLego, self).__init__()
        self._templates = {}

    def add_template(self, xml):
        xmlid = xml.attrib["id"]
        self._templates[xmlid] = xml

    def from_files(self, *files):
        for f in files:
            tree = etree.parse(f)
            templates = tree.getroot().findall("template")  # use xpath instead?
            for t in templates:
                self.add_template(t)

    def load(self, xmlid):
        return self._templates[xmlid]


class XMLego:
    def __init__(self, loader=DefaultTemplateLoader()):
        super(XMLego, self).__init__()
        self._templates = {}
        self._loader = loader
    
    @property
    def loader(self):
        return self._loader

    def add_template(self, xml, loader=None):
        xmlid = self._make_id(xml.attrib["id"])
        inherits = xml.attrib.get("inherits")
        pool = []
        if inherits:
            pool = self._templates.setdefault(inherits, [])
        

        # graph = self._templates.get(xmlid)
        # if graph:  # Redefinition
        #     if inherits is None:  # We can override
        # else:  # New node
        #     if inherits is None:
        #         graph = igraph.Graph(directed=True)
        #     else:
        #         graph = self._templates.get(inherits)
        
        # graph.add_vertex(id, id=id, template=xml, inherits=inherits)


# graph = igraph.Graph(directed=True)
# graph.add_vertex   # Add vertex "node"
# graph.bfsiter(0)   # Iter over vertex
# graph.vs.find("test")  # Get vertex by its name