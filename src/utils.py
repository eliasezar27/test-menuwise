import re

__all__ = [
    'extract_numeric_value',
    'remove_numeric_values',
    'itemize_instructions'
    ]

def extract_numeric_value(input_string) -> str:
    # Mapping of common fractional characters to their numeric values
    fraction_map = {
        '½': 0.5, '⅓': 1/3, '⅔': 2/3, '¼': 0.25, '¾': 0.75,
        '⅕': 0.2, '⅖': 0.4, '⅗': 0.6, '⅘': 0.8, '⅙': 1/6, '⅚': 5/6,
        '⅛': 0.125, '⅜': 0.375, '⅝': 0.625, '⅞': 0.875
    }

    # Total numeric value accumulated
    total_value = 0

    # Find all numbers and fractions in the input string
    parts = re.findall(r'\d+\s*[⅐-⅞½-¾]|\d+', input_string)
    for part in parts:
        # Check for fractional part
        if any(frac in part for frac in fraction_map):
            for frac, value in fraction_map.items():
                if frac in part:
                    # Add the fraction value and any whole number part
                    whole_number = re.findall(r'\d+', part)
                    total_value += value
                    if whole_number:
                        total_value += float(whole_number[0])
        else:
            # Add whole numbers directly
            total_value += int(part)

    return total_value


def remove_numeric_values(text) -> str:
    # Regular expression to match digits, Unicode fractions, and decimal points
    pattern = r'[\d⅓¼½¾⅛⅜⅝⅞.]+'
    # Replace found patterns with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text.strip()


def itemize_instructions(instructions) -> str:
    # Split the instructions by '\n ' to separate items into list items
    steps = instructions.split('\n')
    steps = [i for i in steps if i != '']
    # Initialize an empty list to store formatted steps
    formatted_steps = []
    # Loop through the steps and enumerate them, starting at 1
    for index, step in enumerate(steps, 1):
        # Add the step number and the step text to the formatted list
        # Ensure we add a period back if it's not the last element
        if index < len(steps):
            formatted_steps.append(f"{index}. {step}")
        else:
            formatted_steps.append(f"{index}. {step}")
    # Join all the formatted steps with a newline character for clear separation
    return '\n'.join(formatted_steps)