import json
import argparse

def modify_json(input_file, sourcel, targetl):
    a_file = open("./config1.json", "r")
    json_object = json.load(a_file)
    a_file.close()

    json_object["options"]["input file"] = input_file
    json_object["options"]["align file"] = "/content/forward_align.txt"
    json_object["options"]["token file"] = input_file[:-4] + "_token.txt"
    json_object["options"]["source language"] = sourcel

    if sourcel == "ru":
        json_object["options"]["source language extended"] = "ru", "ba", "be", "bg", "kk", "ky", "mk", "mn", "sr", "tt", "uk"
    elif sourcel == "en":
        json_object["options"]["source language extended"] = "en", "fr"
    else:
        json_object["options"]["source language extended"] = sourcel

    json_object["options"]["target language"] = targetl
    if targetl == "ru":
        json_object["options"]["target language extended"] = "ru", "ba", "be", "bg", "kk", "ky", "mk", "mn", "sr", "tt", "uk"
    elif targetl == "en":
        json_object["options"]["target language extended"] = "en", "fr"
    else:
        json_object["options"]["target language extended"] = targetl

# Пример изменения других полей (фильтров)
#    json_object["policies"][0] = ["OneNo", "off"]

    a_file = open("./config1.json", "w")
    json.dump(json_object, a_file)
    a_file.close()

def _main():
    parser = argparse.ArgumentParser('Modify config.json file for further prccessing.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--inputs', type=str, 
                        help='input text file')

    parser.add_argument('-s', '--source', type=str,
                        help='source language')

    parser.add_argument('-t', '--target', type=str,
                        help='target language')

    args = parser.parse_args()
    modify_json(input_file=args.inputs,
       sourcel=args.source,
       targetl = args.target)


if __name__ == '__main__':
    _main()