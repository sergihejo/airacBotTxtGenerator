import os
import re
import sys

import pdfplumber
from bs4 import BeautifulSoup
import requests

# Define const
FIRS = ['LECB', 'LECS', 'LECM', 'GCCC', 'ATC']

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"\033[31mError: El archivo {pdf_path} no se ha encontrado. Asegúrate de que el archivo existe y está en el directorio actual.")
        sys.exit(1)

    return text

def format_line(line):
    # Add parentheses to page numbers if they are not already
    line = re.sub(r"(?i)(?<!\()P[aáÁ]g\.? \d+(-\d+)?(?!\))", r"(\g<0>)", line)
    # If available, get rid of ○ character and add ● character. If there is no ○ character, add ● character
    line = line.replace("○", "\t●") if "○" in line else "\t● " + line
    # Ensure colon after FIR code if not already present
    line = re.sub(r"(● (LE..|GC..))(?!:)", r"\1:", line)
    # Remove extra spaces
    return re.sub(r" +", " ", line)

def save_text_to_txt(text, txt_path, wef, airac, amdt):
    fir = ""
    changes = {}

    for line in text.splitlines():
        # Extract FIR or Airport
        match = re.search(r"(LE..|GC..|ATC)", line)
        # If FIR is found, save it
        if match and match.group(0) in FIRS:
            fir = match.group(0)
            continue
        if fir and fir != "ATC":
            # Skip lines that do not contain FIR or Airporta
            if not re.search(r"(LE..|GC..)", line):
                continue
            # Add FIR to changes if it is not already
            changes.setdefault(fir, []).append(format_line(line))

        # Build the formatted text
    changes_text = "\n".join(
        f"**FIR de {fir}**\n" + "\n".join(lines) + "\n"
        for fir, lines in changes.items()
    )

    # Template for the text output
    output_template = (
        f"**Comunicación Mensual de Enmienda AIRAC** **Ciclo {airac}**\n"
        f"*Fecha de entrada en vigor: {wef}*\n\n"
        "Enlaces de descarga de la enmienda:\n"
        f"[AMDT]({amdt})\n\n"
        f"{changes_text}\n"
        "**Aerovías Antiguas**\n"
        "ENR antiguo con información del sistema anterior de aerovías:\n"
        "[ENR 3.0](https://files.es.ivao.aero/FIR/AOC/AIRACS/2402_LE_ENR_3_0_en.pdf)\n"
        "[ENR 3.1](https://files.es.ivao.aero/FIR/AOC/AIRACS/2402_LE_ENR_3_1_en.pdf)\n"
        "[ENR 3.2](https://files.es.ivao.aero/FIR/AOC/AIRACS/2402_LE_ENR_3_2_en.pdf)\n\n"
        "Este documento se ha generado automáticamente. Puede contener errores.\n\n"
        "SOLO PARA USO EN SIMULACIÓN - NO VÁLIDO PARA OPERACIONES REALES\n\n"
        "Departamento de Operaciones ATC de IVAO España 📡\n"
    )

    with open(txt_path, "w") as file:
        file.write(output_template)


def get_airac_data(html_content, target_airac):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <tr> elements
    rows = soup.find_all('tr')

    # Iterate through the rows to find the one with the specified AIRAC
    for row in rows:
        cells = row.find_all('td')  # Find all <td> in the current <tr>

        if len(cells) > 0:
            # Check if the second <td> contains the target AIRAC cycle
            airac_cell = cells[1].find('strong')  # Get the <strong> tag
            if airac_cell and airac_cell.text.strip() == target_airac:
                # If found, get the last date (last <strong> in the row)
                last_date_cell = cells[-1].find('strong')  # Get the last <strong> tag
                return last_date_cell.text.strip() if last_date_cell else None
    return None


def main():
    print("Generador de documento txt para el bot de Discord de IVAO España")
    print("Este programa extrae la información del documento PDF de la enmienda AIRAC y la guarda en un archivo de texto.")
    print("Asegúrate de tener en este mismo directorio (", os.getcwd() , ") el documento PDF de la enmienda AIRAC con el nombre 'AIRAC_XXXX.pdf'.")
    print("Desarrollado por Sergio H (626590)\n")

    airac = input("Introduce el número de ciclo AIRAC: ").strip()
    if not airac.isdigit() and len(airac) != 4:
        print("\033[31mError: Número de ciclo AIRAC no válido.")
        sys.exit(1)

    file_path = "AIRAC_" + airac + ".pdf"
    text = extract_text_from_pdf(file_path)

    amdt = input("Introduce el enlace de descarga de la enmienda de ENAIRE: ").strip()
    if not re.match(r"https://aip.enaire.es/AIP/contenido_AMDT/LE_Amdt_A_\d{4}_\d{2}_en.pdf", amdt):
        print("\033[31mError: Enlace de descarga de la enmienda no válido. Asegúrate de que sigue el formato \033[34mhttps://aip.enaire.es/AIP/contenido_AMDT/LE_Amdt_A_XXXX_XX_en.pdf.")
        sys.exit(1)

    try:
        # Make a GET request to the specified URL
        response = requests.get("https://www.nm.eurocontrol.int/RAD/common/airac_dates.html")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            wef = get_airac_data(response.text, airac)
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response content:", response.text)
            wef = input("Introduce la fecha de entrada en vigor: ").strip()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        wef = input("Introduce la fecha de entrada en vigor: ").strip()

    output_path = "ciclo" + airac + ".txt"


    save_text_to_txt(text, output_path, wef, airac, amdt)
    print(f"\033[32m\nEl txt se ha generado correctamente en {output_path}.")


if __name__ == "__main__":
    main()
