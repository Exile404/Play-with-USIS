import Backend.Constant as const
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
from selenium.webdriver.support.ui import Select
from prettytable import PrettyTable
import time

class Usis(webdriver.Chrome):
    def __init__(self, driver_path=r"F:\Bot", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-logging'])
        super(Usis, self).__init__(options=options)
        self.implicitly_wait(300)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def login(self,email,password):
        email_ele= self.find_element(By.ID,'username')
        pwd_ele=self.find_element(By.ID,'password')
        email_ele.send_keys(email)
        pwd_ele.send_keys(password)
        submit=self.find_element(By.ID,'ctl00_leftColumn_ctl00_btnLogin')
        submit.click()
    def seat_status_option(self):
        seat_stat=self.find_element(By.XPATH,'//*[@id="accordion1"]/h3[2]')
        seat_stat.click()
        seat_stat_select=self.find_element(By.XPATH,'//*[@id="accordion1"]/div[2]/div[2]/a')
        seat_stat_select.click()
    def seat_stattus_selection(self,year,session,coursename):

        year_select=Select(self.find_element(By.ID,'academiaYear'))
        year_select.select_by_visible_text(year)
        academic_session=Select(self.find_element(By.ID,'academiaSession'))
        academic_session.select_by_visible_text(session)
        time.sleep(30)
        search_field=self.find_element(By.ID,'queryCourseStatus')
        search_field.clear()
        search_field.send_keys(coursename)
        search_button=self.find_element(By.ID,'search-button')
        search_button.click()
    def courses_list(self):
        course_list = self.find_elements(By.CSS_SELECTOR,'tr[class="ui-widget-content jqgrow ui-row-ltr"]')
        collections=[]

        for element in course_list:
            course_name=element.find_element(By.CSS_SELECTOR,'td[aria-describedby="jqgrid-grid-studentStatusCourseList_course_code"]').get_attribute('innerHTML').strip()
            faculty_name=element.find_element(By.CSS_SELECTOR,'td[aria-describedby="jqgrid-grid-studentStatusCourseList_title"]').get_attribute('innerHTML').strip()
            total_seat=element.find_element(By.CSS_SELECTOR,'td[aria-describedby="jqgrid-grid-studentStatusCourseList_seat_capacity"]').get_attribute('innerHTML').strip()
            booked_seat=element.find_element(By.CSS_SELECTOR,'td[aria-describedby="jqgrid-grid-studentStatusCourseList_seat_booked"]').get_attribute('innerHTML').strip()
            if total_seat=='&nbsp;' or booked_seat=='&nbsp;':
                continue
            rem_seat=int(total_seat)-int(booked_seat)
            if rem_seat<=0:
                continue
            section_no=element.find_element(By.CSS_SELECTOR,'td[aria-describedby="jqgrid-grid-studentStatusCourseList_short_name"]').get_attribute('innerHTML').strip()
            collections.append([course_name,faculty_name,section_no,rem_seat])

        self.get(const.BASE_URL1)



        j=0
        new = self.find_elements(By.CSS_SELECTOR, 'td[style="text-align: center; width: 100px"]')
        course_time = self.find_elements(By.CSS_SELECTOR, 'td[style="text-align: center; width: 290px;"]')
        course_sec = self.find_elements(By.CSS_SELECTOR, 'td[style="text-align: center; width: 69px;"]')


        for i in range(len(new)-1):
            course_time1=course_time[i].get_attribute('innerHTML').strip()
            course_sec1=course_sec[i].get_attribute('innerHTML').strip()
            x=new[i].get_attribute('innerHTML').strip()

            if collections[j][2]==course_sec1 and x==course_name:
                collections[j].append(course_time1)
                j+=1
                if j==len(collections):
                    break

        table = PrettyTable(
            field_names=["Course Name","Faculty Name","Section No","Empty Seats","Course Time"]
        )
        table.add_rows(collections)
        print(table)



