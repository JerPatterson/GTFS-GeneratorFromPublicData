import os

GTFS_OUTPUT_PATH = "./output"


def create_agency_content() -> None:
    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)

    agency_txt_content = "agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_email\n"
    agency_txt_content += "mrcjoliette,MRC de Joliette,https://mrcjoliette.qc.ca/transport-mrc-joliette/,America/Montreal,fr,450-756-2785,info.transport@mrcjoliette.qc.ca\n"

    with open(f"{GTFS_OUTPUT_PATH}/agency.txt", "w", encoding="utf-8") as f:
        f.write(agency_txt_content)


def main() -> None:
    print("Creating agency information...")
    create_agency_content()


if __name__ == "__main__":
    main()
