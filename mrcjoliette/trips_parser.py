import os
import pdfplumber
import re

SCHEDULES_PATH = "./schedules"
GTFS_OUTPUT_PATH = "./output"


def is_departure_header_row(row: list[str]) -> bool:
    return len(row) > 2 and (
        (row[0] and "DÉPART" in row[0].replace(" ", "").upper()) or
        (row[1] and "DÉPART" in row[1].replace(" ", "").upper())
    )

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

def get_service_ids_from_timetables(timetables: list[list[list[str | None]]]) -> list[list[str]]:
    service_ids = []

    for i, timetable in enumerate(timetables):
        service_ids.append([""] * len(timetable[i]))

        for j, row in enumerate(timetable):
            if is_departure_header_row(row):
                service_id = get_service_id_from_name("")
                for k, service_name in enumerate(timetable[j-1]):
                    if service_name:
                        service_id = get_service_id_from_name(service_name)

                    service_ids[-1][k] = service_id

                break

    return service_ids

def get_trip_numbers_from_timetables(timetables: list[list[list[str | None]]]) -> list[list[str]]:
    trip_numbers = []

    for i, timetable in enumerate(timetables):
        trip_numbers.append([""] * len(timetable[i]))

        for row in timetable:
            if is_departure_header_row(row):
                for j, trip_number in enumerate(row):
                    if trip_number and trip_number.isnumeric():
                        trip_numbers[-1][j] = str(trip_number)

                break

    return trip_numbers

def get_trip_headsigns_from_timetables(timetables: list[list[list[str | None]]]) -> list[list[str]]:
    trip_headsigns = []

    for i, timetable in enumerate(timetables):
        trip_headsigns.append([""] * len(timetable[i]))
        furthest_headsigns = ["NONE"] * len(timetable[i])

        for j, row in enumerate(timetable):
            if j == 0:
                if row[1] and (not row[0] or len(row[1]) > len(row[0])):
                    furthest_headsigns = [row[1].split(" ")[-1]] * len(row)
                elif row[0]:
                    furthest_headsigns = [row[0].split(" ")[-1]] * len(row)

            for k, value in enumerate(row):
                if not value and row[1] and (not row[0] or len(row[1]) > len(row[0])):
                    furthest_headsigns[k] = row[1] if "/" not in row[1] else furthest_headsigns[k]
                elif not value and row[0]:
                    furthest_headsigns[k] = row[0] if "/" not in row[0] else furthest_headsigns[k]

                if value and len(value) == 5:
                    trip_headsigns[-1][k] = furthest_headsigns[k]

    return trip_headsigns

def get_direction_ids_from_timetables(timetables: list[list[list[str | None]]]) -> list[str]:
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

def get_stop_ids_of_trips_from_timetables(timetables: list[list[list[str | None]]]) -> list[list[list[str]]]:
    stop_ids: list[list[list[str]]] = []
    pattern_24hr = r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"

    for i, timetable in enumerate(timetables):
        stop_ids.append([[] for _ in range(len(timetable[i]))])

        for row in timetable:
            stop_id = None
            for j, value in enumerate(row):
                if value and value.isnumeric() and len(value) == 5:
                    stop_id = value

                elif stop_id and value and re.match(pattern_24hr, value[0:5]):
                    if len(value) > 5 and len(row) > j + 1 and not row[j + 1]:
                        row[j + 1] = value[5:].strip()
                        value = value[0:5]

                    stop_ids[-1][j].append(stop_id)

    return stop_ids

def get_shape_ids_from_timetables(route_short_name: str, timetables: list[list[list[str | None]]]) -> list[str | None]:
    shape_ids = []
    stop_ids_of_trips = get_stop_ids_of_trips_from_timetables(timetables)

    for i, timetable in enumerate(timetables):
        shape_ids.append([""] * len(timetable[i]))

        shape_id_by_stop_count = {}
        unique_stop_counts = set(map(lambda x: len(x), stop_ids_of_trips[i]))
        unique_stop_counts.remove(0)

        for j, stop_count in enumerate(sorted(unique_stop_counts, reverse=True)):
            shape_id_by_stop_count[stop_count] = f"{route_short_name}DIR{i}V{j + 1}"

        for j, stop_ids in enumerate(stop_ids_of_trips[i]):
            if len(stop_ids) in shape_id_by_stop_count:
                shape_ids[i][j] = shape_id_by_stop_count[len(stop_ids)]
            else:
                shape_ids[i][j] = None

    return shape_ids


def extract_trips_content_for_local_route(route_short_name: str) -> str:
    timetables: list[list[str | None]] = []
    with pdfplumber.open(f"{SCHEDULES_PATH}/{route_short_name}.pdf") as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                timetables.append(table)
    print(f"Extracting trips for route {route_short_name}... ({len(timetables)} timetable found)")

    trips_txt_content = ""
    for i, timetable in enumerate(timetables):
        for j in range(1, len(timetable[i][2:]) + 1):
            trips_txt_content += f"{route_short_name},{"SEMAINE" if j < 3 else "REGULIER"},{route_short_name}D{j},,{j},{i},{route_short_name}DIR0V1\n"

    return trips_txt_content

def extract_trips_content_for_regional_route(route_short_name: str) -> str:
    timetables = extract_timetables_from_pdf(route_short_name)

    service_ids = get_service_ids_from_timetables(timetables)
    trip_numbers = get_trip_numbers_from_timetables(timetables)
    trip_headsigns = get_trip_headsigns_from_timetables(timetables)
    direction_ids = get_direction_ids_from_timetables(timetables)
    shape_ids = get_shape_ids_from_timetables(route_short_name, timetables)

    # Hard coded because of the structure of its timetable
    if route_short_name == "131138":
        service_ids[-1] = service_ids[0]
    
    trips_txt_content = ""
    for i in range(len(timetables)):
        for service_id, trip_number, trip_headsign, shape_id in zip(service_ids[i], trip_numbers[i], trip_headsigns[i], shape_ids[i]):
            if trip_number and trip_number.isnumeric():
                trips_txt_content += f"{route_short_name},{service_id},{route_short_name}D{trip_number},{trip_headsign},{trip_number},{direction_ids[i]},{shape_id}\n"


    return trips_txt_content


def extract_trips_content_for_all_routes() -> None:
    trips_txt_content = "route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,shape_id\n"
    trips_txt_content += extract_trips_content_for_local_route("A")
    trips_txt_content += extract_trips_content_for_local_route("B")
    trips_txt_content += extract_trips_content_for_local_route("C")
    trips_txt_content += extract_trips_content_for_local_route("D")
    trips_txt_content += extract_trips_content_for_local_route("E")
    trips_txt_content += extract_trips_content_for_local_route("X")
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
