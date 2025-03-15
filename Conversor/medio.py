import pandas as pd
import math
import sys

def conversor_excel(ruta_archivo, ruta_salida):
    """
    Méotdo para transformar un archivo excel con las columnas: anio, concepto y valor
        Siguiendo las reglas: 
        anio -> Debe ser un valor numérico de cuatro dígitos. Si el valor no tiene cuatro
        dígitos, se debe completar con ceros a la izquierda

        concepto -> Debe ser un valor alfanumérico de máximo diez caracteres. Si el valor
        tiene menos de diez caracteres, se debe completar con "$" a la derecha
        
        valor ->  Debe ser un valor numérico de máximo veinte dígitos. Si el valor tiene menos
        de veinte dígitos, se debe completar con ceros a la izquierda

        Reglas adicionales del archivo
        Si un valor en el archivo Excel no cumple con ninguna de las reglas anteriores o no se
        encuentra relacionada ningún valor del Excel, se debe dejar tal cual está en el archivo
        Excel

        Si un valor numérico en el archivo Excel tiene valor NaN, se debe transformar a una
        cadena de texto vacía
    """
    try:
        data = pd.read_excel(ruta_archivo, dtype={"ANIO": str, "CONCEPTO": str, "VALOR": str})
        data_converter = []

        for _, row in data.iterrows():
            anio = row["ANIO"]
            concepto = row["CONCEPTO"]
            valor = row["VALOR"]

            # Manejo de valores Nan
            anio = "" if pd.isna(anio) else str(anio).zfill(4) if anio.isdigit() and len(anio) <= 4 else anio
            concepto = "" if pd.isna(concepto) else str(concepto).ljust(10, "$")[:10]
            valor = "" if pd.isna(valor) else str(valor).zfill(20) if valor.isdigit() and len(valor) <= 20 else valor

            transformed_row = f"{anio}{concepto}{valor}"
            data_converter.append(transformed_row)
        
        # Guardar en archivo convertido
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write("\n".join(data_converter))
        
        print(f"Archivo convertido y guardado en: {ruta_salida} con exito")
    except Exception as e:
        print(f"Error al procesar el archivo - {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Comando: python medio.py ruta_excel ruta_salida_txt")
    else:
        ruta_excel = sys.argv[1]
        ruta_salida = sys.argv[2]
        conversor_excel(ruta_excel, ruta_salida)