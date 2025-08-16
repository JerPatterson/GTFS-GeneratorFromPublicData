import zipfile
import glob
import os

from agency_builder import create_agency_content
from calendar_builder import create_calendar_content
from calendar_dates_builder import create_calendar_dates_content
from feed_info_builder import create_feed_info_content
from routes_builder import create_routes_content_for_all_routes
from shapes_parser import extract_shapes_content_for_all_routes
from stop_times_parser import extract_stop_times_content_for_all_routes
from stops_parser import extract_stops_content_for_all_routes
from trips_parser import extract_trips_content_for_all_routes


def main() -> None:
    create_agency_content()
    create_calendar_content()
    create_calendar_dates_content()
    create_feed_info_content()
    create_routes_content_for_all_routes()
    extract_shapes_content_for_all_routes()
    extract_stop_times_content_for_all_routes()
    extract_stops_content_for_all_routes()
    extract_trips_content_for_all_routes()

    folder = "./output"
    zip_name = "mrcjoliette.zip"

    with zipfile.ZipFile(zip_name, 'w') as zf:
        for file in glob.glob(os.path.join(folder, "*.txt")):
            zf.write(file, os.path.basename(file))


if __name__ == "__main__":
    main()
