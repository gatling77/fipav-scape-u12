from standings import Team, Match, Score, Championship
import json

def main():
    file = "campionato.json"
    with open(file, "r") as infile: 
        d = json.load(infile)
    champ = Championship.from_json(d)

    with open("stats.json", "w") as out_file: 
        json.dump(champ.stats(),indent=True, fp= out_file)


if __name__ == "__main__":
    main()