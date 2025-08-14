import os
import pdfplumber

SCHEDULES_PATH = "./schedules"
GTFS_OUTPUT_PATH = "./output"


def get_service_id_from_name(name: str) -> str:
    name = name.upper()

    if "LUN" in name and "JEU" in name:
        return "LUNDI_JEUDI"
    if "LUN" in name and "VEN" in name:
        return "SEMAINE"
    if "SAM" in name and "DIM" in name:
        return "FIN_DE_SEMAINE"
    if "VEN" in name:
        return "VENDREDI"
    if "SAM" in name:
        return "SAMEDI"
    if "DIM" in name:
        return "DIMANCHE"
    
    return "SEMAINE"

def get_trip_headsigns_from_timetable(timetable: list[list[str | None]]) -> str:
    trip_headsigns = [""] * len(timetable[0])
    furthest_headsigns = ["NONE"] * len(timetable[0])
    for i, row in enumerate(timetable):
        if i == 0:
            if timetable[0][1] and (not timetable[0][0] or len(timetable[0][1]) > len(timetable[0][0])):
                furthest_headsigns = [timetable[0][1].split(" ")[-1]] * len(timetable[0])
            elif timetable[0][0]:
                furthest_headsigns = [timetable[0][0].split(" ")[-1]] * len(timetable[0])

        for j, value in enumerate(row):
            if not value and row[1] and (not row[0] or len(row[1]) > len(row[0])):
                furthest_headsigns[j] = row[1] if "/" not in row[1] else furthest_headsigns[j]
            elif not value and row[0]:
                furthest_headsigns[j] = row[0] if "/" not in row[0] else furthest_headsigns[j]

            if value and len(value) == 5:
                trip_headsigns[j] = furthest_headsigns[j]

    return trip_headsigns

def get_trip_direction_ids_from_timetables(timetables: list[list[list[str | None]]]) -> list[str]:
    direction_ids = []
    current_direction = 0
    name_by_direction = {}
    
    for timetable in timetables:
        timetable_title = timetable[0][0]

        if timetable_title not in name_by_direction:
            name_by_direction[timetable_title] = current_direction
            current_direction += 1

        direction_ids.append(name_by_direction[timetable_title])

    return direction_ids


def is_relevant_table_from_pdf(route_short_name: str, table: list[list[str]]) -> bool:
    for row in table:
        if len(row) > 2 and ((row[1] and f"DÉPART#" in row[1].replace(" ", "").upper())
                or (row[0] and f"CIRCUIT#{route_short_name}" in row[0].replace(" ", "").upper())):
            return True
    return False

def extract_timetables_from_pdf(route_short_name: str) -> list[list[list[str | None]]]:
    timetables: list[list[str | None]] = []
    with pdfplumber.open(f"{SCHEDULES_PATH}/{route_short_name}.pdf") as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if is_relevant_table_from_pdf(route_short_name, table):
                    timetables.append(table)
    print(f"Extracting trips for route {route_short_name}... ({len(timetables)} timetables found)")

    return timetables

def extract_trips_content_for_regional_route(route_short_name: str) -> str:
    timetables = extract_timetables_from_pdf(route_short_name)
    direction_ids = get_trip_direction_ids_from_timetables(timetables)
    
    trips_txt_content = ""
    for i, timetable in enumerate(timetables):    
        for j, row in enumerate(timetable):
            trip_headsigns = get_trip_headsigns_from_timetable(timetable)

            if len(row) > 2 and ((row[0] and "DÉPART" in row[0].replace(" ", "").upper())
                    or (row[1] and "DÉPART" in row[1].replace(" ", "").upper())):

                service_id = get_service_id_from_name("")
                for service_name, trip_number, headsign in zip(timetable[j-1], row, trip_headsigns):
                    if service_name:
                        service_id = get_service_id_from_name(service_name)
                    if trip_number and trip_number.isnumeric():
                        trips_txt_content += f"{route_short_name},{service_id},{route_short_name}D{trip_number},{headsign},{trip_number},{direction_ids[i]},TODO\n"

                break

    return trips_txt_content


def extract_trips_content_for_all_routes() -> None:
    trips_txt_content = "route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,shape_id\n"
    trips_txt_content += extract_trips_content_for_regional_route("32")
    trips_txt_content += extract_trips_content_for_regional_route("34")
    trips_txt_content += extract_trips_content_for_regional_route("50")
    trips_txt_content += extract_trips_content_for_regional_route("125")
    trips_txt_content += extract_trips_content_for_regional_route("131138")

    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)
    with open(f"{GTFS_OUTPUT_PATH}/trips.txt", "w", encoding="utf-8") as f:
        f.write(trips_txt_content)


if __name__ == "__main__":
    print("Extracting trips of routes...")
    extract_trips_content_for_all_routes()
