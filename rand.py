import random
import string


def generate_random_unique_number(min_length=6, max_length=8):
    """
    Generate a random unique number of length between min_length and max_length.
    
    :param min_length: Minimum length of the generated number.
    :param max_length: Maximum length of the generated number.
    :return: Random unique number as a string.
    """
    length = random.randint(min_length, max_length)  # Choose a random length within the specified range.
    digits = string.digits  # Pool of digits to choose from.

    return ''.join(random.sample(digits, k=length))  # Generate and return the random unique number.


# Example usage
random_number = generate_random_unique_number()
