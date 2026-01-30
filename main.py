import sys
import os
import socket
import json

ruta = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta)

from modules.scraper_eventos import buscar_conciertos
from modules.scraper_clima import sacar_clima
from modules.scraper_hotel import buscar_hotel

IP_SERVER = '127.0.0.1'
PUERTO = 65432

if __name__ == "__main__":
    print("=============================")
    print("      CLIENTE TourMate")
    print("=============================")
    
    artista = input("\nDime el artista: ")
    print("\nBuscando conciertos de " + artista + " en Wegow")
    lista = buscar_conciertos(artista)
    
    if len(lista) == 0:
        print("\nVaya... no he encontrado ningún concierto activo para " + artista + ".")
    else:
        num = len(lista)
        limite = 3
        if num > limite:
            num = limite
        print("\nHay " + str(len(lista)) + " conciertos. Cogemos los " + str(num) + " primeros: ")
        datos_enviar = []
        for i in range(num):
            evento = lista[i]
            sitio = evento['ciudad']
            dia = evento['fecha']
            print("\nDestino " + str(i+1) + ": " + sitio + " (" + dia + ")")
            
            tiempo = sacar_clima(sitio)
            print("    El tiempo: " + tiempo)
            
            precio = buscar_hotel(sitio, dia)
            print("    Precio hotel: " + precio)
            
            mi_dato = {"Artista": artista, "Ciudad": sitio, "Fecha": dia, "El Tiempo": tiempo, "Precio Hotel": precio}
            datos_enviar.append(mi_dato)
            
        if len(datos_enviar) > 0:
            paquete = {"artista": artista, "datos": datos_enviar}
            mensaje = json.dumps(paquete)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((IP_SERVER, PUERTO))
                s.sendall(mensaje.encode('utf-8'))
                s.close()
                print("\nDatos enviados al servidor")
            except:
                print("ERROR")