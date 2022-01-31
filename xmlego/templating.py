# import imp
import imp
from lxml import etree
from .utils import copy_element, insert_after, print_xml, remove_element, clear_element
from itertools import chain
from .code import eval_code, exec_code

FOR_VALUE_ATTR = "t-foreach"
FOR_AS_ATTR = "t-as"

VAR_TAG = "t-set"
VAR_TAG_VALUE = "value"
VAR_TAG_AS = "as"

TEXT_ATTR = "t-text"

TRANSIENT_TAG = "t"
# This is meant to avoid name colision when injecting in exec_code
TEMP_VAR_NAME = "rewqrewvnkjvnkrntlwkqerjweholifuhlnrkjnqlrekwjcvhdlsiurenqwlfkjnfdasfsd"
ATTR_EVAL_PREFIX = "t-att-"
ATTR_EVAL_PREFIX_LEN = len(ATTR_EVAL_PREFIX)

ATTR_IF = "t-if"
ATTR_ELIF = "t-elif"
ATTR_ELSE = "t-else"

def remove_transient_tags(xml):
    transients = chain(
        xml.xpath(".//{}".format(TRANSIENT_TAG)),
        xml.xpath(".//{}".format(VAR_TAG))
    )
    for t in transients:
        clear_element(t)

def eval_xml_for(xml, variables=None, globals=None):
    if variables is None:
        variables = {}

    # Retrieve data
    values_code = "({})".format(xml.attrib[FOR_VALUE_ATTR])
    as_attr = "({}) = {}".format(
        xml.attrib[FOR_AS_ATTR],
        TEMP_VAR_NAME
    )
    values = eval_code(values_code, globals, locals=variables)

    # We need a common parent and clear the current content
    tmp = etree.Element(TRANSIENT_TAG)
    tmp.extend(xml.getchildren())
    xml.clear()

    for it in values:
        # Prepare loop
        loop_vars = {TEMP_VAR_NAME: it}
        exec_code(as_attr, globals=globals, locals=loop_vars)
        loop_vars.pop(TEMP_VAR_NAME)
        local_vars = {**variables, **loop_vars}

        # Handle iteration
        res, _ = _eval_xml(copy_element(tmp), local_vars, globals=globals)
        xml.append(res)

        # Update variables
        for k in loop_vars:
            local_vars.pop(k, None)
        variables.update(local_vars)
    return xml

def eval_xml_variable(xml, variables=None, globals=None):
    if variables is None:
        variables = {}

    # Retrieve data
    values_code = "({})".format(xml.attrib[VAR_TAG_VALUE])
    as_attr = "({}) = {}".format(
        xml.attrib[VAR_TAG_AS],
        TEMP_VAR_NAME
    )
    value = eval_code(values_code, globals, locals=variables)
    variables[TEMP_VAR_NAME] = value
    exec_code(as_attr, globals=globals, locals=variables)
    variables.pop(TEMP_VAR_NAME)


def eval_xml_text(xml, variables=None, globals=None):
    code = xml.get(TEXT_ATTR)
    if code is None:
        return code
    text = eval_code(code, globals=globals, locals=variables)
    xml.text = (xml.text or "") + str(text)
    xml.attrib.pop(TEXT_ATTR)

def eval_xml_condition(xml, next_elements=[], variables=None, globals=None):
    """
        xml: The current node
        next_elements: the next elements that may contain elif or else statement
    """
    cond = xml.attrib[ATTR_IF]
    to_check = [(xml, cond)]
    for el in next_elements:
        cond = el.attrib.get(ATTR_ELIF)
        if cond is not None:
            to_check.append((el, cond))
            continue
        if ATTR_ELSE in el.attrib:
            to_check.append((el, "True"))
        break
    
    # Remove elements from processing list
    next_elements = next_elements[len(to_check) - 1:]

    ok = None
    while to_check:
        el, cond = to_check.pop(0)
        if ok is not None or not eval_code(cond, globals=globals, locals=variables):
            remove_element(el)
            continue
        # The condition is okay
        ok = el
        for attr in (ATTR_IF, ATTR_ELIF, ATTR_ELSE):
            el.attrib.pop(attr, None)
    _eval_xml(el, variables, globals=globals)
    return next_elements


def eval_xml_attributes(xml, variables=None, globals=None):
    dynamic_attrs = (
        (k, k[ATTR_EVAL_PREFIX_LEN:], code)
        for k, code in xml.attrib.items()
        if k.startswith(ATTR_EVAL_PREFIX)
    )
    for dyn, attr, code in dynamic_attrs:
        text = str(eval_code(code, globals=globals, locals=variables))
        xml.attrib[attr] = text
        xml.attrib.pop(dyn)
   
def _eval_xml(xml, variables=None, globals=None):
    if variables is None:
        variables = {}
    
    # Nb: Thoses functions will edit the tree IN-PLACE! Do a copy before any call if needed
    if FOR_VALUE_ATTR in xml.attrib:
        eval_xml_for(xml, variables=variables, globals=globals)
        return xml, variables

    if xml.tag == VAR_TAG:
        eval_xml_variable(xml, variables=variables, globals=globals)
        return xml, variables

    children = xml.getchildren()
    while children:
        child = children.pop(0)
        if ATTR_IF in child.attrib:
            children = eval_xml_condition(child, children, variables=variables, globals=globals)
        else:
            _eval_xml(child, variables=variables, globals=globals)
        
    eval_xml_text(xml, variables=variables, globals=globals)
    eval_xml_attributes(xml, variables=variables, globals=globals)
    return xml, variables


def eval_xml(xml, variables=None, globals=None, preserve=False):
    if preserve:
        xml = copy_element(xml)
    if variables is None:
        variables = {}
    xml, _ = _eval_xml(xml, variables=variables, globals=globals)
    remove_transient_tags(xml)
    return xml, variables