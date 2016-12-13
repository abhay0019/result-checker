#!/usr/bin/python
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import sys
import os
import re
import logging
import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sch=BlockingScheduler()


if len(sys.argv)!=6:
  print "usage : ./result_checker.py your_registrationNo your_password check_interval_hour check_interval_minute            check_interval_second "
  sys.exit()
  
@sch.scheduled_job('interval',hours=int(sys.argv[3]),minutes=int(sys.argv[4]),seconds=int(sys.argv[5]))
def checker():
  print "Starting .."
  driver = webdriver. Chrome("/home/abhay/Desktop/py/result-checker/chromedriver")
  driver.get("https://academics.mnnit.ac.in/")
  elem = driver.find_element_by_name("regno")
  elem.clear()
  elem.send_keys(sys.argv[1])
  elem = driver.find_element_by_name("pass")
  elem.clear()
  elem.send_keys(sys.argv[2])
  driver.find_element_by_name("Submit").click()
  elem = driver.find_element_by_partial_link_text("View")
  elem.click()
  source=driver.page_source
  gp=re.search('<div class="midboldtxt" style="float:left;margin-top:-2px;">Result of Semester: 4</div>',source)
  if gp:
    os.system("notify-send 'nahi aya abhi!!'")
  else:
    os.system("notify-send 'Aa gya bhai .. :O '")
  driver.close()

  
inp=raw_input("If u want Display enter 1 else 2 : ")
if inp=='1':
  os.environ['DISPLAY']=":0.0"
elif inp=='2':
  os.environ['DISPLAY']=":99.0"
else:
  print "Wrong Choice .. Exiting Program !! Run again to get service .."
  sys.exit()  
sch.start()    
