#!/usr/bin/env python3
"""
Interactive Command Line Interface for Password Storage System.
Built with Python and pickle.
"""

import sys
import os
import getpass
from password_manager import PasswordVault, generate_password


def prompt_password(prompt_text: str = "Password: ") -> str:
    """
    Prompts for a password without echoing characters to screen.
    Falls back to input() if getpass is not supported by terminal.
    """
    try:
        pwd = getpass.getpass(prompt_text)
    except Exception:
        pwd = input(prompt_text)
    return pwd


def print_banner():
    print("=" * 60)
    print("        PYTHON SECURE PASSWORD VAULT (PICKLE)        ")
    print("=" * 60)


def print_menu():
    print("\n" + "-" * 40)
    print(" [1] Add New Account")
    print(" [2] Search / Retrieve Account")
    print(" [3] List All Accounts")
    print(" [4] Update Account Password/Username")
    print(" [5] Delete an Account")
    print(" [6] Generate Strong Password")
    print(" [7] Setup / Change Security Recovery Questions")
    print(" [8] Vault Summary & Info")
    print(" [9] Lock & Exit")
    print("-" * 40)


def handle_add_account(vault: PasswordVault):
    print("\n--- Add New Account ---")
    service = input("Service / Website name (e.g., Google, GitHub): ").strip()
    if not service:
        print("[Error] Service name cannot be empty.")
        return

    username = input("Username or Email: ").strip()
    if not username:
        print("[Error] Username cannot be empty.")
        return

    gen_choice = input("Generate a strong random password? (y/n, default: n): ").strip().lower()
    if gen_choice == 'y':
        try:
            length_input = input("Password length (default 16): ").strip()
            length = int(length_input) if length_input else 16
        except ValueError:
            length = 16
        password = generate_password(length=length)
        print(f"Generated Password: {password}")
    else:
        password = prompt_password("Enter password: ").strip()
        if not password:
            print("[Error] Password cannot be empty.")
            return

    notes = input("Notes (optional): ").strip()

    try:
        vault.add_account(service=service, username=username, password=password, notes=notes)
        print(f"[Success] Account for '{service}' has been saved to the vault.")
    except KeyError as e:
        print(f"[Warning] {e}")
    except Exception as e:
        print(f"[Error] Error saving account: {e}")


def handle_search_account(vault: PasswordVault):
    print("\n--- Search / Retrieve Account ---")
    query = input("Enter search term (service or username): ").strip()
    if not query:
        print("[Error] Search query cannot be empty.")
        return

    results = vault.search_accounts(query)
    if not results:
        print(f"No accounts found matching '{query}'.")
        return

    print(f"\nFound {len(results)} matching account(s):")
    print("=" * 60)
    for idx, acc in enumerate(results, start=1):
        print(f"[{idx}] Service:   {acc['service']}")
        print(f"    Username:  {acc['username']}")
        print(f"    Password:  {acc['password']}")
        if acc.get("notes"):
            print(f"    Notes:     {acc['notes']}")
        if acc.get("updated_at"):
            print(f"    Updated:   {acc['updated_at']}")
        print("-" * 60)


def handle_list_accounts(vault: PasswordVault):
    print("\n--- Stored Accounts ---")
    accounts = vault.list_accounts()
    if not accounts:
        print("Your vault is empty. Use Option 1 to add accounts.")
        return

    header = f"{'#':<4} {'Service':<22} {'Username':<26} {'Updated':<19}"
    print(header)
    print("-" * len(header))
    for idx, acc in enumerate(accounts, start=1):
        print(f"{idx:<4} {acc['service'][:20]:<22} {acc['username'][:24]:<26} {acc.get('updated_at', '')[:19]:<19}")
    print(f"\nTotal: {len(accounts)} account(s)")
    print("Tip: To view passwords, use Option 2 (Search / Retrieve).")


def handle_update_account(vault: PasswordVault):
    print("\n--- Update Account ---")
    service = input("Enter service name to update: ").strip()
    if not service:
        print("[Error] Service name cannot be empty.")
        return

    existing = vault.get_account(service)
    if not existing:
        print(f"[Error] Account '{service}' not found.")
        return

    print(f"Current Username: {existing['username']}")
    new_username = input("New Username (leave blank to keep current): ").strip()

    print("\nUpdate password?")
    pwd_choice = input("(1) Keep current, (2) Enter new password, (3) Generate new: ").strip()
    new_password = None

    if pwd_choice == "2":
        new_password = prompt_password("Enter new password: ").strip()
    elif pwd_choice == "3":
        new_password = generate_password(length=16)
        print(f"Generated New Password: {new_password}")

    new_notes = input("New Notes (leave blank to keep current): ").strip()

    updated = vault.update_account(
        service=service,
        new_username=new_username if new_username else None,
        new_password=new_password if new_password else None,
        new_notes=new_notes if new_notes else None
    )

    if updated:
        print(f"[Success] Account for '{service}' updated successfully.")
    else:
        print("[Error] Update failed.")


def handle_delete_account(vault: PasswordVault):
    print("\n--- Delete Account ---")
    service = input("Enter service name to delete: ").strip()
    if not service:
        print("[Error] Service name cannot be empty.")
        return

    existing = vault.get_account(service)
    if not existing:
        print(f"[Error] Account '{service}' not found.")
        return

    confirm = input(f"Are you sure you want to permanently delete '{service}'? (y/N): ").strip().lower()
    if confirm == 'y':
        if vault.delete_account(service):
            print(f"[Success] Account for '{service}' deleted.")
        else:
            print("[Error] Failed to delete account.")
    else:
        print("Action cancelled.")


def handle_generate_password():
    print("\n--- Password Generator ---")
    try:
        len_input = input("Password length (default 16): ").strip()
        length = int(len_input) if len_input else 16
    except ValueError:
        length = 16

    use_upper = input("Include UPPERCASE letters? (Y/n): ").strip().lower() != 'n'
    use_digits = input("Include numbers (0-9)? (Y/n): ").strip().lower() != 'n'
    use_symbols = input("Include special symbols (!@#$...)? (Y/n): ").strip().lower() != 'n'

    pwd = generate_password(length, use_upper, use_digits, use_symbols)
    print("\n" + "=" * 50)
    print(f"Generated Password: {pwd}")
    print("=" * 50)


def handle_vault_summary(vault: PasswordVault):
    print("\n--- Vault Summary ---")
    summary = vault.get_summary()
    print(f"Vault File:         {summary['vault_file']}")
    print(f"Total Accounts:     {summary['total_accounts']}")
    print(f"Vault Created At:   {summary['created_at']}")
    print(f"Encryption Backend: {summary['encryption_backend']}")
    print(f"File Size:          {summary['file_size_bytes']} bytes")
    rec_status = "Configured (Active)" if summary.get("recovery_enabled") else "Not Set (Recommended)"
    print(f"Recovery Questions: {rec_status}")


def handle_setup_recovery(vault: PasswordVault):
    print("\n--- Setup / Change Security Recovery Questions ---")
    print("These questions allow you to recover your vault and reset your master password")
    print("if you ever forget it, WITHOUT losing any of your saved credentials.\n")

    questions = vault.get_recovery_questions()
    answers = []
    for i, q in enumerate(questions, start=1):
        print(f"Question {i}: {q}")
        ans = input(f"Your Answer {i}: ").strip()
        if not ans:
            print("[Error] Answers cannot be blank. Setup cancelled.")
            return
        answers.append(ans)

    try:
        vault.setup_recovery(answers, questions)
        print("\n[Success] Security recovery questions configured and encrypted successfully.")
    except Exception as e:
        print(f"[Error] Failed to configure recovery questions: {e}")


def handle_vault_recovery(vault: PasswordVault) -> bool:
    print("\n" + "=" * 60)
    print("                VAULT PASSWORD RECOVERY                 ")
    print("=" * 60)

    if not vault.has_recovery():
        print("[Error] No security recovery questions were configured for this vault.")
        print("Master password recovery is not possible without recovery questions set up.")
        return False

    print("Please answer your 3 security questions to verify your identity:\n")
    questions = vault.get_recovery_questions()
    answers = []
    for i, q in enumerate(questions, start=1):
        print(f"Question {i}: {q}")
        ans = input(f"Your Answer {i}: ").strip()
        answers.append(ans)

    valid, _ = vault.verify_recovery_answers(answers)
    if not valid:
        print("\n[Error] Verification failed. Answers do not match our encrypted records.")
        return False

    print("\n[Verified] Identity confirmed successfully!")
    print("You can now set a new Master Password for your vault.\n")

    while True:
        new_pwd1 = prompt_password("Set New Master Password: ")
        if not new_pwd1:
            print("[Error] Master password cannot be empty. Try again.")
            continue

        new_pwd2 = prompt_password("Confirm New Master Password: ")
        if new_pwd1 != new_pwd2:
            print("[Error] Passwords do not match. Try again.\n")
            continue

        try:
            if vault.recover_and_reset_password(answers, new_pwd1):
                print("\n[Success] Master password has been reset successfully!")
                print("[Success] All stored credentials have been re-encrypted with your new key.")
                print("[Success] Vault unlocked. Welcome back.\n")
                return True
            else:
                print("[Error] Recovery process failed.")
                return False
        except Exception as e:
            print(f"[Error] Recovery error: {e}")
            return False


def unlock_or_setup_vault(vault: PasswordVault) -> bool:
    """Handles first-time initialization or unlocking with master password."""
    if not vault.vault_exists():
        print("\nNo existing password vault found.")
        print("Let's create your vault and set a Master Password.")
        print("[IMPORTANT] Do not forget this master password! It is required to decrypt your vault.\n")

        while True:
            pwd1 = prompt_password("Set Master Password: ")
            if not pwd1:
                print("[Error] Master password cannot be empty. Try again.")
                continue

            pwd2 = prompt_password("Confirm Master Password: ")
            if pwd1 != pwd2:
                print("[Error] Passwords do not match. Try again.\n")
                continue

            try:
                vault.initialize_vault(pwd1)
                print("\n[Success] Vault created and encrypted successfully.")

                setup_rec = input("\nWould you like to set up Security Recovery Questions now? (Y/n): ").strip().lower()
                if setup_rec != 'n':
                    handle_setup_recovery(vault)

                return True
            except Exception as e:
                print(f"[Error] Failed to create vault: {e}")
                return False
    else:
        print("\nExisting vault found.")
        if vault.has_recovery():
            print("Tip: If you forgot your password, enter 'r' or 'recover' to reset via security questions.")

        attempts = 3
        while attempts > 0:
            master_pwd = prompt_password("Enter Master Password: ")

            # Check if user requested recovery mode
            if master_pwd.strip().lower() in ('r', 'recover'):
                return handle_vault_recovery(vault)

            try:
                if vault.unlock(master_pwd):
                    print("[Success] Vault unlocked successfully. Welcome back.\n")
                    return True
                else:
                    attempts -= 1
                    if attempts > 0:
                        print(f"[Error] Incorrect master password. {attempts} attempt(s) remaining.")
                    else:
                        print("[Error] Maximum failed attempts reached.")
                        if vault.has_recovery():
                            choice = input("Would you like to recover using security questions? (y/N): ").strip().lower()
                            if choice == 'y':
                                return handle_vault_recovery(vault)
                        return False
            except Exception as e:
                print(f"[Error] Error unlocking vault: {e}")
                return False
        return False


def main():
    print_banner()

    vault = PasswordVault()

    try:
        if not unlock_or_setup_vault(vault):
            sys.exit(1)

        while True:
            print_menu()
            choice = input("Select an option (1-9): ").strip()

            if choice == "1":
                handle_add_account(vault)
            elif choice == "2":
                handle_search_account(vault)
            elif choice == "3":
                handle_list_accounts(vault)
            elif choice == "4":
                handle_update_account(vault)
            elif choice == "5":
                handle_delete_account(vault)
            elif choice == "6":
                handle_generate_password()
            elif choice == "7":
                handle_setup_recovery(vault)
            elif choice == "8":
                handle_vault_summary(vault)
            elif choice == "9":
                vault.lock()
                print("\nVault safely locked. Goodbye.")
                break
            else:
                print("[Warning] Invalid option. Please enter a number from 1 to 9.")

    except KeyboardInterrupt:
        vault.lock()
        print("\n\nInterrupted. Vault locked. Goodbye.")
        sys.exit(0)


if __name__ == "__main__":
    main()
