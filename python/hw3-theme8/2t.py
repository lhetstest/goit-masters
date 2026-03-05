import re
from typing import Generator, Callable


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Generator that yields all real numbers found in the input text.
    Numbers are assumed to be correctly formatted and separated by spaces.

    Args:
        text (str): Input text containing real numbers separated by spaces.

    Yields:
        float: Each real number found in the text.
    """
    # Pattern to match real numbers separated by spaces
    pattern = r'(?<=\s)[+-]?\d+(?:\.\d+)?(?=\s)'
    for match in re.finditer(pattern, text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Calculates the sum of all real numbers in the text using the provided generator function.

    Args:
        text (str): Input text containing real numbers.
        func (Callable): Generator function that yields real numbers from the text.

    Returns:
        float: Sum of all real numbers found in the text.
    """
    return sum(func(text))


if __name__ == "__main__":
    sample_text = (
        "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    )
    total_profit = sum_profit(sample_text, generator_numbers)
    print(f"Total profit: {total_profit}")
