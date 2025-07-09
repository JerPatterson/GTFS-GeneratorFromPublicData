import urllib.request

SCHEDULES_PATH = "schedules"

ROUTE_32_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/01/horaire-32-horaire-20240115.pdf"
ROUTE_34_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/01/horaire-34-2024-0115.pdf"
ROUTE_50_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2024/08/horaire-50-horaire-28-avril-2024-vf.pdf"
ROUTE_125_SCHEDULE_URL = "https://mrcjoliette.qc.ca/wp-content/uploads/2020/07/20200831-horaire-125-recto-verso-31-aout-2020.pdf"
ROUTE_131_138_SCHEDULE_URL = "https://drive.google.com/file/d/1yz7RamN5h8BZQWTpdkymo9yDur1RscCA/view"


def download_schedule_file(url, route_name):
    with urllib.request.urlopen(url) as response:
        with open(f"{SCHEDULES_PATH}/{route_name}.pdf", "wb") as f:
            f.write(response.read())
        
    print(f"Downloaded schedule for route {route_name}.")

def download_regional_routes_schedules():
    download_schedule_file(ROUTE_32_SCHEDULE_URL, "32")
    download_schedule_file(ROUTE_34_SCHEDULE_URL, "34")
    download_schedule_file(ROUTE_50_SCHEDULE_URL, "50")
    download_schedule_file(ROUTE_125_SCHEDULE_URL, "125")
    download_schedule_file(ROUTE_131_138_SCHEDULE_URL, "131_138")


def main():
    print("Fetching schedules...")
    download_regional_routes_schedules()


if __name__ == "__main__":
    main()
