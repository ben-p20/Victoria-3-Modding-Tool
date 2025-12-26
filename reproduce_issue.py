
import os
import sys
import importlib.util
import shutil

# Setup test environment
mod_path = os.path.abspath("test_mod")
os.makedirs(os.path.join(mod_path, "common/character_templates"), exist_ok=True)
os.makedirs(os.path.join(mod_path, "common/history/countries"), exist_ok=True)

# Create the template file
template_content = """
FRA_louis_philippe = { first_name = Louis-Philippe last_name = d_Orleans historical = yes culture = primary_culture ruler = yes birth_date = 1773.10.6 dna = dna_king_louis_philippe_01 interest_group = ig_industrialists ideology = ideology_orleanist traits = { basic_political_operator tactful } on_created = { set_variable = { name = is_married } set_variable = house_orleans } trait_generation = { # nothing! } }
"""
with open(os.path.join(mod_path, "common/character_templates/country_fra.txt"), "w") as f:
    f.write(template_content)

# Import the logic class
spec = importlib.util.spec_from_file_location("ModdingTool", "ModdingTool.py")
module = importlib.util.module_from_spec(spec)
sys.modules["ModdingTool"] = module
spec.loader.exec_module(module)
Vic3Logic = module.Vic3Logic

# Mock logger
def log_callback(msg, level='info'):
    print(f"[{level.upper()}] {msg}")

# Run the test
logic = Vic3Logic(log_callback)
logic.set_mod_path(mod_path)

print("Loading country history details for 'fra'...")
info = logic.load_country_history_details("fra")

print("Result:")
print(info["ruler"])

if info["ruler"]["first"] == "Louis-Philippe":
    print("SUCCESS: Ruler found.")
else:
    print("FAILURE: Ruler not found.")
