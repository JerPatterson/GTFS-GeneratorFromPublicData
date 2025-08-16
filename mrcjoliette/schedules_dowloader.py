import os
import gdown
import urllib.request

SCHEDULES_PATH = "./schedules"

ROUTE_A_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/06/horaire-circuit-a-notre-dame-des-prairies.pdf"
ROUTE_B_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/06/horaire-circuit-b-saint-charles-borromee.pdf"
ROUTE_C_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/09/20241007-web-horaire-circuit-c-saint-charles-borromee-et-joliette-secteur-christ-roi-et-belair.pdf"
ROUTE_D_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/09/20241007-web-horaire-circuit-d-joliette-secteurs-st-pierre-et-carrefour-du-moulin.pdf"
ROUTE_E_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/07/horaire-circuit-e-joliette-secteurs-saint-jean-baptiste-et-ste-therese.pdf"
ROUTE_X_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/09/20241007-web-horaire-circuit-x-express.pdf"

ROUTE_32_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/01/horaire-32-horaire-20240115.pdf"
ROUTE_34_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/01/horaire-34-2024-0115.pdf"
ROUTE_50_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/08/horaire-50-horaire-28-avril-2024-vf.pdf"
ROUTE_125_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2020/07/20200831-horaire-125-recto-verso-31-aout-2020.pdf"
ROUTE_131_138_SCHEDULE_URL = "https://drive.google.com/uc?id=1yz7RamN5h8BZQWTpdkymo9yDur1RscCA"


def download_schedule_file(url, route_short_name):
    with urllib.request.urlopen(url) as response:
        with open(f"{SCHEDULES_PATH}/{route_short_name}.pdf", "wb") as f:
            f.write(response.read())
        
    print(f"Downloaded schedule for route {route_short_name}.")

def download_schedule_file_from_google_drive(url, route_short_name):
    gdown.download(url, f"{SCHEDULES_PATH}/{route_short_name}.pdf", quiet=True)
    print(f"Downloaded schedule for route {route_short_name}.")


def download_local_routes_schedules():
    os.makedirs(SCHEDULES_PATH, exist_ok=True)

    download_schedule_file(ROUTE_A_SCHEDULE_URL, "A")
    download_schedule_file(ROUTE_B_SCHEDULE_URL, "B")
    download_schedule_file(ROUTE_C_SCHEDULE_URL, "C")
    download_schedule_file(ROUTE_D_SCHEDULE_URL, "D")
    download_schedule_file(ROUTE_E_SCHEDULE_URL, "E")
    download_schedule_file(ROUTE_X_SCHEDULE_URL, "X")

def download_regional_routes_schedules():
    os.makedirs(SCHEDULES_PATH, exist_ok=True)

    download_schedule_file(ROUTE_32_SCHEDULE_URL, "32")
    download_schedule_file(ROUTE_34_SCHEDULE_URL, "34")
    download_schedule_file(ROUTE_50_SCHEDULE_URL, "50")
    download_schedule_file(ROUTE_125_SCHEDULE_URL, "125")
    download_schedule_file_from_google_drive(ROUTE_131_138_SCHEDULE_URL, "131138")


def main():
    print("Fetching schedules...")
    download_local_routes_schedules()
    download_regional_routes_schedules()


if __name__ == "__main__":
    main()
