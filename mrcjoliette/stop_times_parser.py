import os
import pdfplumber
import re

MAPS_PATH = "./maps"
SCHEDULES_PATH = "./schedules"
GTFS_OUTPUT_PATH = "./output"

KML_NAMESPACE = {
    "kml": "http://www.opengis.net/kml/2.2"
}


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
    print(f"Extracting stop times for route {route_short_name}... ({len(timetables)} timetables found)")

    return timetables

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


def extract_stop_times_content_for_regional_route(route_short_name: str) -> str:
    timetables = extract_timetables_from_pdf(route_short_name)

    direction_id = 0
    trip_ids_of_direction: list[list[str | None]] = []
    pattern_24hr = r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"

    stop_times_txt_content = ""
    for timetable in timetables:
        stop_sequence_numbers: list[int] = []
        trip_ids_of_direction.append([])
        trip_headsigns = [""] * len(timetable[0])
        furthest_headsigns = ["NONE"] * len(timetable[0])

        for row in timetable:
            if len(row) > 2 and ((row[0] and "DÉPART" in row[0].replace(" ", "").upper())
                    or (row[1] and "DÉPART" in row[1].replace(" ", "").upper())):
                
                for trip_number in row:
                    stop_sequence_numbers.append(0)
                    if trip_number and trip_number.isnumeric():    
                        trip_ids_of_direction[-1].append(f"{route_short_name}D{trip_number}")
                    else:
                        trip_ids_of_direction[-1].append(None)

            if len(trip_ids_of_direction[direction_id]) > 0:
                
                stop_id = None
                for j, value in enumerate(row):
                    if not value and row[1] and (not row[0] or len(row[1]) > len(row[0])):
                        furthest_headsigns[j] = row[1] if "/" not in row[1] else furthest_headsigns[j]
                    elif not value and row[0]:
                        furthest_headsigns[j] = row[0] if "/" not in row[0] else furthest_headsigns[j]

                    if value and len(value) == 5:
                        trip_headsigns[j] = furthest_headsigns[j]

                    if value and value.isnumeric() and len(value) == 5:
                        stop_id = value

                    elif stop_id and value and re.match(pattern_24hr, value[0:5]):
                        if len(value) > 5 and len(row) > j + 1 and not row[j + 1]:
                            row[j + 1] = value[5:].strip()
                            value = value[0:5]

                        stop_sequence_numbers[j] += 1
                        stop_pickup_type = "1" if "(DÉBARQUEMENT SEULEMENT)" in trip_headsigns[j] else "0"
                        stop_drop_off_type = "1" if "(EMBARQUEMENT SEULEMENT)" in trip_headsigns[j] else "0"
                        stop_times_txt_content += f"{trip_ids_of_direction[direction_id][j]},{value},{value},{stop_id},{stop_sequence_numbers[j]},{stop_pickup_type},{stop_drop_off_type}\n"

        direction_id += 1

    return stop_times_txt_content


def extract_stop_times_content_for_all_routes() -> None:
    trips_txt_content = "trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type\n"
    trips_txt_content += extract_stop_times_content_for_regional_route("32")
    trips_txt_content += extract_stop_times_content_for_regional_route("34")
    trips_txt_content += extract_stop_times_content_for_regional_route("50")
    trips_txt_content += extract_stop_times_content_for_regional_route("125")
    trips_txt_content += extract_stop_times_content_for_regional_route("131138")

    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)
    with open(f"{GTFS_OUTPUT_PATH}/stop_times.txt", "w", encoding="utf-8") as f:
        f.write(trips_txt_content)


if __name__ == "__main__":
    print("Extracting stop times of routes...")
    extract_stop_times_content_for_all_routes()
