import xml.etree.ElementTree as ET

def convert(data):
  xml = '<Annotations MicronsPerPixel="0.499000">\n' + '<Annotation Id="1" Name="" ReadOnly="0" NameReadOnly="0" LineColorReadOnly="0" Incremental="0" Type="4" LineColor="65535" Visible="1" Selected="1" MarkupImagePath="" MacroName="">\n' + '<Attributes>\n' + '<Attribute Name="Description" Id="0" Value=""/>\n' + '</Attributes>\n' + '<Regions>\n' + '<RegionAttributeHeaders>\n' + '<AttributeHeader Id="9999" Name="Region" ColumnWidth="-1"/>\n' + '<AttributeHeader Id="9997" Name="Length" ColumnWidth="-1"/>\n' + '<AttributeHeader Id="9996" Name="Area" ColumnWidth="-1"/>\n' + '<AttributeHeader Id="9998" Name="Text" ColumnWidth="-1"/>\n' + '<AttributeHeader Id="1" Name="Description" ColumnWidth="-1"/>\n' + '</RegionAttributeHeaders>\n'
  
  for index, annotation in enumerate(data['left']):
    id = index+1
    selector = annotation['target']['selector']
    vertices = ""
    type = 0
    #print(selector)
    if selector['type'] == 'FragmentSelector':
      coords = [float(i) for i in selector['value'].split(":")[1].split(",")]
      vertices = '<Vertex X="{x}" Y="{y}" Z="0"/>\n'.format(x=coords[0], y=coords[1]) + '<Vertex X="{x}" Y="{y}" Z="0"/>\n'.format(x=coords[0]+coords[2], y=coords[1]) + '<Vertex X="{x}" Y="{y}" Z="0"/>\n'.format(x=coords[0]+coords[2], y=coords[1]+coords[3]) + '<Vertex X="{x}" Y="{y}" Z="0"/>'.format(x=coords[0], y=coords[1]+coords[3])
      type = 1
    elif selector['type'] == 'SvgSelector':
      root = ET.fromstring(selector['value'])
      for child in root:
        if child.tag == "polygon":
          points = list(map(lambda x: x.split(",") , child.attrib['points'].split(" ")))
          vertices = "\n".join(list(map(lambda x: '<Vertex X="{a}" Y="{b}" Z="0"/>'.format(a=x[0], b=x[1]) , points)))
          type = 0
  
        elif child.tag == "circle":
          cx = float(child.attrib['cx'])
          cy = float(child.attrib['cy'])
          r = float(child.attrib['r'])
          vertices = '<Vertex X="{a}" Y="{b}" Z="0"/>\n'.format(a=cx-r, b=cy-r) + '<Vertex X="{a}" Y="{b}" Z="0"/>'.format(a=cx+r, b=cy+r)
          type = 2
  
        elif child.tag == "ellipse":
          cx = float(child.attrib['cx'])
          cy = float(child.attrib['cy'])
          rx = float(child.attrib['rx'])
          ry = float(child.attrib['ry'])
          vertices = '<Vertex X="{a}" Y="{b}" Z="0"/>\n'.format(a=cx-rx, b=cy-ry) + '<Vertex X="{a}" Y="{b}" Z="0"/>'.format(a=cx+rx, b=cy+ry)
          type = 2
  
        elif child.tag == "path":
          commands = child.attrib['d'].split(' ')
          for i in range(len(commands)):
            type = commands[i][0]
  
            if type=='M' or type=='L':
              x = float(commands[i][1:])
              y = float(commands[i+1])
              vertices += '<Vertex X="{a}" Y="{b}" Z="0"/>\n'.format(a=x, b=y)
              i = i+1
          type = 0
  
    xml += '<Region Id="{id}" Type="{type}" Zoom="0.669026" Selected="0" ImageLocation="" ImageFocus="-1" Length="0" Area="0" LengthMicrons="0" AreaMicrons="0" Text="" NegativeROA="0" InputRegionId="0" Analyze="1" DisplayId="{id}">\n'.format(id=id, type=type) + '<Attributes></Attributes>\n' + '<Vertices>\n' + vertices + '</Vertices>\n' + '</Region>\n';
              
   
  xml += '</Regions>\n' + '<Plots></Plots>\n' + '</Annotation>\n' + '</Annotations>';
  
  return xml