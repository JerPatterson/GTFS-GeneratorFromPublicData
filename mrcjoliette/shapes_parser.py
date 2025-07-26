import os
import xml.etree.ElementTree as ET

MAPS_PATH = "./maps"
GTFS_OUTPUT_PATH = "./output"

KML_NAMESPACE = {
    "kml": "http://www.opengis.net/kml/2.2"
}


def extract_shapes_content_for_route(route_short_name: str) -> str:
    tree = ET.parse(f"{MAPS_PATH}/{route_short_name}.kml")
    root = tree.getroot()

    shape_txt_content = ""
    placemarks = root.findall(".//kml:Placemark", KML_NAMESPACE)
    for placemark in placemarks:
        name = placemark.find("kml:name", KML_NAMESPACE)
        shape_name = name.text.strip() if name is not None else "(undefined)"

        linestring = placemark.find(".//kml:LineString/kml:coordinates", KML_NAMESPACE)
        if linestring is not None:
            print(f"Extracting shape (ID: {shape_name}) for route {route_short_name}...")
            coord_lines = linestring.text.strip().split()
            for i, coord in enumerate(coord_lines):
                lon, lat, *_ = coord.split(",")
                shape_txt_content += f"{shape_name},{lat},{lon},{i+1}\n"

    return shape_txt_content


def extract_shapes_content_for_all_routes() -> None:
    shape_txt_content = "shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\n"
    shape_txt_content += extract_shapes_content_for_local_routes()
    shape_txt_content += extract_shapes_content_for_regional_routes()

    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)
    with open(f"{GTFS_OUTPUT_PATH}/shapes.txt", "w") as f:
        f.write(shape_txt_content)


def extract_shapes_content_for_local_routes(shape_txt_content = "") -> str:
    shape_txt_content += extract_shapes_content_for_route("A")
    shape_txt_content += extract_shapes_content_for_route("B")
    shape_txt_content += extract_shapes_content_for_route("C")
    shape_txt_content += extract_shapes_content_for_route("D")
    shape_txt_content += extract_shapes_content_for_route("E")
    shape_txt_content += extract_shapes_content_for_route("X")

    return shape_txt_content


def extract_shapes_content_for_regional_routes(shape_txt_content = "") -> str:
    shape_txt_content += extract_shapes_content_for_route("32")
    shape_txt_content += extract_shapes_content_for_route("34")
    shape_txt_content += extract_shapes_content_for_route("50")
    shape_txt_content += extract_shapes_content_for_route("125")
    shape_txt_content += extract_shapes_content_for_route("131138")

    return shape_txt_content


def main() -> None:
    print("Extracting shapes of routes...")
    extract_shapes_content_for_all_routes()


if __name__ == "__main__":
    main()
