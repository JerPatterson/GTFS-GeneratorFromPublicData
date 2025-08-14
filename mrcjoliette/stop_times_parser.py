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

def extract_stop_times_content_for_regional_route(route_short_name: str) -> str:
    timetables = extract_timetables_from_pdf(route_short_name)

    direction_id = 0
    trip_ids_of_direction: list[list[str | None]] = []
    pattern_24hr = r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"

    stop_times_txt_content = ""
    for timetable in timetables:
        stop_sequence_numbers: list[int] = []
        trip_ids_of_direction.append([])
        
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
                for i, value in enumerate(row):
                    if value and value.isnumeric() and len(value) == 5:
                        stop_id = value
                    elif stop_id and value and re.match(pattern_24hr, value):
                        stop_sequence_numbers[i] += 1
                        stop_times_txt_content += f"{trip_ids_of_direction[direction_id][i]},{value},{value},{stop_id},{stop_sequence_numbers[i]},0,0\n"
                    elif stop_id and value and len(value) > 5 and re.match(pattern_24hr, value[0:5]) and len(row) > i + 1 and not row[i + 1]:
                        stop_sequence_numbers[i] += 1
                        row[i + 1] = value[5:].strip()
                        stop_times_txt_content += f"{trip_ids_of_direction[direction_id][i]},{value[0:5]},{value[0:5]},{stop_id},{stop_sequence_numbers[i]},0,0\n"

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
