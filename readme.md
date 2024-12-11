Step 1 - Print Data From File
Now that we are finished with the Git prep we can get started with the actual assessment. Our end goal is generating HTML, but this step is not related to HTML yet. We’re just going to print the data that we have in the JSON file.
Data Description
In the file animals_data.json (look at the file tree), you have a data structure that describes types of foxes. Observe the data, you can assist an online JSON parser if you need it.
Reading the data
To read the data from the file, import the json library at the top of your Python code:
import json
And then define the function:
def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)

Now when you want to read the content of the file in your code, call the function:
animals_data = load_data('animals_data.json')
Try to read the content of the file with Python and printing it. You should get a list which has nested structures inside of it.
Task
Write a simple Python script that reads the content of animals_data.json, iterates through the animals, and for each one prints:
Name
Diet
The first location from the locations list
Type
If one of these fields doesn’t exist, don’t print it.


Example output
`Name: American Foxhound
Diet: Omnivore
Location: North-America
Type: Hound

Name: Arctic Fox
Diet: Carnivore
Location: Eurasia
Type: Mammal

Name: Cross Fox
Diet: Carnivore
Location: North-America
Type: mammal`

...
The English Foxhound doesn’t have a type field, and therefore we will not print this field:
...

Name: English Foxhound
Diet: Omnivore
Location: Europe

...
