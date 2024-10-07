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
    " Model Availability": "e - Calidad",
    " S/Q Rating (1 to 10 stars)": "e - Calidad",
    " S/Q Rating (min = 3.0 stars)": "e - Calidad",
    " Market Share (%)": "d - Cuota",
    " Brand Advertising ($000s)": "g - Imagen",
    " Brand Reputation (prior-year image)": "g - Imagen",
    " Celebrity Appeal": "g - Imagen",
    " Search Engine Advert. ($000s)": "g - Imagen",
    " Delivery Time (weeks)": "f - Marketing",
    " Free Shipping": "f - Marketing",
    " Retail Outlets": "f - Marketing",
    " Retailer Support ($ per outlet)": "f - Marketing",
    " Offer Price (max = $40.00)": "b - Precio",
    " Rebate Offer ($ per pair)": "b - Precio",
    " Retail Price ($ per pair)": "b - Precio",
    " Wholesale Price ($ per pair)": "b - Precio",
    "   Gained / Lost (due to stockouts)": "c - Volumen",
    " Online Orders (000s)": "c - Volumen",
    " Pairs Demanded (000s)": "c - Volumen",
    " Pairs Offered (000s)": "c - Volumen",
    " Pairs Sold (000s)": "c - Volumen",
}
