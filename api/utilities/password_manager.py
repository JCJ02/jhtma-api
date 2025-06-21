from passlib.context import CryptContext

# Initialize the password context to use bcrypt
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password (str): The plain text password to hash.

        Returns:
            str: The hashed password.
        """
        if not password or not isinstance(password, str):
            raise ValueError("Password Must Be A Non-Empty String.")

        return password_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password) -> bool:
        """
        Verify if the plain password matches the hashed password.

        Args:
            plain_password (str): The plain text password.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        if not plain_password or not hashed_password:
            raise ValueError("Plain and Hashed Password must not Empty!")
        
        return password_context.verify(plain_password, hashed_password)