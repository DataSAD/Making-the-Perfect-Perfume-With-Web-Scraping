from collections import Counter

with open('perfect_recipe.txt', 'w') as f:
    pass


def eliminate_notes(file):

    with open(file, 'r') as f:
        notes_raw = f.readlines()

    notes = []
    for note in notes_raw:
        notes.append(note[:-1])

    counts = Counter(notes)
    # print(counts)

    total = len(notes)

    notes_final = {note: (count / total)*100 for note, count in counts.items() if (count / total)*100 > 2}
    return notes_final


def make_the_perfume():
    top = eliminate_notes('top.txt')
    mid = eliminate_notes('mid.txt')
    base = eliminate_notes('base.txt')

    # Let's say %50 alcohol and %50 essence. For a 100ml fragrance, essence is 50ml. We will take the total of the
    # ratios and calculate how much ml it is for a total of 50ml

    ratio_total = 0
    for ratio in top.values():
        ratio_total += ratio

    for ratio in mid.values():
        ratio_total += ratio

    for ratio in base.values():
        ratio_total += ratio

    # calculate a multiplier to multiply with ratios and reach total 50 ml for all the notes combined.
    multiplier_to_find_ml = 50 / ratio_total

    with open('perfect_recipe.txt', 'a') as f:
        f.write('\n\n***TOP NOTES***\n\n')

    for note, ratio in top.items():
        # Convert ratio to ml. Round it.
        ml_value = str(round(ratio * multiplier_to_find_ml, 2)) + 'ml'
        top[note] = ml_value
        with open('perfect_recipe.txt', 'a') as f:
            f.write(f'{note}: {ml_value}\n')

    with open('perfect_recipe.txt', 'a') as f:
        f.write('\n\n***MID NOTES***\n\n')

    for note, ratio in mid.items():
        # Convert ratio to ml. Round it.
        ml_value = str(round(ratio * multiplier_to_find_ml, 2)) + 'ml'
        mid[note] = ml_value
        with open('perfect_recipe.txt', 'a') as f:
            f.write(f'{note}: {ml_value}\n')

    with open('perfect_recipe.txt', 'a') as f:
        f.write('\n\n***BASE NOTES***\n\n')

    for note, ratio in base.items():
        # Convert ratio to ml. Round it.
        ml_value = str(round(ratio * multiplier_to_find_ml, 2)) + 'ml'
        base[note] = ml_value
        with open('perfect_recipe.txt', 'a') as f:
            f.write(f'{note}: {ml_value}\n')


make_the_perfume()