"""Template robot with Python."""
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.Tables import Tables
from datetime import datetime
import time
import os
browser_lib = Selenium()
lib = Files()
table = Tables()
dwPath = f"output/"
def open_the_website(url):
    browser_lib.set_download_directory(os.path.join(os.getcwd(),dwPath))
    browser_lib.open_available_browser(url)
def close_the_website():
    browser_lib.close_browser()
def click_button(xpath):
    dive_element = "xpath:%s" % (xpath)
    browser_lib.find_element(dive_element).click()
def agency_totals():
    time.sleep(30)
    while True:
        try:
            lista = browser_lib.find_elements("xpath://div[@id='agency-tiles-widget']")
            break
        except:
            pass
    for symbol in lista:
        element_text = symbol.text
        formatted = element_text.split("\n")
    return formatted
def create_worksheet(nameW):
    lib.create_worksheet(nameW)
def write_excel_worksheet(path, nameW, result):
    lista = []
    excel = lib.open_workbook(path)
    date = datetime.today().strftime('%Y-%m-%d %H:%M')
    for i in range(len(result)):
        if result[i] == "view":
            agencies = result[i-3]
            amount = result[i-1]
            lista.append([date, agencies, amount])
    headers = ['Datetime', 'Agency', 'Amount']
    browser_lib.set_browser_implicit_wait(5)
    tablaExcel = table.create_table(data=lista, columns=(headers))
    browser_lib.set_browser_implicit_wait(5)
    lib.append_rows_to_worksheet(tablaExcel, nameW, headers)
    browser_lib.set_browser_implicit_wait(5)
    lib.save_workbook(path)
    browser_lib.set_browser_implicit_wait(5)
    return [len(result),lista]
def close_excel_file(path):
    lib = Files()
    lib.close_workbook(path)
def get_max_pag():
    browser_lib.wait_until_page_contains("Next",'15')
    pages = "xpath://*[@id='investments-table-object_paginate']/span/a"
    listaPAgs = browser_lib.find_elements(pages)
    time.sleep(30)
    span = "/span/a[%s]" % (len(listaPAgs))
    element = "xpath://*[@id='investments-table-object_paginate']%s" % (span)
    time.sleep(30)
    txtMaxPag = browser_lib.find_element(element).text
    return txtMaxPag
def get_headers():
    div = "/div[3]/div[1]/div/table/thead/tr[2]/th"
    element = "xpath://*[@id='investments-table-object_wrapper']%s" % (div)
    listaEncabezado = browser_lib.find_elements(element)
    encabezado = []
    for symbol in listaEncabezado:
        element_text = symbol.text
        encabezado.append(element_text)
    result = [len(listaEncabezado), encabezado]
    return result
def individual_investment(path):
    element1 = "xpath://*[@id='investments-table-object']/tbody/tr/td/a"
    listaFilasLinks = browser_lib.find_elements(element1)
    element2 = "xpath://*[@id='investments-table-object']/tbody/tr"
    listaFilas = browser_lib.find_elements(element2)
    lenHeaders = get_headers()[0]
    headers = get_headers()[1]
    filaGeneral = []
    for f in range(len(listaFilas)):
        filas = []
        for c in range(lenHeaders):
            el3 = "/tbody/tr[%s]/td[%s]" % (f+1, c+1)
            element4 = "xpath://*[@id='investments-table-object']%s" % (el3)
            fila = browser_lib.find_element(element4).text
            filas.append(fila)
        filaGeneral.append(filas)
    time.sleep(1)
    tablaExcel = table.create_table(data=filaGeneral, columns=headers)
    time.sleep(1)
    lib.open_workbook(path)
    time.sleep(1)
    lib.append_rows_to_worksheet(tablaExcel, "Investments", headers)
    time.sleep(10)
    lib.save_workbook(path)
    time.sleep(10)
    filasLinks = []
    if len(listaFilasLinks)>0:
        for h in listaFilasLinks:
            href = h.get_attribute('href')
            time.sleep(5)
            #browser_lib2.op
            open_the_website(href)
            time.sleep(15)
            element5 = "xpath://*[@id='business-case-pdf']/a"
            browser_lib.find_element(element5).click()
            time.sleep(20)      
            browser_lib.close_browser()
            time.sleep(20)  
    time.sleep(20)
def minimal_task():
    try:
        path = f"output/amounts.xlsx"      
        open_the_website("https://itdashboard.gov/")
        browser_lib.set_browser_implicit_wait(30)
        click_button("//*[@id='node-23']/div/div/div/div/div/div/div/a")
        browser_lib.set_browser_implicit_wait(35)
        totals = agency_totals()
        print("Totals",totals)
        print(write_excel_worksheet(path, 'Agencies', totals))
        browser_lib.set_browser_implicit_wait(5)
        div = "//*[@id='agency-tiles-widget']/div/div[1]/div[1]/div/div/div/div[2]/a"
        click_button(div)
        browser_lib.set_browser_implicit_wait(25)
        print(individual_investment(path))
        time.sleep(15)
    finally:
        close_the_website()
if __name__ == "__main__":
    minimal_task()
