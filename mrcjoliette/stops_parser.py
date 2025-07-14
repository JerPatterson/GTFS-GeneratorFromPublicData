import os
import xml.etree.ElementTree as ET

MAPS_PATH = "./maps"
GTFS_OUTPUT_PATH = "./output"

KML_NAMESPACE = {
    "kml": "http://www.opengis.net/kml/2.2"
}


def extract_shapes_content_for_regional_route(stops: set[str], route_short_name: str) -> str:
    print(f"Extracting stops for route: {route_short_name}...")
    tree = ET.parse(f"{MAPS_PATH}/{route_short_name}.kml")
    root = tree.getroot()

    stops_txt_content = ""
    placemarks = root.findall(".//kml:Placemark", KML_NAMESPACE)
    for placemark in placemarks:
        name = placemark.find("kml:name", KML_NAMESPACE)
        name_text = name.text.strip() if name is not None else "(undefined)"
        stop_id, stop_name = name_text.split(" - ", 1) if " - " in name_text else ("(undefined)", name_text)

        point = placemark.find(".//kml:Point/kml:coordinates", KML_NAMESPACE)
        if point is not None:
            coords = point.text.strip()
            lon, lat, *_ = coords.split(",")

            if stop_id not in stops:
                stops_txt_content += f"{stop_id},{stop_id if "?" not in stop_id else ""},{stop_name},{lat},{lon}\n"
                stops.add(stop_id)

    return stops_txt_content


def extract_shapes_content_for_regional_routes() -> None:
    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)

    stops = set()
    stops_txt_content = "stop_id,stop_code,stop_name,stop_lat,stop_lon\n"
    stops_txt_content += extract_shapes_content_for_regional_route(stops, "32")
    stops_txt_content += extract_shapes_content_for_regional_route(stops, "34")
    stops_txt_content += extract_shapes_content_for_regional_route(stops, "50")
    stops_txt_content += extract_shapes_content_for_regional_route(stops, "125")
    stops_txt_content += extract_shapes_content_for_regional_route(stops, "131138")

    with open(f"{GTFS_OUTPUT_PATH}/stops.txt", "w", encoding="utf-8") as f:
        f.write(stops_txt_content)


def main() -> None:
    print("Extracting stops of routes...")
    extract_shapes_content_for_regional_routes()


if __name__ == "__main__":
    main()
