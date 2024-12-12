import json
from json import JSONDecodeError


import logging
import os

FoxDict = list[dict]

json_file = "animals_data.json"


def setup_logging() -> logging:
    """
    setup global logger for debugging
    :return:
    :rtype:
    """
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
    """
    load data from json file
    :param json_file:
    :type json_file:
    :param logger:
    :type logger:
    :return:
    :rtype:
    """
    try:
        logger.info("loading data from %s", json_file)
        with open(json_file, "r", encoding="utf-8") as handler:
            if handler:
                logger.info(f"{json_file} loaded")
                data = json.load(handler)
            else:
                logger.error(f"{json_file} empty")
    except FileNotFoundError:
        logger.error(f"{json_file} not found")
    except JSONDecodeError:
        logger.error(f"{json_file} could not be decoded")
    except Exception as e:
        logger.error("Unexpected error caught %s", e)
    return data


def sort_fox_dict(fox_dict: FoxDict, logger: logging) -> FoxDict:
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
        logger.info("fox_dict found starting to parse")
        for item in fox_dict:
            name = item.get("name", "")
            characteristics = item.get("characteristics", {})
            diet = characteristics.get("diet", "")
            top_speed = characteristics.get("top_speed", "")
            fox_type = characteristics.get("type", "")
            target_skin_type = characteristics.get("skin_type", "")
            location = item.get("locations", [])
            taxonomy = item.get("taxonomy", {})
            family = taxonomy.get("family", "")
            genus = taxonomy.get("genus", "")
            details = {
                "Name": name,
                "Family": family,
                "Genus": genus,
                "Top Speed": top_speed,
                "Diet": diet,
                "Location": location[0] if location else None,
                "Type": fox_type,
                "Skin Type": target_skin_type,
            }
            sorted_foxs.append({key: value for key, value in details.items() if value})
            logger.info(f"Fox added to list with {details}")
    else:
        logger.error("fox_dict is empty")
    return sorted_foxs


def print_sorted_fox(sorted_foxs: FoxDict, logger: logging) -> None:
    """
    function for printing sorted fox to display
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


def create_content(sorted_foxs: FoxDict, logger: logging) -> str:
    """
    create content for animals.html
    :param sorted_foxs:
    :type sorted_foxs:
    :param logger:
    :type logger:
    :return:
    :rtype:
    """
    logger.info("Starting to create content for template")
    content = "\n"
    serialize_start = '          <li class="cards__item">\n'
    serialize_end = "          </ul>\n</p>\n</li>"
    if sorted_foxs:
        logger.info("sorted_foxs found")

        for fox in sorted_foxs:
            content += serialize_start
            name_key, name_value = next(iter(fox.items()))
            content += (
                f'<div class="card__title">{name_value}</div>\n'
                f'<p class="card__text">\n'
                "<ul>\n"
            )

            for key, value in list(fox.items())[1:]:
                item = f"            <li>{key.ljust(8)}: {value}</li>\n"
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


def get_skin_types(fox_dict: FoxDict, logger: logging) -> set:
    logger.info("parsing fox_dict for skin types")
    skin_types = set()
    if fox_dict:
        logging.info("fox_dict found starting to parse")
        for item in fox_dict:
            characteristics = item.get("characteristics", {})
            skin_type = characteristics.get("skin_type", "")
            if skin_type and skin_type not in skin_types:
                skin_types.add(skin_type)
                logger.info(f"skin type added: {skin_type}")
    logging.info("skin types defined %s", skin_types)
    return skin_types


def display_skin_types(skin_types: set, logger: logging) -> set:
    """
    display skin types
    :param skintypes:
    :type skintypes:
    :return:
    :rtype:
    """
    logger.info("displaying skin types")
    print("Available Skin types to choose from:")
    for idx, skin_type in enumerate(skin_types):
        print(f"{str(idx+1).ljust(2)}: {skin_type}")
    return skin_types


def get_skin_type_input(skin_types: set, logger: logging) -> str:
    """
    get user input for generating new webpage
    based on skin type
    :return:
    :rtype:
    """
    logger.info("getting user input for skin types")
    while True:
        choice = input("What skin type do you want to select ?").lower().strip()
        if choice.capitalize() in skin_types:
            print(f"{choice.capitalize()} selected")
            logger.info(f"Skin type {choice} selected")
            return choice
        else:
            print("invalid option")
            print("Valid options are:")
            for idx, skin_type in enumerate(skin_types):
                print(f"{str(idx + 1).ljust(2)}: {skin_type}")
            continue


def create_filtered_html(content: str, logger: logging, choice) -> None:
    logger.info("starting to populate animal.html")
    template = "animals_template.html"
    animal_page = f"animal_with_{choice}.html"
    replace_text = "__REPLACE_ANIMALS_INFO__"
    replace_title = "My Animal Repository"
    new_title = f"Animals filtered by skin type: {choice.capitalize()}"
    print(f"Generating {animal_page}")

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
        new_page_title = template_data.replace(replace_title, new_title)
        animal_page_contents = new_page_title.replace(replace_text, content)
        logger.info(f"New content for {animal_page} created")
        logger.debug(f"Content being written to {animal_page}: {content}")
        try:
            logger.info(f"trying to open or create {animal_page}")
            with open(animal_page, "w", encoding="utf-8") as handler:
                handler.write(animal_page_contents)
                logger.info(f"created new content for {animal_page}")
                print(f"{animal_page} created")
        except Exception as e:
            logger.error("Unexpected error caught %s", e)
    else:
        logger.error("sorted fox dictionary is empty")


def filter_fox_dict(fox_dict: FoxDict, logger: logging, choice: str) -> FoxDict:
    """
    get the fox_dict and get specific fields from it.
    diet, location, type and name.
    if empty do not print
    :param foxdict:
    :type foxdict:
    :return:
    """
    print(f"Generating content for page filtered by skin type: {choice}")
    logger.info("Starting to filter Foxes")
    filtered_foxs = []
    if fox_dict:
        logger.info("fox_dict found starting to parse")
        for item in fox_dict:
            name = item.get("name", "")
            characteristics = item.get("characteristics", {})
            diet = characteristics.get("diet", "")
            top_speed = characteristics.get("top_speed", "")
            fox_type = characteristics.get("type", "")
            target_skin_type = characteristics.get("skin_type", "")
            location = item.get("locations", [])
            taxonomy = item.get("taxonomy", {})
            family = taxonomy.get("family", "")
            genus = taxonomy.get("genus", "")
            if choice.capitalize() == target_skin_type:
                details = {
                    "Name": name,
                    "Family": family,
                    "Genus": genus,
                    "Top Speed": top_speed,
                    "Diet": diet,
                    "Location": location[0] if location else None,
                    "Type": fox_type,
                    "Skin Type": target_skin_type,
                }
                filtered_foxs.append(
                    {key: value for key, value in details.items() if value}
                )
                logger.info(f"Fox added to filtered_fox list with {details}")
    else:
        logger.error("fox_dict is empty")
    print("Content generated")
    return filtered_foxs


def main() -> None:
    logger = setup_logging()
    logger.info("animal_web_generator started")
    fox_dict = load_data(json_file=json_file, logger=logger)
    sorted_foxy = sort_fox_dict(fox_dict=fox_dict, logger=logger)
    animal_content = create_content(sorted_foxs=sorted_foxy, logger=logger)
    populate_animal_html(animal_content, logger)
    skin_types = get_skin_types(fox_dict=fox_dict, logger=logger)
    display_skin_types(skin_types, logger)
    choice = get_skin_type_input(skin_types, logger)
    filtered_fox = filter_fox_dict(fox_dict, logger, choice)
    filter_content = create_content(sorted_foxs=filtered_fox, logger=logger)
    create_filtered_html(filter_content, logger, choice)


if __name__ == "__main__":
    main()
