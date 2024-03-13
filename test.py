import os
import pandas as pd
import requests


from PIL import Image
from io import BytesIO


#Adrian Martin Hernandez Barrientos 

def descargarImagen(url, sku):
    try:
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                imagen = Image.open(BytesIO(response.content))
                imagen = imagen.convert("RGB")
                imagen.thumbnail((800, 800))
                output = BytesIO()
                imagen.save(output, format='JPEG', quality=85)
                if len(output.getvalue()) <= 100 * 1024: 
                    with open(f"imagenes/{sku}.jpg", "wb") as f:
                        f.write(output.getvalue())
                    print(f"Imagen guardada con SKU {sku}")
                else:
                    print(f"Imagen con SKU {sku} excede los 100KB y no se va a guardar.")
            else:
                print(f"Error al descargar la imagen de SKU {sku}")
        else:
            print(f"No hay URL de imagen de SKU {sku}")
    except Exception as e:
        print(f"Error al procesar la imagen para SKU {sku}: {e}")

def main():
    catalogo = pd.read_excel("catalogo.xlsx")

    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

    for index, row in catalogo.iterrows():
        sku = row["SKU"]
        url = row["Url"]
        descargarImagen(url, sku)

if __name__ == "__main__":
    main()
