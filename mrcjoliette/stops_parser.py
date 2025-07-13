import os
import xml.etree.ElementTree as ET

MAPS_PATH = "./maps"
GTFS_OUTPUT_PATH = "./output"

KML_NAMESPACE = {
    "kml": "http://www.opengis.net/kml/2.2"
}


def extract_shapes_content_for_regional_route(route_short_name: str) -> str:
    tree = ET.parse(f"{MAPS_PATH}/{route_short_name}.kml")
    root = tree.getroot()

    shape_txt_content = ""
    placemarks = root.findall(".//kml:Placemark", KML_NAMESPACE)
    for placemark in placemarks:
        name = placemark.find("kml:name", KML_NAMESPACE)
        stop_name = name.text.strip() if name is not None else "(undefined)"

        point = placemark.find('.//kml:Point/kml:coordinates', KML_NAMESPACE)
        if point is not None:
            coords = point.text.strip()
            lon, lat, *_ = coords.split(',')  # Only take lon and lat
            print(f'📍 {stop_name}: Point ({lat}, {lon})')

    return shape_txt_content


def extract_shapes_content_for_regional_routes() -> None:
    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)

    shape_txt_content = "shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\n"
    shape_txt_content += extract_shapes_content_for_regional_route("32")
    shape_txt_content += extract_shapes_content_for_regional_route("34")
    shape_txt_content += extract_shapes_content_for_regional_route("50")
    shape_txt_content += extract_shapes_content_for_regional_route("125")
    shape_txt_content += extract_shapes_content_for_regional_route("131_138")

    with open(f"{GTFS_OUTPUT_PATH}/shapes.txt", "w") as f:
        f.write(shape_txt_content)


def main() -> None:
    print("Extracting shapes of routes...")
    extract_shapes_content_for_regional_routes()


if __name__ == "__main__":
    main()
