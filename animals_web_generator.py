import json

FoxDict = list[dict]


def load_data(json_file) -> FoxDict:
    with open(json_file, "r") as handler:
        return json.load(handler)


def step_1(fox_dict: FoxDict) -> FoxDict:
    """
    get the fox_dict and get specific fields from it.
    diet, location, type and name.
    if empty do not print
    :param foxdict:
    :type foxdict:
    :return:
    """

    sorted_foxs = []

    for item in fox_dict:
        name = item.get("name", "")
        characteristics = item.get("characteristics", {})
        diet = characteristics.get("diet", "")
        location = item.get("locations", [])
        fox_type = characteristics.get("type", "")

        details = {
            "Name": name,
            "Diet": diet,
            "Location": location[0],
            "Type": fox_type,
        }
        sorted_foxs.append({key: value for key, value in details.items() if value})

    return sorted_foxs


def print_sorted_fox(sorted_foxs: list[dict]) -> None:
    """
    :param sorted_foxs:
    :type sorted_foxs:
    :return:
    :rtype:
    """
    for fox in sorted_foxs:
        for key, value in fox.items():
            print(f"{key} : {value}")
        print("\n")


def main() -> None:
    json_file = "animals_data.json"
    fox_dict = load_data(json_file)
    ans_task1 = step_1(fox_dict)
    print_sorted_fox(ans_task1)


if __name__ == "__main__":
    main()
