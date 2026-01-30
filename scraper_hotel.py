from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta

def arreglar_fecha(f):
    try:
        trozos = f.split(" ")
        dia = trozos[0]
        mes = trozos[1].lower()[:3]
        anio = trozos[2]
        
        n_mes = "01"
        if mes == "ene": n_mes = "01"
        elif mes == "feb": n_mes = "02"
        elif mes == "mar": n_mes = "03"
        elif mes == "abr": n_mes = "04"
        elif mes == "may": n_mes = "05"
        elif mes == "jun": n_mes = "06"
        elif mes == "jul": n_mes = "07"
        elif mes == "ago": n_mes = "08"
        elif mes == "sep": n_mes = "09"
        elif mes == "set": n_mes = "09"
        elif mes == "oct": n_mes = "10"
        elif mes == "nov": n_mes = "11"
        elif mes == "dic": n_mes = "12"
        else: return None
        
        if len(dia) == 1:
            dia = "0" + dia
        return anio + "-" + n_mes + "-" + dia
    except:
        return None

def buscar_hotel(ciudad, fecha):
    f_in = arreglar_fecha(fecha)
    
    if f_in == None:
        return "Fecha incorrecta"
    try:
        d = datetime.strptime(f_in, "%Y-%m-%d")
        d2 = d + timedelta(days=1)
        f_out = d2.strftime("%Y-%m-%d")
    except:
        return "Error calculando fecha"
        
    url = "https://www.booking.com/searchresults.html?ss=" + ciudad + "&checkin=" + f_in + "&checkout=" + f_out + "&group_adults=2"
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=opts)
    res = "No encontrado"
    
    try:
        driver.get(url)
        time.sleep(6)
        
        try:
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except:
            pass

        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)
        precios = driver.find_elements(By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']")
        
        if len(precios) == 0:
            precios = driver.find_elements(By.XPATH, "//*[contains(text(), '€')]")
        lista = []
        count = 0
        for p in precios:
            t = p.text.replace("€", "").replace(",", ".").strip()
            if len(t) > 8: continue
            try:
                v = float(t)
                if v > 10: 
                    lista.append(v)
                    count = count + 1
            except:
                continue
            if count == 5: break
        if len(lista) > 0:
            media = sum(lista) / len(lista)
            res = str(int(media)) + " euros (Precio Medio)"
        else:
            body = driver.find_element(By.TAG_NAME, "body").text
            if "No hay alojamientos" in body:
                res = "Agotado / Lleno"
            else:
                res = "No he podido ver el precio"
    except:
        res = "Error en Booking"
        
    driver.quit()
    return res