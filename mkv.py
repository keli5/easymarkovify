import markovify
import sys
import json
from os.path import exists
STATE_SIZE = 3  # The number of words to consider when generating a new sentence. ae
TRIES = STATE_SIZE * 10  # The number of times to try to generate a sentence before giving up.
MODEL_FILE = 'model.json'  # The name of the file to save the model to
MODEL_TYPE = markovify.Text  # The type of model to use. markovify.Text or markovify.NewlineText (or a custom model)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if ('-r' in sys.argv) or not exists(MODEL_FILE):
    print(bcolors.WARNING + "Building model")
    with open("corpus.txt", encoding="utf-8") as f:
        text = f.read()
    model = MODEL_TYPE(text, well_formed=False, state_size=STATE_SIZE)
    model = model.compile()
    model_json = model.to_json()
    with open(MODEL_FILE, 'w') as f:
        json.dump(model_json, f)
    print(bcolors.OKGREEN + "Saved")
else:
    print(bcolors.WARNING + "Loading model from disk")
    with open(MODEL_FILE) as f:
        model_json = json.load(f)
    try:
        model = markovify.Text.from_json(model_json)
    except Exception as e:
        print(bcolors.FAIL + "Error loading model: " + str(e))
        exit(1)

print(bcolors.ENDC)
if '-i' in sys.argv:
    starting = ""
    while True:
        print(bcolors.OKBLUE + "Options:")
        print("g - Generate")
        print("s - Generate + start")
        print("q - Quit")
        choice = input(bcolors.OKGREEN + "Choice (g): ")

        print(bcolors.ENDC, end="")
        if choice == 'g':
            print(model.make_sentence(tries=TRIES))

        elif choice == 's':
            prev = starting or ""
            starting = input(f"Starting words (max length {STATE_SIZE}): ")
            if starting == "":
                if prev != "":
                    starting = prev
                else:
                    print(model.make_sentence(tries=TRIES))
                    continue
            print(model.make_sentence_with_start(starting))

        elif choice == 'q':
            exit(0)

        elif choice == "":
            print(model.make_sentence(tries=TRIES))

else:
    print(model.make_sentence(tries=TRIES))
