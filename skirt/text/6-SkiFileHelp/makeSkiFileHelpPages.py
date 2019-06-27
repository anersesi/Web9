#!/usr/bin/env python
# -*- coding: utf8 -*-

# This Python script generates Doxygen input pages from the contents of the skirt.smile schema definition file.
# To be completed.
#
# The script is executed as part of the "makeHTML" process, *before* running Doxygen on this part of the web site.
# It accepts two optional command line arguments specifying the directory holding the skirt.smile file
# and the directory holding the output file(s) of this script (i.e. input for Doxygen).
#
# Developer note: this script has been developed and tested with Python 3.7.2.
#

# -----------------------------------------------------------------

import sys
import lxml.etree as etree

# -----------------------------------------------------------------

## This function returns an attribute value or element tag as a string. The first argument is an XPath expression
# relative to the document root that selects exactly one element. The second argument is an attribute name string
# or None. In the latter case, the element tag (corresponding to the SMILE property or type name) is returned.
# If the element is not found, there are multiple elements, or the selected element does not have the specified
# attribute, an error is raised.
def getStringAttribute(smiletree, xpath, attribute):
    # get the element(s) and verify there is exactly one
    elems = smiletree.xpath(xpath)
    if len(elems) == 0: raise ValueError("Smile file has no element for xpath '{}'".format(xpath))
    if len(elems) > 1: raise ValueError("Smile file has multiple elements for xpath '{}'".format(xpath))
    elem = elems[0]
    if not etree.iselement(elem): raise ValueError("Smile file xpath '{}' returns a non-element".format(xpath))

    # get the attribute value or the element tag
    value = elem.get(attribute) if attribute is not None else elem.tag
    if not isinstance(value, str): raise ValueError("Smile file element for xpath '{}' has no attribute '{}'" \
                                                    .format(xpath, attribute))
    return value

## This function returns a list including the string values of a particular attribute for a number of elements.
# The first argument is an XPath expression relative to the document root that selects one or more elements.
# The second argument is the attribute name (the attribute must be present for all selected elements).
# If the attribute argument is None, the element tags (corresponding to SMILE type names) are returned instead.
# If no elements are found, the function returns an empty list. If one or more of the selected element does
# not have the specified attribute, an error is raised.
def getStringAttributes(smiletree, xpath, attribute):
    values = []
    # loop over the element(s)
    for elem in smiletree.xpath(xpath):
        if not etree.iselement(elem): raise ValueError("Smile file xpath '{}' returns a non-element".format(xpath))
        # get the attribute value or the element tag
        value = elem.get(attribute) if attribute is not None else elem.tag
        if not isinstance(value, str): raise ValueError("Smile file element for xpath '{}' has no attribute '{}'" \
                                                        .format(xpath, attribute))
        values.append(value)
    return values

# -----------------------------------------------------------------

# returns True if the candidate item inherits the base item, or False if not.
def inheritsItem(smiletree, candidate, base):

    while True:
        # if the candidate matches the base type (possibly after iteration), there is inheritance
        if candidate == base:
            return True
        # if the candidate matches the topmost type (usually after iteration), there is no inheritance
        if candidate == "SimulationItem":
            return False
        # replace the candidate by the candidate's base type and try again
        candidate = getStringAttribute(smiletree, "//Type[@name='{}']".format(candidate), "base")

# -----------------------------------------------------------------

# get the directory holding the skirt.smile file
smiledir = sys.argv[1] if len(sys.argv)>1 else "."
if not smiledir.endswith("/"): smiledir += "/"

# get the output file directory
outdir = sys.argv[2] if len(sys.argv)>2 else "."
if not outdir.endswith("/"): outdir += "/"

# -----------------------------------------------------------------

# load the XML tree from the smile file
smiletree = etree.parse(smiledir+"skirt.smile")

# get the SKIRT version
version = getStringAttribute(smiletree, "//smile-schema", "producer")
print (version)
print ()

# get the set of simulation items that are mentioned as a base in Item or ItemList properties
list0 = getStringAttributes(smiletree, "//Schema", "type")
list1 = getStringAttributes(smiletree, "//ItemProperty", "base")
list2 = getStringAttributes(smiletree, "//ItemListProperty", "base")
baseItems = sorted(set(list0+list1+list2))

# get the list of concrete simulation items
concreteItems = getStringAttributes(smiletree, "//Type[@concrete='true']", "name")

# for each base item...
for baseItem in baseItems:
    print ("->", baseItem)

    # get the concrete items inheriting from it
    inheritingItems = sorted([ item for item in concreteItems if inheritsItem(smiletree, item, baseItem) ])

    # for each inheriting item...
    for item in inheritingItems:
        print ("     ", item)

        # get a list of XML elements representing the properties of this item, including inherited properties,
        # split between scalar and compound properties, and otherwise in the order they would appear in the Q&A
        # ...


# -----------------------------------------------------------------
