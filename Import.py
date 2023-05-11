import sqlite3
import sys
import xml.etree.ElementTree as ET

# Read pokemon XML file name from command-line
if len(sys.argv) < 2:
    print("You must pass at least one XML file name containing Pokemon to insert")
    sys.exit(1)

# Connect to the SQLite database
conn = sqlite3.connect('pokemon.sqlite')
cursor = conn.cursor()

# Iterate over each XML file passed as a command-line argument
for xml_file in sys.argv[1:]:
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Extract Pokemon data from XML
        pokedex = root.attrib.get('pokedex', '')
        classification = root.attrib.get('classification', '')
        generation = root.attrib.get('generation', '')

        name = root.findtext('name', '')
        hp = root.findtext('hp', '')
        types = [elem.text for elem in root.findall('type')]
        attack = root.findtext('attack', '')
        defense = root.findtext('defense', '')
        speed = root.findtext('speed', '')
        sp_attack = root.findtext('sp_attack', '')
        sp_defense = root.findtext('sp_defense', '')
        height = root.findtext('height/m', '')
        weight = root.findtext('weight/kg', '')
        abilities = [elem.text for elem in root.findall('abilities/ability')]

        # Check if the Pokemon already exists in the database
        cursor.execute("SELECT COUNT(*) FROM pokemon WHERE name = ?", (name,))
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"Skipping duplicate Pokemon: {name}")
            continue

        # Insert the Pokemon data into the main table
        cursor.execute("""
            INSERT INTO pokemon (pokedex_number, classification_id, generation, name, hp, attack, defense, speed,
                                 sp_attack, sp_defense, height_m, weight_kg)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cursor.lastrowid, classification, generation, name, hp, attack, defense, speed,
              sp_attack, sp_defense, height, weight))

        # Get the ID of the inserted Pokemon
        pokemon_id = cursor.lastrowid

        # Insert the Pokemon types into the mapping table
        for pokemon_type in types:
            cursor.execute("INSERT INTO type (id, type_name) VALUES (?, ?)", (pokemon_id, pokemon_type))

        # Insert the Pokemon abilities into the abilities table
        for ability in abilities:
            cursor.execute("INSERT INTO pokemon_abilities (pokemon_id, ability_id) VALUES (?, ?)", (pokemon_id, ability))

        print(f"Inserted Pokemon: {name}")
    except Exception as e:
        print(f"Error inserting Pokemon from {xml_file}: {str(e)}")

# Commit the changes and close the database connection
conn.commit()
conn.close()











# import sqlite3

# # Connect to the SQLite database
# conn = sqlite3.connect('pokemon.sqlite')
# cursor = conn.cursor()

# # Delete a row from the pokemon table based on the name
# pokemon_name = "FunnyBunny"
# cursor.execute("DELETE FROM pokemon WHERE name = ?", (pokemon_name,))

# # Commit the changes and close the database connection
# conn.commit()
# conn.close()