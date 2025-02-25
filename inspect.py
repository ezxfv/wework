from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.mac import Mac2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 使用Mac2Options设置所需的capabilities
options = Mac2Options()
options.bundle_id = 'com.tencent.WeWorkMac'
options.platform_name = 'mac'
options.automation_name = 'mac2'
#options.set_capability('forceAppLaunch', True)

# 初始化driver，使用Mac2Driver
driver = webdriver.Remote('http://localhost:4723', options=options)

try:    
    # 查找表格
    table = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeTable"))
    )
    
    # 获取表格中的所有行
    rows = table.find_elements(AppiumBy.XPATH, ".//XCUIElementTypeTableRow")
    print(f"找到 {len(rows)} 行")

    # 从每行提取联系人名称
    contact_names = []
    for row in rows:
        static_texts = row.find_elements(AppiumBy.XPATH, ".//XCUIElementTypeCell/XCUIElementTypeStaticText")
        if static_texts:
            contact_name = static_texts[0].get_attribute('value')
            if contact_name and len(contact_name) > 0:
                contact_names.append(contact_name)
                print(f"找到联系人: {contact_name}")    
    # 打印所有联系人名称
    print("\n联系人名称列表:")
    for name in contact_names:
        print(name)

except Exception as e:
    print(f"发生错误: {e}")
    
finally:
    # 关闭driver
    driver.quit()