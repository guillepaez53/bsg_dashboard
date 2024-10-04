import os

# Directorio base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directorio del proyecto

PROJECT_DIR = os.path.join(BASE_DIR, "..")

# Directorio de datos

DATA_DIR = os.path.join(PROJECT_DIR, "data")
DATA_RAW_DIR = os.path.join(DATA_DIR, "raw")
DATA_RAW_CI_DIR = os.path.join(DATA_RAW_DIR, "competitive_intelligence")
DATA_PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
DATA_ACCUMULATED_DIR = os.path.join(DATA_DIR, "accumulated")

# Definición de constantes

COMPANY = "D"
COMPANIES = ["A", "B", "C", "D", "E"]
NO_COMPANIES = ["F", "G", "H", "I", "J", "K", "L"]
OTHER_COMPANIES = ["A", "B", "C", "E"]

REGIONES = {
    "NA": "North America",
    "EA": "Europe-Africa",
    "AP": "Asia-Pacifc",
    "LA": "Latin America",
}

METRICAS = {
    " Model Availability": "B - Calidad",
    " S/Q Rating (1 to 10 stars)": "B - Calidad",
    " S/Q Rating (min = 3.0 stars)": "B - Calidad",
    " Market Share (%)": "F - Cuota",
    " Brand Advertising ($000s)": "D - Imagen",
    " Brand Reputation (prior-year image)": "D - Imagen",
    " Celebrity Appeal": "D - Imagen",
    " Search Engine Advert. ($000s)": "D - Imagen",
    " Delivery Time (weeks)": "C - Marketing",
    " Free Shipping": "C - Marketing",
    " Retail Outlets": "C - Marketing",
    " Retailer Support ($ per outlet)": "C - Marketing",
    " Offer Price (max = $40.00)": "A - Precio",
    " Rebate Offer ($ per pair)": "A - Precio",
    " Retail Price ($ per pair)": "A - Precio",
    " Wholesale Price ($ per pair)": "A - Precio",
    "   Gained / Lost (due to stockouts)": "E - Volumen",
    " Online Orders (000s)": "E - Volumen",
    " Pairs Demanded (000s)": "E - Volumen",
    " Pairs Offered (000s)": "E - Volumen",
    " Pairs Sold (000s)": "E - Volumen",
}
