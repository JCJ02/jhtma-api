import random, string
from passlib.context import CryptContext

# INITIALIZE THE PASSWORD CONTEXT TO USE "BCRYPT"
random_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generateRandomText(length = 16):
    """
    GENERATES A RANDOM STRING WITH AT LEAST 1 NUMBER AND 1 SPECIAL CHARACTER.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    result = []

    # ENSURE AT LEAST ONE NUMBER AND ONE SPECIAL CHARACTER
    result.append(random.choice(string.digits))
    result.append(random.choice(string.punctuation))

    # FILL THE REMAINING CHARACTERS
    remaining_length = length - 2
    if remaining_length > 0:
        result.extend(random.choice(characters) for _ in range(remaining_length))

    # SHUFFLE THE RESULT TO MIX THE CHARACTERS
    random.shuffle(result)
    shuffled = ''.join(result)
    return random_context.hash(shuffled)

print("Generated Random Text: " + generateRandomText())