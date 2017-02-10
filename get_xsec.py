import time
import getpass
import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from pyvirtualdisplay import Display

username = raw_input("Username: ")
password = getpass.getpass()
sample_filename = "sample_list.txt"


# Driver nonsense

os.system("export PATH=$PATH:GECKO_PATH")

### User defined values

username_html="ctl00_ctl00_NICEMasterPageBodyContent_SiteContentPlaceholder_txtFormsLogin"
password_html="ctl00_ctl00_NICEMasterPageBodyContent_SiteContentPlaceholder_txtFormsPassword"
button_html="ctl00_ctl00_NICEMasterPageBodyContent_SiteContentPlaceholder_btnFormsLogin"


shown_list = ['PrepId', 'Actions', 'Approval', 'Status', 'Dataset name', 'History', 'Tags', 'Analysis id', 'Block black list', 'Block white list', 'Cmssw release', 'Completed events', 'Config id', 'Energy', 'Extension', 'Filter efficiency', 'Flown with', 'Fragment', 'Fragment tag', 'Generator parameters', 'Generators', 'Input dataset', 'Keep output', 'Mcdb id', 'Member of campaign', 'Member of chain', 'Memory', 'Name of fragment', 'Notes', 'Output dataset', 'Pileup dataset name', 'Priority', 'Process string', 'Pwg', 'Reqmgr name', 'Sequences', 'Size event', 'Time event', 'Total events', 'Type', 'Validation', 'Verion']

shown_wants = ['Dataset name', 'Generator parameters', 'Generators']


shown_val=0
for item in shown_wants:
    shown_val += pow(2, shown_list.index(item))

baseurl='https://cms-pdmv.cern.ch/mcm/requests'
all_pages='&page=-1'
show_text='&shown='+str(shown_val)

sample_list = []
f = open(sample_filename)
first_line=True
for line in f:
    if first_line:
        first_line = False
        continue
    sample_list.append(line.strip())

xvfb_installed = False

if xvfb_installed:
    display = Display(visible=0, size=(800,600))
    display.start()
caps = DesiredCapabilities.FIREFOX.copy()
caps['acceptInsecureCerts'] = True
ff_binary = FirefoxBinary("FIREFOX_AREA")

driver = webdriver.Firefox(firefox_binary=ff_binary, capabilities=caps)
driver.implicitly_wait(30)
driver.get(baseurl)

element_log = driver.find_element_by_id(username_html)
element_log.send_keys(username)
element_pass = driver.find_element_by_id(password_html)
element_pass.send_keys(password)
element_but = driver.find_element_by_id(button_html)
element_but.send_keys(Keys.RETURN)
time.sleep(5)

for sample in sample_list:
    sample=sample.replace('/', '%2F')

    driver.get(baseurl+'?produce=' + sample + all_pages + show_text)
    num_pos=len(driver.find_elements_by_xpath("//div[@ng-switch-when='" + shown_wants[0] + "']"))


    final_list = []
    for i in range(0, num_pos):
        full_list = []
        for item in shown_wants:
            text = driver.find_elements_by_xpath("//div[@ng-switch-when='" + item + "']")[i].text
            if text == "":
                break
            full_list.append(text)

        if len(full_list) != len(shown_wants):
            continue
        passed = True
        for exist in final_list:
            if exist == full_list:
                passed = False
                break
        if not passed:
            continue

        final_list.append(full_list)
    print final_list



driver.quit()
if xvfb_installed:
    display.stop()
