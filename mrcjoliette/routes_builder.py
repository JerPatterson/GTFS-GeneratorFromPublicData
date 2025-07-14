import os

GTFS_OUTPUT_PATH = "./output"

KML_NAMESPACE = {
    "kml": "http://www.opengis.net/kml/2.2"
}


def create_routes_content_for_regional_routes() -> None:
    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)

    routes_txt_content = "route_id,agency_id,route_short_name,route_long_name,route_type,route_url,route_color,route_text_color\n"
    routes_txt_content += "32,mrcjoliette,32,Joliette / Saint-Michel-des-Saints,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuit-32-joliette-saint-michel-des-saints/,81A449,FFFFFF\n"
    routes_txt_content += "34,mrcjoliette,34,Joliette / Rawdon,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuit-34-joliette-rawdon/,81A449,FFFFFF\n"
    routes_txt_content += "50,mrcjoliette,50,Joliette / Repentigny / Montréal,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuit-50-joliette-montreal/,81A449,FFFFFF\n"
    routes_txt_content += "125,mrcjoliette,125,Saint-Donat / Chertsey / Montréal,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuit-125-saint-donat-chertsey-montreal/,81A449,FFFFFF\n"
    routes_txt_content += "131138,mrcjoliette,131-138,Joliette / Berthierville,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuits-131-138-joliette-berthierville/,81A449,FFFFFF\n"

    with open(f"{GTFS_OUTPUT_PATH}/routes.txt", "w", encoding="utf-8") as f:
        f.write(routes_txt_content)


def main() -> None:
    print("Creating routes information...")
    create_routes_content_for_regional_routes()


if __name__ == "__main__":
    main()
