import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filepath',
                        dest='filepath',
                        type=str,
                        required=True)

args = parser.parse_args()
filepath = args.filepath

def remove_duplicate_lines(file_path):
    """Removes duplicate lines from a log file while preserving order."""
    seen_lines = set()
    unique_lines = []

    with open(file_path, "r") as file:
        for line in file:
            if line not in seen_lines:
                seen_lines.add(line)
                unique_lines.append(line)

    with open(file_path, "w") as file:
        file.writelines(unique_lines)




#file_path = "./logs/info2/obxd_test/T2_obxd.log"
remove_duplicate_lines(filepath)