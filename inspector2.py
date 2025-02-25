from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.mac import Mac2Options
import time
import xml.etree.ElementTree as ET

# **配置 Appium 选项**
options = Mac2Options()
options.bundle_id = 'com.tencent.WeWorkMac'  # 指定企业微信
options.platform_name = 'mac'
options.automation_name = 'mac2'
options.set_capability("autoLaunch", False)
options.set_capability("forceAppLaunch", False)  # 不强制启动应用
options.set_capability("useRunningApp", True)  # 连接已经运行的企业微信
options.set_capability("shouldUseSingletonTestManager", True)  # 避免重复创建 WDA 实例
options.set_capability("wdaLocalPort", 8100)  # 绑定已有 WDA，防止重启应用
# 绑定已有进程id
options.set_capability("processId", '8365')  # 替换为实际的进程 ID
options.set_capability("connectHardwareKeyboard", True)  # 连接但不干扰输入法

# **初始化 driver**
driver = webdriver.Remote('http://localhost:4723', options=options)

# 提示按回车键继续
input("请按回车键继续...")
page_source = driver.page_source
# 保存到文件中
with open("page_source_3.xml", "w", encoding="utf-8") as file:
    file.write(page_source)
root = ET.fromstring(page_source)

tables = root.findall(".//XCUIElementTypeTable")

users = []
# 定位到 Table
for row in tables[0].findall("./XCUIElementTypeTableRow"):
    cell = row.find("./XCUIElementTypeCell")
    if cell is not None:
        static_text = cell.find("./XCUIElementTypeStaticText")
        if static_text is not None and "value" in static_text.attrib:
            users.append(static_text)

sean = None          
for u in users:
    print(u.attrib["value"])
    if 'seanzhang' in u.attrib["value"].lower():
        sean = u
        break
if sean is None:
    print("未找到 seanzhang")
    exit(0)

# 移动鼠标到sean这个元素里的 x,y, weight, height 算出中心位置，然后在该位置触发右键
# 只需要计算出中心位置，然后在该位置触发右键
# 计算中心位置
x = int(sean.attrib["x"]) + int(sean.attrib["width"]) / 2
y = int(sean.attrib["y"]) + int(sean.attrib["height"]) / 2
driver.execute_script('macos: rightClick', {'x': x, 'y': y})

input("请按回车键继续...")

exit(0)

try:
    # **等待 UI 加载**
    time.sleep(3)

    # **检查 page source**
    page_source = driver.page_source
    if "XCUIElementTypeTable" not in page_source:
        print("未检测到表格，可能 UI 尚未加载")
    else:
        print("页面加载成功，开始查找联系人...")

    # **查找表格**
    tables = driver.find_elements(AppiumBy.XPATH, "//XCUIElementTypeTable")
    if not tables:
        print("未找到表格")
    else:
        print(f"找到 {len(tables)} 个表格，开始解析...")

    # **获取表格中的所有行**
    rows = driver.find_elements(AppiumBy.XPATH, "//XCUIElementTypeTableRow")
    print(f"找到 {len(rows)} 行")

    # **提取联系人名称**
    contact_names = []
    for row in rows:
        row.click()
        static_texts = row.find_elements(AppiumBy.XPATH, ".//XCUIElementTypeCell/XCUIElementTypeStaticText")
        if static_texts:
            contact_name = static_texts[0].get_attribute('value')
            if contact_name:
                contact_names.append(contact_name)
                print(f"找到联系人: {contact_name}")

    # **打印所有联系人**
    print("\n联系人名称列表:")
    for name in contact_names:
        print(name)

except Exception as e:
    print(f"发生错误: {e}")

# **不关闭 driver，保持连接**
