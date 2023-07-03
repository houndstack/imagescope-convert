import json
import pathlib
import os
from converter import convert
import unittest
import xml.etree.ElementTree as ET

class TestConversion(unittest.TestCase):
    def runTest(self):
        f = open('unittest.json')
        data = json.load(f)
        xml_data = convert(data)
        with open("testing.xml", "w") as f:
          f.write(xml_data)
        xml_unittest = ET.tostring(ET.parse('unittest.xml').getroot(), encoding='unicode')
        xml_testing = ET.tostring(ET.parse('testing.xml').getroot(), encoding='unicode')
        
        
        self.assertEqual(xml_testing, xml_unittest, "Doesn't Match")
 
# run the test
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
  
for json_file in pathlib.Path('').glob('*.json'):
  f = open(json_file)
  data = json.load(f)
  xml = convert(data)
  xml_file_path = os.path.splitext(json_file)[0] + ".xml"
  with open(xml_file_path, "w") as f:
      f.write(xml)
  print("Saved to {path}".format(path=xml_file_path))

  


