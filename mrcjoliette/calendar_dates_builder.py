import os

GTFS_OUTPUT_PATH = "./output"


def create_calendar_dates_content() -> None:
    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)

    calendar_txt_content = "service_id,date,exception_type\n"

    calendar_txt_content += f"DIMANCHE,20250101,1\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,20250101,1\n"
    calendar_txt_content += f"SEMAINE,20250101,2\n"
    calendar_txt_content += f"LUNDI_JEUDI,20250101,2\n"

    calendar_txt_content += f"DIMANCHE,20250102,1\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,20250102,1\n"
    calendar_txt_content += f"SEMAINE,20250102,2\n"
    calendar_txt_content += f"LUNDI_JEUDI,20250102,2\n"

    calendar_txt_content += f"DIMANCHE,20250419,1\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,20250419,1\n"
    calendar_txt_content += f"SEMAINE,20250419,2\n"
    calendar_txt_content += f"LUNDI_JEUDI,20250419,2\n"

    calendar_txt_content += f"DIMANCHE,20250624,1\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,20250624,1\n"
    calendar_txt_content += f"SEMAINE,20250624,2\n"
    calendar_txt_content += f"LUNDI_JEUDI,20250624,2\n"

    calendar_txt_content += f"DIMANCHE,20250701,1\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,20250701,1\n"
    calendar_txt_content += f"SEMAINE,20250701,2\n"
    calendar_txt_content += f"LUNDI_JEUDI,20250701,2\n"

    calendar_txt_content += f"DIMANCHE,20250901,1\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,20250901,1\n"
    calendar_txt_content += f"SEMAINE,20250901,2\n"
    calendar_txt_content += f"LUNDI_JEUDI,20250901,2\n"

    calendar_txt_content += f"DIMANCHE,20251013,1\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,20251013,1\n"
    calendar_txt_content += f"SEMAINE,20251013,2\n"
    calendar_txt_content += f"LUNDI_JEUDI,20251013,2\n"

    calendar_txt_content += f"VENDREDI,20251224,1\n"
    calendar_txt_content += f"LUNDI_JEUDI,20251224,2\n"

    calendar_txt_content += f"DIMANCHE,20251225,1\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,20251225,1\n"
    calendar_txt_content += f"SEMAINE,20251225,2\n"
    calendar_txt_content += f"LUNDI_JEUDI,20251225,2\n"

    calendar_txt_content += f"DIMANCHE,20251226,1\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,20251226,1\n"
    calendar_txt_content += f"SEMAINE,20251226,2\n"
    calendar_txt_content += f"VENDREDI,20251226,2\n"

    calendar_txt_content += f"VENDREDI,20251231,1\n"
    calendar_txt_content += f"LUNDI_JEUDI,20251231,2\n"

    with open(f"{GTFS_OUTPUT_PATH}/calendar_dates.txt", "w", encoding="utf-8") as f:
        f.write(calendar_txt_content)


def main() -> None:
    print("Creating calendar dates information...")
    create_calendar_dates_content()


if __name__ == "__main__":
    main()
