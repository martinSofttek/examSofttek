import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

def download_image(url, sku):
    try:
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image = image.convert("RGB")
                image.thumbnail((800, 800))
                output = BytesIO()
                image.save(output, format='JPEG', quality=85)
                if len(output.getvalue()) <= 100 * 1024: 
                    with open(f"imagenes/{sku}.jpg", "wb") as f:
                        f.write(output.getvalue())
                    print(f"Imagen guardada para SKU {sku}")
                else:
                    print(f"La imagen para SKU {sku} excede los 100KB y no se guardará.")
            else:
                print(f"No se pudo descargar la imagen para SKU {sku}")
        else:
            print(f"No hay URL de imagen para SKU {sku}")
    except Exception as e:
        print(f"Error al descargar o procesar la imagen para SKU {sku}: {e}")

def main():
    catalog = pd.read_excel("catalogo.xlsx")

    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

    for index, row in catalog.iterrows():
        sku = row["SKU"]
        url = row["Url"]
        download_image(url, sku)

if __name__ == "__main__":
    main()
