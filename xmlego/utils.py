from lxml import etree
import copy
import igraph

ig = igraph


def print_xml(xml):
    print(etree.tostring(xml, pretty_print=True).decode())


def copy_element(xml):
    return copy.deepcopy(xml)


def insert_after(xml, elements):
    for el in reversed(elements):
        xml.addnext(el)


def insert_before(xml, elements):
    for el in elements:
        xml.addprevious(el)


def remove_element(xml):
    xml.getparent().remove(xml)


def clear_element(xml):
    children = xml.getchildren()
    insert_after(xml, children)
    remove_element(xml)


def _get_position_handler(element, position):
    setter = None
    if position == "after":
        setter = insert_after
    elif position == "before":
        setter = insert_before

    def handler(children, element=element, setter=setter):
        setter(element, children)

    return handler


def apply_xpath(base, xpath):
    expr = xpath.attrib["expr"]
    position = xpath.attrib["position"]
    elements = base.xpath(expr)
    for el in elements:
        handler = _get_position_handler(el, position)
        handler(xpath.getchildren())


def to_graph(templates, graph=None):
    if graph is None:
        graph = igraph.Graph(directed=True)
    # Add all template as vertices
    for t in templates:
        id = t.attrib["id"]
        inherits = t.attrib.get("inherits")
        graph.add_vertex(id, id=id, template=t, inherits=inherits)
    # Add the edges
    edges = []
    for v in graph.vs:
        attrs = v.attributes()
        inherits = attrs.get("inherits")
        if inherits:
            edges.append((attrs["id"], inherits))  # child, parent
    graph.add_edges(edges)
    return graph


def plot_graph(graph):
    ig.plot(graph, vertex_label=graph.vs["name"])


def has_cycles(graph):
    return not graph.is_dag()


def split_graph(graph):
    return graph.decompose("weak")  # Split unconnected graphs


def reverse_topological_order(graph):
    return graph.vs.select(reversed(graph.topological_sorting()))


def graph_resolve_order(graph):
    # We use the reversed topological order to ensure that the first node is the base
    # We could have used bfs or dfs algorithm instead as long as the first value is the top node of the "tree"
    vertices = reverse_topological_order(graph)
    templates = (v.attributes()["template"] for v in vertices)
    base = next(templates)
    return base, templates


def _solve_graph(graph):
    base, templates = graph_resolve_order(graph)
    for t in templates:
        for xpath in t.xpath("xpath"):
            apply_xpath(base, xpath)
    return base


def solve_graph(graph):
    # TODO: add check for cycles
    if has_cycles(graph):
        raise Exception("has cycle")
    return [_solve_graph(g) for g in split_graph(graph)]
