import logging
import pytest
from animals_web_generator import setup_logging, load_data, step_1, print_sorted_fox
import os


def test_dummy():
    pass


@pytest.fixture(scope="module")
def logger():
    logger = setup_logging()
    yield logger
    logging.shutdown()


def test_logging(caplog, logger):
    folder = "logging"
    file_name = "logs.txt"
    path = os.path.join(folder, file_name)
    with caplog.at_level(logging.INFO):
        setup_logging()
    assert os.path.exists(path), f"File {path} does not exist"
    assert "logging started..." in caplog.text, "logging not started"


def test_load_json(caplog, logger):
    folder = ".."
    json_file = "animals_data.json"
    os.path.join(folder, json_file)
    with caplog.at_level(logging.INFO):
        fox_data = load_data(json_file, logger)
    assert f"{json_file} loaded" in caplog.text
    assert fox_data, "No data in JSON file"


def test_sort_fox_1(caplog, logger):
    test_fox_dict_1 = [
        {
            "name": "Arctic Fox",
            "locations": ["Eurasia"],
            "characteristics": {
                "type": "Furry Fox",
                "diet": "Carnivore",
            },
        },
    ]
    with caplog.at_level(logging.INFO):
        sorted_fox = step_1(test_fox_dict_1, logger)
    for fox in sorted_fox:
        assert fox["Name"] == "Arctic Fox"
        assert fox["Location"] == "Eurasia"
        assert fox["Type"] == "Furry Fox"
        assert fox["Diet"] == "Carnivore"


def test_sort_fox_2(caplog, logger):
    test_fox_dict_2 = [
        {"name": "Missing Data Fox", "locations": [], "characteristics": {}},
    ]
    with caplog.at_level(logging.INFO):
        sorted_fox = step_1(test_fox_dict_2, logger)
    for fox in sorted_fox:
        assert fox["Name"] == "Missing Data Fox"
        assert "Location" not in fox
        assert "Type" not in fox
        assert "Diet" not in fox


def test_print_sorted_fox(capfd, caplog, logger):
    test_fox_dict = [
        {
            "Name": "Arctic Fox",
            "Diet": "Carnivore",
            "Location": "Eurasia",
            "Type": "Furry Fox",
        },
        {"Name": "Missing Data Fox"},
    ]

    with caplog.at_level(logging.INFO):
        print_sorted_fox(test_fox_dict, logger)

    assert "Starting to print sorted foxs to display" in caplog.text
    assert "sorted_foxs found" in caplog.text
    assert "finished printing sorted_foxes" in caplog.text

    captured = capfd.readouterr()
    expected_output = (
        "Name : Arctic Fox\nDiet : Carnivore\nLocation : Eurasia\nType : Furry Fox\n\n"
        "Name : Missing Data Fox\n\n"
    )

    assert captured.out == expected_output
