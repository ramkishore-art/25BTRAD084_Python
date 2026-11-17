"""
Unit tests for the Password Storage System (password_manager.py).
Tests all CRUD operations, pickle serialization, master password verification,
and password generation.
"""

import os
import unittest
import tempfile
from password_manager import PasswordVault, generate_password, derive_key


class TestPasswordManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault_file = os.path.join(self.temp_dir.name, "test_vault.pkl")
        self.master_pwd = "SuperSecretMasterPassword123!"
        self.vault = PasswordVault(self.vault_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initialize_and_pickle_file_creation(self):
        """Test vault initialization and pickle file creation."""
        self.assertFalse(self.vault.vault_exists())
        self.vault.initialize_vault(self.master_pwd)

        self.assertTrue(self.vault.vault_exists())
        self.assertTrue(self.vault.is_unlocked)
        self.assertGreater(os.path.getsize(self.vault_file), 0)

    def test_unlock_with_correct_and_wrong_password(self):
        """Test unlock with correct vs wrong master password."""
        self.vault.initialize_vault(self.master_pwd)
        self.vault.lock()
        self.assertFalse(self.vault.is_unlocked)

        # Wrong password should fail
        unlocked = self.vault.unlock("WrongPassword!")
        self.assertFalse(unlocked)
        self.assertFalse(self.vault.is_unlocked)

        # Correct password should succeed
        unlocked = self.vault.unlock(self.master_pwd)
        self.assertTrue(unlocked)
        self.assertTrue(self.vault.is_unlocked)

    def test_add_and_get_account(self):
        """Test adding an account and retrieving it with decrypted password."""
        self.vault.initialize_vault(self.master_pwd)

        self.vault.add_account(
            service="GitHub",
            username="dev_naveen",
            password="MySecretGitHubPassword!456",
            notes="Personal account"
        )

        account = self.vault.get_account("GitHub")
        self.assertIsNotNone(account)
        self.assertEqual(account["service"], "GitHub")
        self.assertEqual(account["username"], "dev_naveen")
        self.assertEqual(account["password"], "MySecretGitHubPassword!456")
        self.assertEqual(account["notes"], "Personal account")

    def test_pickle_persistence_across_instances(self):
        """Test that data saved with pickle persists across new class instances."""
        self.vault.initialize_vault(self.master_pwd)
        self.vault.add_account("Google", "user@gmail.com", "P@ssword1")

        # Open in a brand new instance
        vault2 = PasswordVault(self.vault_file)
        self.assertTrue(vault2.vault_exists())
        self.assertTrue(vault2.unlock(self.master_pwd))

        account = vault2.get_account("google")
        self.assertIsNotNone(account)
        self.assertEqual(account["password"], "P@ssword1")

    def test_update_account(self):
        """Test updating username, password, or notes."""
        self.vault.initialize_vault(self.master_pwd)
        self.vault.add_account("Netflix", "old_email@gmail.com", "old_pass123")

        updated = self.vault.update_account(
            service="Netflix",
            new_username="new_email@gmail.com",
            new_password="new_strong_pass!789"
        )
        self.assertTrue(updated)

        account = self.vault.get_account("Netflix")
        self.assertEqual(account["username"], "new_email@gmail.com")
        self.assertEqual(account["password"], "new_strong_pass!789")

    def test_delete_account(self):
        """Test deleting an account."""
        self.vault.initialize_vault(self.master_pwd)
        self.vault.add_account("Spotify", "music_lover", "tune_pass_123")

        self.assertIsNotNone(self.vault.get_account("Spotify"))
        deleted = self.vault.delete_account("Spotify")
        self.assertTrue(deleted)
        self.assertIsNone(self.vault.get_account("Spotify"))

        # Deleting non-existent should return False
        self.assertFalse(self.vault.delete_account("NonExistent"))

    def test_list_and_search_accounts(self):
        """Test listing and searching stored accounts."""
        self.vault.initialize_vault(self.master_pwd)
        self.vault.add_account("Google", "naveen@gmail.com", "pass1")
        self.vault.add_account("GitHub", "naveen_coder", "pass2")
        self.vault.add_account("Twitter", "naveen_tweets", "pass3")

        # List
        accounts = self.vault.list_accounts()
        self.assertEqual(len(accounts), 3)

        # Search by service
        results = self.vault.search_accounts("git")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["service"], "GitHub")
        self.assertEqual(results[0]["password"], "pass2")

        # Search by username substring
        results2 = self.vault.search_accounts("naveen")
        self.assertEqual(len(results2), 3)

    def test_password_generator(self):
        """Test random password generation properties."""
        pwd1 = generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True)
        self.assertEqual(len(pwd1), 12)
        self.assertTrue(any(c.isupper() for c in pwd1))
        self.assertTrue(any(c.islower() for c in pwd1))
        self.assertTrue(any(c.isdigit() for c in pwd1))

        # Check randomness (two passwords should be different)
        pwd2 = generate_password(length=16)
        self.assertNotEqual(pwd1, pwd2)

    def test_setup_recovery_and_successful_password_reset(self):
        """Test configuring recovery questions and recovering vault after forgotten master password."""
        self.vault.initialize_vault(self.master_pwd)
        self.assertFalse(self.vault.has_recovery())

        # Add credentials to vault
        self.vault.add_account("AWS", "naveen_cloud", "MySuperAWSSecret987!", notes="Root console")

        # Configure recovery answers: Mother's name, Pet's name, Favorite teacher
        answers = ["Martha", "Charlie", "Professor Snape"]
        self.vault.setup_recovery(answers)
        self.assertTrue(self.vault.has_recovery())

        # Lock the vault (simulating user forgot master password)
        self.vault.lock()
        self.assertFalse(self.vault.is_unlocked)

        # Recover using security questions and reset master password
        new_master_pwd = "BrandNewMasterPassword2026!#"
        recovered = self.vault.recover_and_reset_password(answers, new_master_pwd)
        self.assertTrue(recovered)
        self.assertTrue(self.vault.is_unlocked)

        # Verify old accounts are intact and decryptable
        account = self.vault.get_account("AWS")
        self.assertIsNotNone(account)
        self.assertEqual(account["password"], "MySuperAWSSecret987!")
        self.assertEqual(account["notes"], "Root console")

        # Lock and unlock with the NEW master password
        self.vault.lock()
        self.assertFalse(self.vault.unlock(self.master_pwd))  # Old password must fail
        self.assertTrue(self.vault.unlock(new_master_pwd))     # New password must succeed

    def test_recovery_with_wrong_answers_fails(self):
        """Test that incorrect security question answers prevent recovery."""
        self.vault.initialize_vault(self.master_pwd)
        answers = ["Martha", "Charlie", "Professor Snape"]
        self.vault.setup_recovery(answers)
        self.vault.lock()

        # Try recovering with wrong answers
        wrong_answers = ["Martha", "WrongPet", "Professor Snape"]
        valid, recovery_key = self.vault.verify_recovery_answers(wrong_answers)
        self.assertFalse(valid)
        self.assertIsNone(recovery_key)

        recovered = self.vault.recover_and_reset_password(wrong_answers, "AnyNewPassword123")
        self.assertFalse(recovered)
        self.assertFalse(self.vault.is_unlocked)

    def test_recovery_case_and_whitespace_insensitivity(self):
        """Test that recovery answers are trimmed and case-insensitive."""
        self.vault.initialize_vault(self.master_pwd)
        self.vault.setup_recovery(["Martha", "Charlie", "Professor Snape"])
        self.vault.lock()

        # Submit answers with mixed casing and spaces
        fuzzy_answers = ["   mArThA  ", "  cHaRlIe ", "PrOfEsSoR SnApE  "]
        recovered = self.vault.recover_and_reset_password(fuzzy_answers, "NewPass123!")
        self.assertTrue(recovered)
        self.assertTrue(self.vault.is_unlocked)


if __name__ == "__main__":
    unittest.main()
