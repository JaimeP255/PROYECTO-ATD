import requests
API = "22e06e27ca83dfe9cc965693ca0e96b5"

def sacar_clima(ciudad):
    try:
        limpia = ciudad.split(",")[0].strip()
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + limpia + ",ES&appid=" + API + "&units=metric&lang=es"
        r = requests.get(url)
        d = r.json()
        
        if r.status_code == 200:
            temp = d['main']['temp']
            desc = d['weather'][0]['description']
            hum = d['main']['humidity']
            return str(temp) + "ºC, " + desc + " (" + str(hum) + "%)"
        else:
            return "Datos no disponibles"
    except:
        return "Error"

if __name__ == "__main__":
    print(sacar_clima("Madrid"))
    
    