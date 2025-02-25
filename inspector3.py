import xml.etree.ElementTree as ET

with open("page_source.txt", "r") as f:
    # 解析 XML
    root = ET.fromstring(f.read())

# 定位到 Table
for table in root.findall(".//XCUIElementTypeTable"):
    for row in table.findall("./XCUIElementTypeTableRow"):
        cell = row.find("./XCUIElementTypeCell")
        if cell is not None:
            static_text = cell.find("./XCUIElementTypeStaticText")
            if static_text is not None and "value" in static_text.attrib:
                print(static_text.attrib["value"])
