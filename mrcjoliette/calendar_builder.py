import os

GTFS_OUTPUT_PATH = "./output"

START_DATE = "20250101"
END_DATE = "20251231"


def create_calendar_content() -> None:
    os.makedirs(GTFS_OUTPUT_PATH, exist_ok=True)

    calendar_txt_content = "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n"
    calendar_txt_content += f"REGULIER,1,1,1,1,1,1,1,{START_DATE},{END_DATE}\n"
    calendar_txt_content += f"SEMAINE,1,1,1,1,1,0,0,{START_DATE},{END_DATE}\n"
    calendar_txt_content += f"LUNDI_JEUDI,1,1,1,1,0,0,0,{START_DATE},{END_DATE}\n"
    calendar_txt_content += f"FIN_DE_SEMAINE,0,0,0,0,0,1,1,{START_DATE},{END_DATE}\n"
    calendar_txt_content += f"VENDREDI,0,0,0,0,1,0,0,{START_DATE},{END_DATE}\n"
    calendar_txt_content += f"SAMEDI,0,0,0,0,0,1,0,{START_DATE},{END_DATE}\n"
    calendar_txt_content += f"DIMANCHE,0,0,0,0,0,0,1,{START_DATE},{END_DATE}\n"

    with open(f"{GTFS_OUTPUT_PATH}/calendar.txt", "w", encoding="utf-8") as f:
        f.write(calendar_txt_content)


def main() -> None:
    print("Creating calendar information...")
    create_calendar_content()


if __name__ == "__main__":
    main()
