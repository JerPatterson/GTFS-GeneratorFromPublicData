import os

GTFS_OUTPUT_PATH = "./output"


def create_routes_content_for_all_routes() -> None:
    routes_txt_content = "route_id,agency_id,route_short_name,route_long_name,route_type,route_url,route_color,route_text_color\n"
    routes_txt_content += create_routes_content_for_local_routes()
    routes_txt_content += create_routes_content_for_regional_routes()

    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)
    with open(f"{GTFS_OUTPUT_PATH}/routes.txt", "w", encoding="utf-8") as f:
        f.write(routes_txt_content)


def create_routes_content_for_local_routes(routes_txt_content = "") -> str:
    routes_txt_content += "A,mrcjoliette,A,Circuit A,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-urbains/,FCDC12,000000\n"
    routes_txt_content += "B,mrcjoliette,B,Circuit B,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-urbains/,00693F,FFFFFF\n"
    routes_txt_content += "C,mrcjoliette,C,Circuit C,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-urbains/,1263B0,FFFFFF\n"
    routes_txt_content += "D,mrcjoliette,D,Circuit D,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-urbains/,4B0082,FFFFFF\n"
    routes_txt_content += "E,mrcjoliette,E,Circuit E,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-urbains/,FA8901,FFFFFF\n"
    routes_txt_content += "X,mrcjoliette,X,Circuit X-Express,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-urbains/,000000,FFFFFF\n"

    return routes_txt_content

def create_routes_content_for_regional_routes(routes_txt_content = "") -> str:
    routes_txt_content += "32,mrcjoliette,32,Joliette / Saint-Michel-des-Saints,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuit-32-joliette-saint-michel-des-saints/,81A449,FFFFFF\n"
    routes_txt_content += "34,mrcjoliette,34,Joliette / Rawdon,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuit-34-joliette-rawdon/,81A449,FFFFFF\n"
    routes_txt_content += "50,mrcjoliette,50,Joliette / Repentigny / Montréal,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuit-50-joliette-montreal/,81A449,FFFFFF\n"
    routes_txt_content += "125,mrcjoliette,125,Saint-Donat / Chertsey / Montréal,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuit-125-saint-donat-chertsey-montreal/,81A449,FFFFFF\n"
    routes_txt_content += "131138,mrcjoliette,131-138,Joliette / Berthierville,3,https://mrcjoliette.qc.ca/transport-mrc-joliette/circuits-regionaux/circuits-131-138-joliette-berthierville/,81A449,FFFFFF\n"

    return routes_txt_content


def main() -> None:
    print("Creating routes information...")
    create_routes_content_for_all_routes()


if __name__ == "__main__":
    main()
