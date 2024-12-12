import json
from json import JSONDecodeError


import logging
import os

FoxDict = list[dict]

json_file = "animals_data.json"


def setup_logging() -> logging:
    folder = "logging"
    file_name = "logs.txt"
    path = os.path.join(folder, file_name)
    os.makedirs(folder, exist_ok=True)
    logging.basicConfig(
        filename=path,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("logging started...")
    return logger


def load_data(json_file, logger: logging) -> FoxDict:
    try:
        logger.info("loading data from %s", json_file)
        with open(json_file, "r", encoding="utf-8") as handler:
            if handler:
                logger.info(f"{json_file} loaded")
                return json.load(handler)
            else:
                logger.error(f"{json_file} empty")
    except FileNotFoundError:
        logger.error(f"{json_file} not found")
    except JSONDecodeError:
        logger.error(f"{json_file} could not be decoded")
    except Exception as e:
        logger.error("Unexpected error caught %s", e)


def step_1(fox_dict: FoxDict, logger: logging) -> FoxDict:
    """
    get the fox_dict and get specific fields from it.
    diet, location, type and name.
    if empty do not print
    :param foxdict:
    :type foxdict:
    :return:
    """
    logger.info("Starting to sort Foxes as per Step1")
    sorted_foxs = []
    if fox_dict:
        logging.info("fox_dict found starting to parse")
        for item in fox_dict:
            name = item.get("name", "")
            characteristics = item.get("characteristics", {})
            diet = characteristics.get("diet", "")
            location = item.get("locations", [])
            fox_type = characteristics.get("type", "")

            details = {
                "Name": name,
                "Diet": diet,
                "Location": location[0] if location else None,
                "Type": fox_type,
            }
            sorted_foxs.append({key: value for key, value in details.items() if value})
            logger.info(f"Fox added to list with {details}")
    else:
        logging.error("fox_dict is empty")
    return sorted_foxs


def print_sorted_fox(sorted_foxs: list[dict], logger: logging) -> None:
    """
    :param sorted_foxs:
    :type sorted_foxs:
    :return:
    :rtype:
    """
    logger.info("Starting to print sorted foxs to display")
    if sorted_foxs:
        logger.info("sorted_foxs found")
        for fox in sorted_foxs:
            for key, value in fox.items():
                print(f"{key} : {value}")
            print()
        else:
            logger.error("sorted foxs is empty")
    logger.info(("finished printing sorted_foxes"))


def create_content(sorted_foxs: list[dict], logger: logging) -> str:
    logger.info("Starting to create content for template")
    content = "\n"
    serialize_start = '          <li class="cards__item">\n'
    serialize_end = "          </li>\n"
    if sorted_foxs:
        logger.info("sorted_foxs found")

        for fox in sorted_foxs:
            content += serialize_start
            for key, value in fox.items():
                item = f"            {key.ljust(8)}: {value}<br> \n"
                content += item
            content += serialize_end

        else:
            logger.error("sorted foxs is empty")
    logger.info(("finished printing sorted_foxes"))
    return content


def populate_animal_html(content: str, logger: logging) -> None:
    logger.info("starting to populate animal.html")
    template = "animals_template.html"
    animal_page = "animals.html"
    replace_text = "__REPLACE_ANIMALS_INFO__"
    if content:
        try:
            logger.info("trying to open template file %s", template)
            with open(template, "r", encoding="utf-8") as handler:
                template_data = handler.read()
                logger.info("template file opened %s", template)
        except FileNotFoundError:
            logger.error(f"{template} not found")
        except Exception as e:
            logger.error("Unexpected error caught %s", e)
        animal_page_contents = template_data.replace(replace_text, content)
        logger.info(f"New content for {animal_page} created")
        logger.debug(f"Content being written to {animal_page}: {content}")
        try:
            logger.info(f"trying to open or create {animal_page}")
            with open(animal_page, "w", encoding="utf-8") as handler:
                handler.write(animal_page_contents)
                logger.info(f"created new content for {animal_page}")
        except Exception as e:
            logger.error("Unexpected error caught %s", e)
    else:
        logger.error("sorted fox dictionary is empty")


def main() -> None:
    logger = setup_logging()
    logger.info("animal_web_generator started")
    fox_dict = load_data(json_file, logger)
    ans_task1 = step_1(fox_dict, logger)
    content = create_content(ans_task1, logger)
    print(content)
    populate_animal_html(content, logger)


if __name__ == "__main__":
    main()
