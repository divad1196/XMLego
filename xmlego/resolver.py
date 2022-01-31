import igraph as ig
from .utils import reverse_topological_order

class DefaultResolver:
    def __init__(self):
        super(DefaultResolver, self).__init__()
        self._graph = ig.Graph(directed=True)

    def add_template(self, xmlid, inherits=None):
        self._graph.add_vertex(xmlid)
        if inherits is not None:
            self._graph.add_edge(xmlid, inherits)

    def _subgraph(self, xmlid):
        return self._graph.subgraph(self._graph.subcomponent(xmlid))

    def resolve(self, xmlid):
        g = self._subgraph(xmlid)
        vertices = reverse_topological_order(g)
        return vertices["name"]


r = DefaultResolver()
r.add_template("a")
r.add_template("b", "a")
r.add_template("c", "a")
r.add_template("d", "b")


r.add_template("e")
r.add_template("f", "e")
r.add_template("g", "e")
r.add_template("h", "f")
