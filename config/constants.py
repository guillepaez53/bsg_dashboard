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
    " Model Availability": "Calidad",
    " S/Q Rating (1 to 10 stars)": "Calidad",
    " S/Q Rating (min = 3.0 stars)": "Calidad",
    " Market Share (%)": "Cuota",
    " Brand Advertising ($000s)": "Imagen",
    " Brand Reputation (prior-year image)": "Imagen",
    " Celebrity Appeal": "Imagen",
    " Search Engine Advert. ($000s)": "Imagen",
    " Delivery Time (weeks)": "Marketing",
    " Free Shipping": "Marketing",
    " Retail Outlets": "Marketing",
    " Retailer Support ($ per outlet)": "Marketing",
    " Offer Price (max = $40.00)": "Precio",
    " Rebate Offer ($ per pair)": "Precio",
    " Retail Price ($ per pair)": "Precio",
    " Wholesale Price ($ per pair)": "Precio",
    "   Gained / Lost (due to stockouts)": "Volumen",
    " Online Orders (000s)": "Volumen",
    " Pairs Demanded (000s)": "Volumen",
    " Pairs Offered (000s)": "Volumen",
    " Pairs Sold (000s)": "Volumen",
}
