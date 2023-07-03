import xml.etree.ElementTree as ET
import json as js
import unittest
import os

def convert(tree):

  json = {"left":[], "right":[]}

  root = tree.getroot()

  for child in root[0][1]:
    if child.tag=="RegionAttributeHeaders":
      continue
    appendage = {"type": "Annotation", "body": [], "target": {"source": "https://datacommons.swmed.edu/scopeviewer/undefined", "selector": {}}, "@context": "http://www.w3.org/ns/anno.jsonld", "id": "#00000000-0000-0000-0000-000000000000"}
    type = int(child.attrib['Type'])
    vertices = child[1]
    if type==1:
      bl = vertices[0].attrib
      tr = vertices[2].attrib
      a=bl['X']
      b=bl['Y']
      c=float(tr['X'])-float(bl['X'])
      d=float(tr['Y'])-float(bl['Y'])
      value = "xywh=pixel:{a},{b},{c},{d}".format(a=a, b=b, c=c, d=d)
      appendage['target']['selector']['type'] = "FragmentSelector"
      appendage['target']['selector']['conformsTo'] = "http://www.w3.org/TR/media-frags/"
      appendage['target']['selector']['value'] = value
    else:
      appendage['target']['selector']['type'] = "SvgSelector"
      if type==0:
        vertex_string = ""
        for index, i in enumerate(vertices):
          letter = 'L'
          if index==0:
            letter = 'M'
          vertex_string = vertex_string + (letter + i.attrib['X'] + ' ' + i.attrib['Y'] + ' ')
        vertex_string = "<svg><path d=\"" + vertex_string[:-1] + "\"></path></svg>"
        appendage['target']['selector']['value'] = vertex_string
      elif type==2:
        vertex_string = ""
        bl = [float(vertices[0].attrib['X']), float(vertices[0].attrib['Y'])]
        tr = [float(vertices[1].attrib['X']), float(vertices[1].attrib['Y'])]
        cx = (tr[0]+bl[0])/2
        cy = (tr[1]+bl[1])/2
        rx = (tr[0]-bl[0])/2
        ry = (tr[1]-bl[1])/2
        vertex_string = vertex_string + " cx=\"" + str(cx) + "\""
        vertex_string = vertex_string + " cy=\"" + str(cy) + "\""
        vertex_string = vertex_string + " rx=\"" + str(rx) + "\""
        vertex_string = vertex_string + " ry=\"" + str(ry) + "\""
        vertex_string = "<svg><ellipse{a}></circle></svg>".format(a=vertex_string)
        appendage['target']['selector']['value'] = vertex_string
    json["left"].append(appendage)
  return json
  



class TestConversion(unittest.TestCase):
    def runTest(self):
        tree = ET.parse('XMLunittest.xml')
        json = convert(tree)
        with open("output.json", "w") as outfile:
          js.dump(json, outfile)
        f = open('XMLunittest.json')
        xml_unittest = js.load(f)
        f = open('output.json')
        xml_testing = js.load(f)
        
        
        
        self.assertEqual(xml_testing, xml_unittest, "Doesn't Match")
 
# run the test
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


