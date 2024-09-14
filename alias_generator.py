import pandas as pd
from ai4bharat.transliteration import XlitEngine
import pandas as pd
import grapheme
from tqdm import tqdm
from inference.engine import Model

e = XlitEngine(beam_width=10, src_script_type="indic")
e1 = XlitEngine("mr" , beam_width=10)
model = Model(r"./indic-en/fairseq_model", model_type="fairseq")

def generate_short_names_4(full_name):
    # Split the name into parts
    parts = full_name.split()

    # Check if title exists
    title = parts[1] if parts[1] in ["श्री.", "श्रीमती", "डॉ.", "प्रोफेसर.", "सर", "श्री.डॉ.", "श्री.प्रा.", "श्री.सर", "प्रा."] else ""

    # Find surname
    surname = parts[0]

    # Initialize first name and middle name
    first_name = ""
    middle_name = ""
    if len(parts) == 4:  # Middle name is provided
        first_name = parts[2]
        middle_name = parts[3]

    # Transliterate first name and middle name
    first_name_translit = e.translit_sentence(first_name, 'mr')
    middle_name_translit = e.translit_sentence(middle_name, 'mr')
    title_translit = e.translit_sentence(title, 'mr')
    surname_name_translit = e.translit_sentence(surname, 'mr')
    title_translation = model.translate_paragraph(title, "mar_Deva", "eng_Latn")
    first_name_translit_1 = e1.translit_sentence(first_name_translit[0], 'mr')
    middle_name_translit_1 = e1.translit_sentence(middle_name_translit[0], 'mr')
    # Generate combinations of short names
    combinations = [
        f"{surname} {title} {first_name} {middle_name}".strip(),
        f"{surname} {first_name} {middle_name}".strip(),
        f"{title} {first_name} {middle_name} {surname}".strip(),
        f"{first_name} {middle_name} {surname}".strip(),
        # as_it_is
        f"{surname} {title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'}".strip(),
        f"{title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {surname}".strip(),
        f"{first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {surname}".strip(),
        f"{surname} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {surname}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {surname}".strip(),
        # english_short
        f"{surname} {title} {first_name} {middle_name_translit_1 + '.'}".strip(),
        f"{surname} {first_name} {middle_name_translit_1 + '.'}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {surname}".strip(),
        f"{title} {first_name} {middle_name_translit_1 + '.'} {surname}".strip(),
        f"{first_name} {middle_name_translit_1 + '.'} {surname}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name} {surname}".strip(),
        # english
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit}".strip(),
        f"{first_name_translit} {middle_name_translit} {surname_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit}".strip(),
        f"{surname_name_translit} {first_name_translit[0] + '.'} {middle_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'}".strip(),
        f"{title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{title_translit} {first_name_translit} {middle_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{title_translit} {first_name_translit[0] + '.'} {middle_name_translit} {surname_name_translit}".strip(),
        f"{first_name_translit} {middle_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{first_name_translit[0] + '.'} {middle_name_translit} {surname_name_translit}".strip(),
        # translation
        f"{surname_name_translit} {title_translation} {first_name_translit} {middle_name_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit[0] + '.'} {middle_name_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit} {middle_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{title_translation} {first_name_translit} {middle_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {middle_name_translit} {surname_name_translit}".strip(),
    ]

    return combinations

def generate_short_names_3(full_name):
    # Split the name into parts
    parts = full_name.split()

    # Check if title exists
    title = parts[1] if parts[1] in ["श्री.", "श्रीमती", "डॉ.", "प्रोफेसर.", "सर", "श्री.डॉ.", "श्री.प्रा.", "श्री.सर"] else ""

    # Find surname
    surname = parts[0]

    # Initialize first name and middle name
    first_name = ""
    if len(parts) == 3:  # Middle name is provided
        first_name = parts[2]

    # Transliterate first name and middle name
    first_name_translit = e.translit_sentence(first_name, 'mr')
    title_translit = e.translit_sentence(title, 'mr')
    surname_name_translit = e.translit_sentence(surname, 'mr')
    title_translation = model.translate_paragraph(title, "mar_Deva", "eng_Latn")
    first_name_translit_1 = e1.translit_sentence(first_name_translit[0], 'mr')
    # Generate combinations of short names
    combinations = [
        f"{surname} {title} {first_name}".strip(),
        f"{surname} {first_name}".strip(),
        f"{title} {first_name} {surname}".strip(),
        f"{first_name} {surname}".strip(),
        # as_it_is
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {surname}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'}".strip(),
        # english_short
        f"{surname} {first_name_translit_1 + '.'}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'}".strip(),
        f"{first_name_translit_1 + '.'} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {surname}".strip(),
        # english
        f"{surname_name_translit} {title_translit} {first_name_translit}".strip(),
        f"{surname_name_translit} {first_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {first_name_translit[0] + '.'}".strip(),
        f"{title_translit} {first_name_translit} {surname_name_translit}".strip(),
        f"{title_translit} {first_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{first_name_translit} {surname_name_translit}".strip(),
        f"{first_name_translit[0] + '.'} {surname_name_translit}".strip(),
        # translation
        f"{surname_name_translit} {title_translation} {first_name_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit[0] + '.'}".strip(),
        f"{title_translation} {first_name_translit} {surname_name_translit}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {surname_name_translit}".strip(),
    ]

    return combinations

def generate_short_names_5(full_name):
    # Split the name into parts
    parts = full_name.split()

    # Check if title exists
    title = parts[1] if parts[1] in ["श्री.", "श्रीमती", "डॉ.", "प्रोफेसर.", "सर", "श्री.डॉ.", "श्री.प्रा.", "श्री.सर"] else ""

    # Find surname
    surname = parts[0]

    # Initialize first name and middle name
    first_name = ""
    middle_name = ""
    middle_name_1 = ""
    if len(parts) == 5:  # Middle name is provided
        first_name = parts[2]
        middle_name = parts[3]
        middle_name_1 = parts[4]

    # Transliterate first name and middle name
    first_name_translit = e.translit_sentence(first_name, 'mr')
    middle_name_translit = e.translit_sentence(middle_name, 'mr')
    middle_name_1_translit = e.translit_sentence(middle_name_1, 'mr')
    title_translit = e.translit_sentence(title, 'mr')
    surname_name_translit = e.translit_sentence(surname, 'mr')
    title_translation = model.translate_paragraph(title, "mar_Deva", "eng_Latn")
    first_name_translit_1 = e1.translit_sentence(first_name_translit[0], 'mr')
    middle_name_translit_1 = e1.translit_sentence(middle_name_translit[0], 'mr')
    middle_name_1_translit_1 = e1.translit_sentence(middle_name_1_translit[0], 'mr')
    # Generate combinations of short names
    combinations = [
        f"{surname} {title} {first_name} {middle_name} {middle_name_1}".strip(),
        f"{surname} {first_name} {middle_name} {middle_name_1}".strip(),
        f"{title} {first_name} {middle_name} {middle_name_1} {surname}".strip(),
        f"{first_name} {middle_name} {middle_name_1} {surname}".strip(),
        # as_it_is
        f"{surname} {title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1}".strip(),
        f"{surname} {title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'}".strip(),
        f"{surname} {title} {first_name} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'}".strip(),
        f"{title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {surname}".strip(),
        f"{title} {first_name} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {surname}".strip(),
        f"{title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {surname}".strip(),
        f"{first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {surname}".strip(),
        f"{first_name} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {surname}".strip(),
        f"{first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {surname}".strip(),
        f"{surname} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1}".strip(),
        f"{surname} {first_name} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'}".strip(),
        f"{surname} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'}".strip(),

        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {surname}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {surname}".strip(),
        # english_short
        f"{surname} {title} {first_name} {middle_name_translit_1 + '.'} {middle_name_1}".strip(),
        f"{surname} {title} {first_name} {middle_name} {middle_name_1_translit_1 + '.'}".strip(),
        f"{surname} {title} {first_name} {middle_name_translit_1 + '.'} {middle_name_1_translit_1}".strip(),
        f"{surname} {first_name} {middle_name_translit_1 + '.'} {middle_name_1}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name} {middle_name_1}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name} {middle_name_1}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name} {middle_name_1_translit_1 + '.'}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1_translit_1 + '.'}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {surname}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1_translit_1 + '.'} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1_translit_1 + '.'} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {surname}".strip(),
        f"{title} {first_name} {middle_name_translit_1 + '.'} {middle_name_1} {surname}".strip(),
        f"{first_name} {middle_name_translit_1 + '.'} {middle_name_1} {surname}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name} {middle_name_1} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name} {middle_name_1} {surname}".strip(),
        # english
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit}".strip(),
        f"{first_name_translit} {middle_name_translit} {middle_name_1_translit} {surname_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit}".strip(),
        f"{surname_name_translit} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit}".strip(),
        f"{title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {surname_name_translit}".strip(),
        f"{first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {surname_name_translit}".strip(),
        f"{title_translit} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {surname_name_translit}".strip(),
        f"{title_translit} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {surname_name_translit}".strip(),
        f"{first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {surname_name_translit}".strip(),
        f"{first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {surname_name_translit}".strip(),
        # translation
        f"{surname_name_translit} {title_translation} {first_name_translit} {middle_name_translit} {middle_name_1_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {surname_name_translit} {middle_name_1_translit}".strip(),
        f"{title_translation} {first_name_translit} {middle_name_translit[0] + '.'} {surname_name_translit} {middle_name_1_translit}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {middle_name_translit} {surname_name_translit} {middle_name_1_translit}".strip(),
    ]

    return combinations


def generate_short_names_6(full_name):
    # Split the name into parts
    parts = full_name.split()

    # Check if title exists
    title = parts[1] if parts[1] in ["श्री.", "श्रीमती", "डॉ.", "प्रोफेसर.", "सर", "श्री.डॉ.", "श्री.प्रा.", "श्री.सर"] else ""

    # Find surname
    surname = parts[0]

    # Initialize first name and middle name
    first_name = ""
    middle_name = ""
    middle_name_1 = ""
    last_name = ""
    if len(parts) == 6:  # Middle name is provided
        first_name = parts[2]
        middle_name = parts[3]
        middle_name_1 = parts[4]
        last_name = parts[5]

    # Transliterate first name and middle name
    first_name_translit = e.translit_sentence(first_name, 'mr')
    middle_name_translit = e.translit_sentence(middle_name, 'mr')
    middle_name_1_translit = e.translit_sentence(middle_name_1, 'mr')
    last_name_translit = e.translit_sentence(last_name, 'mr')
    title_translit = e.translit_sentence(title, 'mr')
    surname_name_translit = e.translit_sentence(surname, 'mr')
    title_translation = model.translate_paragraph(title, "mar_Deva", "eng_Latn")
    first_name_translit_1 = e1.translit_sentence(first_name_translit[0], 'mr')
    middle_name_translit_1 = e1.translit_sentence(middle_name_translit[0], 'mr')
    middle_name_1_translit_1 = e1.translit_sentence(middle_name_1_translit[0], 'mr')
    last_name_translit_1 = e1.translit_sentence(last_name_translit[0], 'mr')
    # Generate combinations of short names
    combinations = [
        f"{surname} {title} {first_name} {middle_name} {middle_name_1} {last_name}".strip(),
        f"{surname} {first_name} {middle_name} {middle_name_1} {last_name}".strip(),
        f"{title} {first_name} {middle_name} {middle_name_1} {last_name} {surname}".strip(),
        f"{first_name} {middle_name} {middle_name_1} {last_name} {surname}".strip(),
        # as_it_is
        f"{surname} {title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {last_name}".strip(),
        f"{surname} {title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name}".strip(),
        f"{surname} {title} {first_name} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name}".strip(),
        f"{surname} {title} {first_name} {middle_name} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {last_name} {surname}".strip(),
        f"{title} {first_name} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name} {surname}".strip(),
        f"{title} {first_name} {middle_name} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name} {surname}".strip(),
        f"{title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{surname} {title} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{surname} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{first_name} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{first_name} {middle_name} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name} {surname}".strip(),
        f"{surname} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {last_name}".strip(),
        f"{surname} {first_name} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name}".strip(),
        f"{surname} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name}".strip(),
        f"{surname} {first_name} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{surname} {first_name} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {last_name}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {last_name} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {last_name} {surname}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {last_name}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {last_name}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {last_name}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {last_name} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {last_name} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {last_name} {surname}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{surname} {title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{surname} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {middle_name_1} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {list(grapheme.graphemes(middle_name))[0] + '.'} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        f"{title} {list(grapheme.graphemes(first_name))[0] + '.'} {middle_name} {list(grapheme.graphemes(middle_name_1))[0] + '.'} {list(grapheme.graphemes(last_name))[0] + '.'} {surname}".strip(),
        # english_short
        f"{surname} {title} {first_name} {middle_name_translit_1 + '.'} {middle_name_1} {last_name}".strip(),
        f"{surname} {title} {first_name} {middle_name} {middle_name_1_translit_1 + '.'} {last_name}".strip(),
        f"{surname} {title} {first_name} {middle_name} {middle_name_1} {last_name_translit_1 + '.'}".strip(),
        f"{surname} {title} {first_name} {middle_name_translit_1 + '.'} {middle_name_1_translit_1} {last_name}".strip(),
        f"{surname} {first_name} {middle_name_translit_1 + '.'} {middle_name_1} {last_name}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name} {middle_name_1} {last_name}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name} {middle_name_1} {last_name}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {last_name}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {last_name}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name} {middle_name_1_translit_1 + '.'} {last_name}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1_translit_1 + '.'} {last_name}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {last_name} {surname}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1_translit_1 + '.'} {last_name} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1_translit_1 + '.'} {last_name} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {last_name} {surname}".strip(),
        f"{title} {first_name} {middle_name_translit_1 + '.'} {middle_name_1} {last_name} {surname}".strip(),
        f"{first_name} {middle_name_translit_1 + '.'} {middle_name_1} {last_name} {surname}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name} {middle_name_1} {last_name} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name} {middle_name_1} {last_name} {surname}".strip(),
        f"{surname} {title} {first_name} {middle_name_translit_1 + '.'} {middle_name_1_translit_1} {last_name_translit_1 + '.'}".strip(),
        f"{surname} {first_name} {middle_name_translit_1 + '.'} {middle_name_1} {last_name_translit_1 + '.'}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name} {middle_name_1} {last_name_translit_1 + '.'}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name} {middle_name_1} {last_name_translit_1 + '.'}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {last_name_translit_1 + '.'}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {last_name_translit_1 + '.'}".strip(),
        f"{surname} {first_name_translit_1 + '.'} {middle_name} {middle_name_1_translit_1 + '.'} {last_name_translit_1 + '.'}".strip(),
        f"{surname} {title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1_translit_1 + '.'} {last_name_translit_1 + '.'}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {last_name} {surname}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1_translit_1 + '.'} {last_name_translit_1 + '.'} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1_translit_1 + '.'} {last_name_translit_1 + '.'} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name_translit_1 + '.'} {middle_name_1} {last_name_translit_1 + '.'} {surname}".strip(),
        f"{title} {first_name} {middle_name_translit_1 + '.'} {middle_name_1} {last_name_translit_1 + '.'} {surname}".strip(),
        f"{first_name} {middle_name_translit_1 + '.'} {middle_name_1} {last_name_translit_1 + '.'} {surname}".strip(),
        f"{first_name_translit_1 + '.'} {middle_name} {middle_name_1} {last_name_translit_1 + '.'} {surname}".strip(),
        f"{title} {first_name_translit_1 + '.'} {middle_name} {middle_name_1} {last_name_translit_1 + '.'} {surname}".strip(),
        # english
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{first_name_translit} {middle_name_translit} {middle_name_1_translit} {last_name_translit} {surname_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit[0] + '.'} {last_name_translit}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit[0] + '.'} {last_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit[0] + '.'} {last_name_translit}".strip(),
        f"{surname_name_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit} {surname_name_translit}".strip(),
        f"{first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit} {surname_name_translit}".strip(),
        f"{title_translit} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit} {surname_name_translit}".strip(),
        f"{title_translit} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit} {surname_name_translit}".strip(),
        f"{first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit} {surname_name_translit}".strip(),
        f"{first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit} {surname_name_translit}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit[0] + '.'} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {first_name_translit} {middle_name_translit} {middle_name_1_translit[0] + '.'} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit[0] + '.'} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{title_translit} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{title_translit} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{title_translit} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'} {surname_name_translit}".strip(),
        f"{first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit[0] + '.'} {surname_name_translit}".strip(),
        # translation
        f"{surname_name_translit} {title_translation} {first_name_translit} {middle_name_translit} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {surname_name_translit} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{title_translation} {first_name_translit} {middle_name_translit[0] + '.'} {surname_name_translit} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {middle_name_translit} {surname_name_translit} {middle_name_1_translit} {last_name_translit}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit[0] + '.'} {middle_name_translit} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{surname_name_translit} {title_translation} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {middle_name_translit[0] + '.'} {surname_name_translit} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{title_translation} {first_name_translit} {middle_name_translit[0] + '.'} {surname_name_translit} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {middle_name_translit} {surname_name_translit} {middle_name_1_translit} {last_name_translit[0] + '.'}".strip(),
        f"{title_translation} {first_name_translit[0] + '.'} {middle_name_translit} {surname_name_translit[0] + '.'} {middle_name_1_translit[0] + '.'} {last_name_translit}".strip()
        ]

    return combinations


df = pd.read_excel(r"./total_members.xlsx")#your names file

# Function to translate text using the translation model
def translate_text_3(text):
    if isinstance(text, str):
        return generate_short_names_3(text)
    else:
        return text

def translate_text_4(text):
    if isinstance(text, str):
        return generate_short_names_4(text)
    else:
        return text

def translate_text_5(text):
    if isinstance(text, str):
        return generate_short_names_5(text)
    else:
        return text

def translate_text_6(text):
    if isinstance(text, str):
        return generate_short_names_6(text)
    else:
        return text

def generate_short_names(full_name):
   if isinstance(full_name, str):
      if len(full_name.split()) == 3:
          return translate_text_3(full_name)
      elif len(full_name.split()) == 4:
          return translate_text_4(full_name)
      elif len(full_name.split()) == 5:
          return translate_text_5(full_name)
      elif len(full_name.split()) == 6:
          return translate_text_6(full_name)
   else:
       return full_name



tqdm.pandas()
df['combinations'] = df['Right name'].progress_apply.progress_apply(generate_short_names)

# SAVE the DataFrame with the new column
df.to_excel("alias_members_name.xlsx", index=False)
# print(generate_short_names("पवार श्रीमती उमेशा शंकर"))
