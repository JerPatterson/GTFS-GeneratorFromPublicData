import os

GTFS_OUTPUT_PATH = "./output"


def create_feed_info_content() -> None:
    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)

    feed_info_txt_content = "feed_publisher_name,feed_publisher_url,feed_lang,feed_start_date,feed_end_date,feed_version,feed_contact_email\n"
    feed_info_txt_content += "MRC de Joliette,https://mrcjoliette.qc.ca/transport-mrc-joliette/,fr,20250101,20251231,1.0,info.transport@mrcjoliette.qc.ca\n"

    with open(f"{GTFS_OUTPUT_PATH}/feed_info.txt", "w", encoding="utf-8") as f:
        f.write(feed_info_txt_content)


def main() -> None:
    print("Creating feed information...")
    create_feed_info_content()


if __name__ == "__main__":
    main()
