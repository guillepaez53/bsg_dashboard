import os

# Directorio base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directorio del proyecto (calculado de manera relativa desde el Directorio base)

PROJECT_DIR = os.path.join(BASE_DIR, "..")

# Directorio raíz de los datos

DATA_DIR = os.path.join(PROJECT_DIR, "data")

# Directorios de los datos crudos

DATA_RAW_DIR = os.path.join(DATA_DIR, "raw")
DATA_RAW_CI_DIR = os.path.join(DATA_RAW_DIR, "competitive_intelligence")
DATA_RAW_FI_DIR = os.path.join(DATA_RAW_DIR, "footwear_industry")
DATA_RAW_CO_DIR = os.path.join(DATA_RAW_DIR, "company_operative")

# Directorio de los datos parseados
DATA_PARSED_DIR = os.path.join(DATA_DIR, "parsed")
DATA_PARSED_FI_DIR = os.path.join(DATA_PARSED_DIR, "footwear_industry")
DATA_PARSED_CO_DIR = os.path.join(DATA_PARSED_DIR, "company_operative")

# Directorio de los datos procesados

DATA_PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
DATA_PROCESSED_CI_DIR = os.path.join(DATA_PROCESSED_DIR, "competitive_intelligence")
DATA_PROCESSED_FI_DIR = os.path.join(DATA_PROCESSED_DIR, "footwear_industry")
DATA_PROCESSED_CO_DIR = os.path.join(DATA_PROCESSED_DIR, "company_operative")

# Directorio de los datos acuumulados

DATA_ACCUMULATED_DIR = os.path.join(DATA_DIR, "accumulated")
DATA_ACCUMULATED_CI_DIR = os.path.join(DATA_ACCUMULATED_DIR, "competitive_intelligence")
DATA_ACCUMULATED_FI_DIR = os.path.join(DATA_ACCUMULATED_DIR, "footwear_industry")
DATA_ACCUMULATED_CO_DIR = os.path.join(DATA_ACCUMULATED_DIR, "company_operative")

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
