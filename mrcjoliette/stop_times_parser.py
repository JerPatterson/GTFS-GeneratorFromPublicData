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
    print(f"Extracting stop times for route {route_short_name}... ({len(timetables)} timetables found)")

    return timetables


def get_trip_ids_from_timetables(route_short_name: str, timetables: list[list[list[str | None]]]) -> list[list[str | None]]:
    trip_ids: list[list[str | None]] = []

    for timetable in timetables:
        trip_ids.append([])

        for row in timetable:
            if is_departure_header_row(row):
                for trip_number in row:
                    if trip_number and trip_number.isnumeric():
                        trip_ids[-1].append(f"{route_short_name}D{trip_number}")
                    else:
                        trip_ids[-1].append(None)

    return trip_ids

def get_stop_headsigns_from_timetables(timetables: list[list[list[str | None]]]) -> list[list[list[str]]]:
    stop_headsigns = []

    for timetable in timetables:
        stop_headsigns.append([[""] * len(timetable[0]) for _ in range(len(timetable))])
        furthest_headsigns = ["NONE"] * len(timetable)

        for i, row in enumerate(timetable):
            if i == 0:
                if row[1] and (not row[0] or len(row[1]) > len(row[0])):
                    furthest_headsigns = [row[1]] * len(row)
                elif row[0]:
                    furthest_headsigns = [row[0]] * len(row)

            for j, value in enumerate(row):
                if not value and row[1] and (not row[0] or len(row[1]) > len(row[0])):
                    furthest_headsigns[j] = row[1] if "/" not in row[1] else furthest_headsigns[j]
                elif not value and row[0]:
                    furthest_headsigns[j] = row[0] if "/" not in row[0] else furthest_headsigns[j]
                
                if value and len(value) == 5:
                    stop_headsigns[-1][i][j] = furthest_headsigns[j]

    return stop_headsigns

def get_pickup_types_from_timetables(timetables: list[list[list[str | None]]]) -> list[list[list[str]]]:
    stop_headsigns = get_stop_headsigns_from_timetables(timetables)
    pickup_types = map(lambda x: [["1" if "(DÉBARQUEMENT SEULEMENT)" in x else "0" for x in x] for x in x], stop_headsigns)

    return list(pickup_types)

def get_drop_off_types_from_timetables(timetables: list[list[list[str | None]]]) -> list[list[list[str]]]:
    stop_headsigns = get_stop_headsigns_from_timetables(timetables)
    drop_off_types = map(lambda x: [["1" if "(EMBARQUEMENT SEULEMENT)" in x else "0" for x in x] for x in x], stop_headsigns)

    return list(drop_off_types)


def extract_stop_times_content_for_regional_route(route_short_name: str) -> str:
    timetables = extract_timetables_from_pdf(route_short_name)

    trip_ids = get_trip_ids_from_timetables(route_short_name, timetables)
    pickup_types = get_pickup_types_from_timetables(timetables)
    drop_off_types = get_drop_off_types_from_timetables(timetables)
    pattern_24hr = r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"

    stop_times_txt_content = ""
    for i, timetable in enumerate(timetables):
        stop_sequence_numbers = [0] * len(timetable[0])

        for j, row in enumerate(timetable):
            stop_id = None
            for k, (trip_id, value, pickup_type, drop_off_type) in enumerate(zip(trip_ids[i], row, pickup_types[i][j], drop_off_types[i][j])):
                if value and value.isnumeric() and len(value) == 5:
                    stop_id = value

                elif stop_id and value and re.match(pattern_24hr, value[0:5]):
                    if len(value) > 5 and len(row) > k + 1 and not row[k + 1]:
                        row[k + 1] = value[5:].strip()
                        value = value[0:5]

                    stop_sequence_numbers[k] += 1
                    stop_times_txt_content += f"{trip_id},{value},{value},{stop_id},{stop_sequence_numbers[k]},{pickup_type},{drop_off_type}\n"

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
