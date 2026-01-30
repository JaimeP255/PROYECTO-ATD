from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def buscar_conciertos(nombre):
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=opts)
    nombre_guion = nombre.lower().replace(" ", "-")
    url = "https://www.wegow.com/es-es/artistas/" + nombre_guion
    res = []
    try:
        driver.get(url)
        time.sleep(4)
        try:
            btn = driver.find_element(By.XPATH, "//button[contains(., 'Aceptar')]")
            btn.click()
            time.sleep(1)
        except:
            pass 

        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(2)
        
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/conciertos/']")
        print("   Hay " + str(len(links)) + " enlaces posibles. Filtramos y nos quedamos con los buenos.")
        
        for l in links:
            try:
                recuadro = l.find_element(By.XPATH, "./../..")
                texto = recuadro.text
                trozos = texto.split("\n")
                
                fecha = "Pendiente"
                ciudad = "Desconocida"
                
                for t in trozos:
                    tiene_num = False
                    for x in t:
                        if x.isdigit():
                            tiene_num = True
                    if tiene_num:
                        fecha = t
                        break
                
                for t in trozos:
                    if " en " in t:
                        partes = t.split(" en ")
                        ciudad = partes[1].strip()
                        break
                
                if ciudad == "Desconocida" and len(trozos) > 0:
                    ciudad = trozos[-1]

                c_min = ciudad.lower()
                valido = True
                
                if "bono" in c_min: valido = False
                if "entradas" in c_min: valido = False
                if "vip" in c_min: valido = False
                if fecha == "Pendiente": valido = False
                
                if valido:
                    nuevo = {}
                    nuevo['ciudad'] = ciudad
                    nuevo['fecha'] = fecha
                    repetido = False
                    for r in res:
                        if r['ciudad'] == ciudad:
                            repetido = True
                    if repetido == False:
                        res.append(nuevo)
            except:
                continue
    except:
        print("   Ups, ha habido un error leyendo Wegow.")
        
    driver.quit()
    return res