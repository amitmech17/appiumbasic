# import pytest
import time

from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from selenium.webdriver.support.wait import WebDriverWait
from ppadb.client import Client as AdbClient


class adbclient:
    client = None

    def __init__(self):
        self.client = AdbClient(host="127.0.0.1", port=5037)

    def get_first_device(self):
        try:
            devices = self.client.devices()
            print(devices)
            return devices[0]
        except Exception as e:
            log.info(e)
            return False

def localSetUp(device_name):
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['udid'] = str(device_name)
    # desired_caps['app'] = 'Enter the path'
    desired_caps['noReset'] = True
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['autoGrantPermissions'] = True
    # desired_caps['appWaitActivity'] = '*.activities.*'
    desired_caps['appPackage'] = 'com.google.android.apps.photos'
    desired_caps['appActivity'] = 'com.google.android.apps.photos.home.HomeActivity'
    # desired_caps['appPackage'] = 'com.google.android.apps.messaging'
    # desired_caps['appActivity'] = 'com.google.android.apps.messaging.ui.HomeActivity'
    desired_caps['autoDismissAlerts'] = True
    desired_caps['skipUnlock'] = True
    desired_caps['disableWindowAnimation']=True
    print("animation is disbled for android device")
    # desired_caps['skipDeviceInitialization'] = False
    # desired_caps['skipServerInstallation'] = False
    # desired_caps['autoWebview'] = True
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    # driver.implicitly_wait(10)
    driver.update_settings({"waitForIdleTimeout": 1})
    driver.implicitly_wait(7)
    driver.start_recording_screen()
    print('driver globalized on local device...')
    return driver


def driversetup():
    service = AppiumService()
    fileObj = open('appium1.log', 'a+')
    service.start(stdout=fileObj)
    adb_object = adbclient()
    try:
        device = adb_object.get_first_device()
    except:
        return False
    device_name = (device.serial).strip()
    print(device_name)
    driver = localSetUp(device_name)
    driver.push_file('/sdcard/Pictures/duck.png', source_path=r'./duck.jpeg')
    # driver.background_app(-1)
    # driver.find_element_by_xpath("//*[@text='Photos']").click()
    # driver.launch_app()
    try:
        driver.find_element_by_xpath("//*[@text='Not now']").click()
    except:
        print("Not now button")
    driver.find_element_by_xpath("//*[@resource-id='com.google.android.apps.photos:id/tab_library']").click()
    folder_name = driver.find_elements_by_xpath("//*[@resource-id='com.google.android.apps.photos:id/album_cover_title']")
    for i in folder_name:
        if i.text == "Pictures":
            i.click()
            break
    all_photos = driver.find_elements_by_xpath("//android.view.ViewGroup[contains(@content-desc,'Photo taken')]")
    for i in all_photos:
        i.click()
        break
    driver.find_element_by_xpath("//*[@resource-id='com.google.android.apps.photos:id/edit']").click()
    try:
        driver.find_element_by_xpath("//*[@text='Got it']").click()
    except:
        print("No got it button")
    driver.find_element_by_xpath("//*[@text='Crop']").click()
    driver.find_element_by_xpath("//*[@resource-id='com.google.android.apps.photos:id/photos_photoeditor_fragments_editor3_rotate_90']").click()
    driver.find_element_by_xpath("//*[@resource-id='com.google.android.apps.photos:id/photos_photoeditor_fragments_editor3_save']").click()
    time.sleep(5)
    driver.background_app(-1)
    driver.find_element_by_xpath("//*[@text='Gmail']").click()
    driver.find_element_by_xpath("//*[@resource-id='com.google.android.gm:id/compose_button']").click()
    driver.find_element_by_xpath("//*[@resource-id='com.google.android.gm:id/to_content']//*[@class='android.widget.EditText']").send_keys("neal.jacob.415@gmail.com")
    driver.find_element_by_xpath("//*[@resource-id='com.google.android.gm:id/add_attachment']").click()
    driver.find_element_by_xpath("//*[@resource-id='com.google.android.gm:id/title']").click()
    driver.find_element_by_xpath("//*[@class='android.widget.CompoundButton' and @text='Images']").click()
    time.sleep(2)
    all_photo = driver.find_elements_by_xpath("//*[@resource-id='com.google.android.documentsui:id/item_root']")
    for photo in all_photo:
        if "~" in photo.find_element_by_xpath("//*[@resource-id='android:id/title']").text:
            photo.click()
            break
    # driver.find_element_by_xpath("//*[@resource-id='com.google.android.documentsui:id/action_menu_select']").click()
    driver.find_element_by_xpath("//*[@resource-id='com.google.android.gm:id/send']").click()
    driver.quit()
    service.stop()
    fileObj.close()


driversetup()
