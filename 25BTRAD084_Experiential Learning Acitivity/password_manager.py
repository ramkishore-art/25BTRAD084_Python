"""
Password Storage System - Core Logic
Uses Python's pickle module for object serialization and storage,
with PBKDF2 hashing for master password verification and symmetric
encryption for stored credentials.
"""

import os
import pickle
import hashlib
import base64
import secrets
import string
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Check if cryptography library is available for AES encryption (Fernet)
try:
    from cryptography.fernet import Fernet
    FERNET_AVAILABLE = True
except ImportError:
    FERNET_AVAILABLE = False


DEFAULT_RECOVERY_QUESTIONS = [
    "What is your mother's maiden name?",
    "What is the name of your first pet or dog?",
    "What was the name of your favorite school teacher?"
]


def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Derives a 32-byte key from the master password and salt
    using PBKDF2-HMAC-SHA256 (100,000 iterations).
    """
    kdf = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=master_password.encode('utf-8'),
        salt=salt,
        iterations=100_000,
        dklen=32
    )
    return kdf


def xor_crypt(data: bytes, key: bytes) -> bytes:
    """
    A pure standard-library fallback stream cipher using SHA-256 keystream expansion.
    Used when the external 'cryptography' package is not installed.
    """
    keystream = b""
    counter = 0
    while len(keystream) < len(data):
        block = hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
        keystream += block
        counter += 1
    return bytes(b ^ k for b, k in zip(data, keystream[:len(data)]))


class EncryptionService:
    """Handles encrypting and decrypting individual password values."""

    def __init__(self, master_password: Optional[str] = None, salt: Optional[bytes] = None,
                 raw_key: Optional[bytes] = None):
        if raw_key is not None:
            self.raw_key = raw_key
        elif master_password is not None and salt is not None:
            self.raw_key = derive_key(master_password, salt)
        else:
            raise ValueError("Must provide either raw_key or (master_password, salt).")

        if FERNET_AVAILABLE:
            fernet_key = base64.urlsafe_b64encode(self.raw_key)
            self.fernet = Fernet(fernet_key)
        else:
            self.fernet = None

    def encrypt(self, plaintext: str) -> str:
        """Encrypts a plaintext string and returns a base64-encoded ciphertext."""
        data_bytes = plaintext.encode('utf-8')
        if self.fernet:
            token = self.fernet.encrypt(data_bytes)
            return token.decode('utf-8')
        else:
            cipher_bytes = xor_crypt(data_bytes, self.raw_key)
            return base64.b64encode(cipher_bytes).decode('utf-8')

    def decrypt(self, ciphertext: str) -> str:
        """Decrypts a base64-encoded ciphertext and returns plaintext string."""
        if self.fernet:
            token = ciphertext.encode('utf-8')
            decrypted_bytes = self.fernet.decrypt(token)
            return decrypted_bytes.decode('utf-8')
        else:
            cipher_bytes = base64.b64decode(ciphertext.encode('utf-8'))
            decrypted_bytes = xor_crypt(cipher_bytes, self.raw_key)
            return decrypted_bytes.decode('utf-8')


class PasswordVault:
    """
    Manages loading, storing, and manipulating accounts stored
    inside a pickled vault file (.pkl / .dat).
    """

    DEFAULT_FILENAME = "vault.pkl"

    def __init__(self, file_path: Optional[str] = None):
        if file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.file_path = os.path.join(base_dir, self.DEFAULT_FILENAME)
        else:
            self.file_path = file_path

        self._crypto: Optional[EncryptionService] = None
        self._is_unlocked: bool = False
        self.data: Dict[str, Any] = {
            "salt": None,
            "master_hash": None,
            "created_at": None,
            "accounts": {},
            "recovery": None
        }

    @property
    def is_unlocked(self) -> bool:
        """Returns True if the vault is currently unlocked."""
        return self._is_unlocked

    def vault_exists(self) -> bool:
        """Checks whether the vault file exists on disk."""
        return os.path.isfile(self.file_path)

    def has_recovery(self) -> bool:
        """Returns True if security recovery questions have been configured."""
        recovery = self.data.get("recovery")
        return bool(recovery and recovery.get("recovery_hash") and recovery.get("wrapped_key"))

    def get_recovery_questions(self) -> List[str]:
        """Returns the configured or default security questions."""
        recovery = self.data.get("recovery")
        if recovery and recovery.get("questions"):
            return list(recovery["questions"])
        return list(DEFAULT_RECOVERY_QUESTIONS)

    def initialize_vault(self, master_password: str, recovery_answers: Optional[List[str]] = None,
                         recovery_questions: Optional[List[str]] = None) -> None:
        """
        Creates a new vault with a master password and optional recovery questions.
        Uses os.urandom for salt and PBKDF2 for password hash.
        """
        if not master_password:
            raise ValueError("Master password cannot be empty.")

        salt = os.urandom(16)
        raw_key = derive_key(master_password, salt)
        master_hash = hashlib.sha256(raw_key + salt).hexdigest()

        self.data = {
            "salt": salt,
            "master_hash": master_hash,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accounts": {},
            "recovery": None
        }

        self._crypto = EncryptionService(master_password=master_password, salt=salt)
        self._is_unlocked = True

        if recovery_answers:
            self.setup_recovery(recovery_answers, recovery_questions)
        else:
            self.save()

    def setup_recovery(self, answers: List[str], questions: Optional[List[str]] = None) -> None:
        """
        Sets up or updates the security recovery questions for master password reset.
        Wraps the current active master encryption key with a key derived from recovery answers.
        """
        self._require_unlocked()

        if len(answers) != 3 or any(not a.strip() for a in answers):
            raise ValueError("You must provide non-empty answers to all 3 security questions.")

        if questions is None or len(questions) != 3:
            questions = list(DEFAULT_RECOVERY_QUESTIONS)

        norm_answers = [a.strip().lower() for a in answers]
        combined_payload = "\x00".join(norm_answers)

        recovery_salt = os.urandom(16)
        recovery_key = derive_key(combined_payload, recovery_salt)
        recovery_hash = hashlib.sha256(recovery_key + recovery_salt).hexdigest()

        # Wrap (encrypt) the current raw master key using the recovery key
        recovery_crypto = EncryptionService(raw_key=recovery_key)
        raw_key_b64 = base64.b64encode(self._crypto.raw_key).decode('utf-8')
        wrapped_key = recovery_crypto.encrypt(raw_key_b64)

        self.data["recovery"] = {
            "questions": questions,
            "recovery_salt": recovery_salt,
            "recovery_hash": recovery_hash,
            "wrapped_key": wrapped_key,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save()

    def verify_recovery_answers(self, answers: List[str]) -> Tuple[bool, Optional[bytes]]:
        """
        Verifies security question answers without unlocking.
        Returns (True, recovery_key) if answers are correct, (False, None) otherwise.
        """
        if not self.vault_exists():
            raise FileNotFoundError(f"Vault file '{self.file_path}' does not exist.")

        self.load()
        if not self.has_recovery():
            return False, None

        if len(answers) != 3:
            return False, None

        norm_answers = [a.strip().lower() for a in answers]
        combined_payload = "\x00".join(norm_answers)

        recovery = self.data["recovery"]
        recovery_salt = recovery["recovery_salt"]
        expected_hash = recovery["recovery_hash"]

        test_recovery_key = derive_key(combined_payload, recovery_salt)
        actual_hash = hashlib.sha256(test_recovery_key + recovery_salt).hexdigest()

        if secrets.compare_digest(actual_hash, expected_hash):
            return True, test_recovery_key
        return False, None

    def recover_and_reset_password(self, answers: List[str], new_master_password: str) -> bool:
        """
        Recovers the vault using security questions, unwraps the encryption key,
        re-encrypts all stored credentials under the new master password, and re-wraps
        the new key. Returns True if successful, False otherwise.
        """
        if not new_master_password:
            raise ValueError("New master password cannot be empty.")

        valid, recovery_key = self.verify_recovery_answers(answers)
        if not valid or recovery_key is None:
            return False

        recovery = self.data["recovery"]
        recovery_crypto = EncryptionService(raw_key=recovery_key)

        # 1. Unwrap the previous raw encryption key using recovery key
        try:
            old_raw_key_b64 = recovery_crypto.decrypt(recovery["wrapped_key"])
            old_raw_key = base64.b64decode(old_raw_key_b64.encode('utf-8'))
            old_crypto = EncryptionService(raw_key=old_raw_key)
        except Exception as e:
            raise ValueError(f"Failed to unwrap encryption key: {e}")

        # 2. Decrypt all stored credentials in memory using the unwrapped key
        decrypted_accounts = {}
        for service_key, acc in self.data.get("accounts", {}).items():
            try:
                decrypted_accounts[service_key] = old_crypto.decrypt(acc["password"])
            except Exception:
                decrypted_accounts[service_key] = None

        # 3. Derive new master key and salt from new master password
        new_salt = os.urandom(16)
        new_raw_key = derive_key(new_master_password, new_salt)
        new_master_hash = hashlib.sha256(new_raw_key + new_salt).hexdigest()

        self.data["salt"] = new_salt
        self.data["master_hash"] = new_master_hash

        new_crypto = EncryptionService(raw_key=new_raw_key)

        # 4. Re-encrypt all stored credentials with new master key
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for service_key, plaintext_pwd in decrypted_accounts.items():
            if plaintext_pwd is not None:
                self.data["accounts"][service_key]["password"] = new_crypto.encrypt(plaintext_pwd)
                self.data["accounts"][service_key]["updated_at"] = now_str

        # 5. Re-wrap the new master key with the existing recovery key
        new_raw_key_b64 = base64.b64encode(new_raw_key).decode('utf-8')
        self.data["recovery"]["wrapped_key"] = recovery_crypto.encrypt(new_raw_key_b64)
        self.data["recovery"]["updated_at"] = now_str

        self._crypto = new_crypto
        self._is_unlocked = True
        self.save()
        return True

    def unlock(self, master_password: str) -> bool:
        """
        Loads vault from pickle file and verifies the master password.
        Returns True if successful, False otherwise.
        """
        if not self.vault_exists():
            raise FileNotFoundError(f"Vault file '{self.file_path}' does not exist.")

        self.load()

        salt = self.data.get("salt")
        expected_hash = self.data.get("master_hash")

        if not salt or not expected_hash:
            raise ValueError("Corrupted vault file: missing salt or master hash.")

        raw_key = derive_key(master_password, salt)
        actual_hash = hashlib.sha256(raw_key + salt).hexdigest()

        if secrets.compare_digest(actual_hash, expected_hash):
            self._crypto = EncryptionService(master_password, salt)
            self._is_unlocked = True
            return True
        else:
            self._crypto = None
            self._is_unlocked = False
            return False

    def lock(self) -> None:
        """Locks the vault and clears sensitive cryptographic material from memory."""
        self._crypto = None
        self._is_unlocked = False

    def save(self) -> None:
        """
        Serializes the internal data structure to disk using pickle.dump().
        """
        parent_dir = os.path.dirname(self.file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(self.file_path, "wb") as f:
            pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self) -> None:
        """
        Deserializes the vault data from disk using pickle.load().
        """
        with open(self.file_path, "rb") as f:
            self.data = pickle.load(f)

    def _require_unlocked(self) -> None:
        if not self._is_unlocked or self._crypto is None:
            raise PermissionError("Vault is locked. Unlock with master password first.")

    def add_account(self, service: str, username: str, password: str, notes: str = "") -> None:
        """Adds a new account entry to the vault."""
        self._require_unlocked()

        service_key = service.strip().lower()
        if not service_key:
            raise ValueError("Service/Website name cannot be empty.")
        if not username.strip():
            raise ValueError("Username cannot be empty.")
        if not password:
            raise ValueError("Password cannot be empty.")

        if service_key in self.data["accounts"]:
            raise KeyError(f"Account for '{service}' already exists. Use update instead.")

        encrypted_pwd = self._crypto.encrypt(password)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.data["accounts"][service_key] = {
            "display_name": service.strip(),
            "username": username.strip(),
            "password": encrypted_pwd,
            "notes": notes.strip(),
            "created_at": now_str,
            "updated_at": now_str
        }
        self.save()

    def get_account(self, service: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves an account by service name, decrypting the password.
        Returns a dictionary or None if not found.
        """
        self._require_unlocked()

        service_key = service.strip().lower()
        account = self.data["accounts"].get(service_key)
        if not account:
            return None

        decrypted_pwd = self._crypto.decrypt(account["password"])
        return {
            "service": account["display_name"],
            "username": account["username"],
            "password": decrypted_pwd,
            "notes": account.get("notes", ""),
            "created_at": account.get("created_at", ""),
            "updated_at": account.get("updated_at", "")
        }

    def update_account(self, service: str, new_username: Optional[str] = None,
                       new_password: Optional[str] = None, new_notes: Optional[str] = None) -> bool:
        """Updates an existing account entry."""
        self._require_unlocked()

        service_key = service.strip().lower()
        account = self.data["accounts"].get(service_key)
        if not account:
            return False

        if new_username is not None and new_username.strip():
            account["username"] = new_username.strip()

        if new_password is not None and new_password:
            account["password"] = self._crypto.encrypt(new_password)

        if new_notes is not None:
            account["notes"] = new_notes.strip()

        account["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()
        return True

    def delete_account(self, service: str) -> bool:
        """Deletes an account entry from the vault."""
        self._require_unlocked()

        service_key = service.strip().lower()
        if service_key in self.data["accounts"]:
            del self.data["accounts"][service_key]
            self.save()
            return True
        return False

    def list_accounts(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all accounts with metadata (passwords kept masked for safety).
        """
        self._require_unlocked()
        result = []
        for key, acc in sorted(self.data["accounts"].items(), key=lambda x: x[1]["display_name"].lower()):
            result.append({
                "service": acc["display_name"],
                "username": acc["username"],
                "created_at": acc.get("created_at", ""),
                "updated_at": acc.get("updated_at", ""),
                "has_notes": bool(acc.get("notes"))
            })
        return result

    def search_accounts(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches accounts where query matches service name or username.
        Returns matching accounts with decrypted passwords.
        """
        self._require_unlocked()
        query = query.strip().lower()
        results = []

        for key, acc in self.data["accounts"].items():
            display_name = acc["display_name"].lower()
            username = acc["username"].lower()
            if query in display_name or query in username:
                decrypted_pwd = self._crypto.decrypt(acc["password"])
                results.append({
                    "service": acc["display_name"],
                    "username": acc["username"],
                    "password": decrypted_pwd,
                    "notes": acc.get("notes", ""),
                    "updated_at": acc.get("updated_at", "")
                })
        return results

    def get_summary(self) -> Dict[str, Any]:
        """Returns non-sensitive metadata about the vault."""
        return {
            "vault_file": self.file_path,
            "total_accounts": len(self.data.get("accounts", {})),
            "created_at": self.data.get("created_at", "Unknown"),
            "encryption_backend": "Fernet (AES-128)" if FERNET_AVAILABLE else "SHA-256 Keystream Stream Cipher",
            "file_size_bytes": os.path.getsize(self.file_path) if self.vault_exists() else 0,
            "recovery_enabled": self.has_recovery()
        }


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True
) -> str:
    """
    Generates a cryptographically secure random password using secrets module.
    Ensures at least one character from each selected character set is present.
    """
    if length < 6:
        length = 6

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_upper else ""
    digits = string.digits if use_digits else ""
    symbols = "!@#$%^&*()-_=+[]{}<>?" if use_symbols else ""

    alphabet = lower + upper + digits + symbols
    if not alphabet:
        alphabet = lower

    required_chars = [secrets.choice(lower)]
    if use_upper:
        required_chars.append(secrets.choice(upper))
    if use_digits:
        required_chars.append(secrets.choice(digits))
    if use_symbols:
        required_chars.append(secrets.choice(symbols))

    remaining_length = length - len(required_chars)
    random_pool = [secrets.choice(alphabet) for _ in range(remaining_length)]

    combined = required_chars + random_pool
    for i in range(len(combined) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        combined[i], combined[j] = combined[j], combined[i]

    return "".join(combined)
