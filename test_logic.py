
import os
import shutil
import unittest
from unittest.mock import MagicMock, patch
import importlib

# Always force copy to ensure fresh code
shutil.copy("Modding Tool", "ModdingTool.py")

import ModdingTool
# Force reload
importlib.reload(ModdingTool)

class TestVic3Logic(unittest.TestCase):
    def setUp(self):
        self.mock_log = MagicMock()
        self.logic = ModdingTool.Vic3Logic(self.mock_log)
        self.test_dir = "test_env"
        self.logic.set_mod_path(self.test_dir)

        # Setup dummy file structure
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_journal_entry(self):
        entry_data = {
            "id": "je_test",
            "title": "Test Entry",
            "desc": "This is a test.",
            "activation": ["c:SWE = THIS", "is_at_war = yes"],
            "completion": ["army_size >= 10"],
            "rewards": ["add_prestige = 100"]
        }
        self.logic.save_journal_entry(entry_data)

        script_path = os.path.join(self.test_dir, "common/journal_entries/test_env_journals.txt")
        with open(script_path, "r") as f:
            content = f.read()
            # Verify the new group and safety flag are added
            self.assertIn("group = je_group_objectives", content)
            self.assertIn("can_revolution_inherit = yes", content)

            # Verify original content
            self.assertIn("c:SWE = THIS", content)
            self.assertIn("army_size >= 10", content)

if __name__ == "__main__":
    unittest.main()
