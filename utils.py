from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError


def data_processing(selection_data: dict):
    current_year = 2024
    first_cup = selection_data["first_cup"]
    first_cup_year = int(first_cup[:4])
    titles = selection_data["titles"]
    max_possible_titles = (current_year - first_cup_year) // 4

    if titles < 0:
        raise NegativeTitlesError("titles cannot be negative")
    elif first_cup_year is None or first_cup_year % 4 != 2 or first_cup_year < 1930:
        raise InvalidYearCupError("there was no world cup this year")
    elif titles > max_possible_titles:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")

    return selection_data
