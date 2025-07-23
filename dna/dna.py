import csv
import sys

def main():
    # Check command-line usage
    if len(sys.argv) != 3:
        sys.exit("python dna.py data.csv sequence.txt")

    # Read database file into a variable
    database = []
    with open(sys.argv[1], 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as file:
        dna_sequence = file.read()

    # Find longest match of each STR in DNA sequence
    subsequences = list(database[0].keys())[1:]  # Exclude the name column

    results = {}
    for subsequence in subsequences:
        # FIXED: Changed 'result' to 'results'
        results[subsequence] = longest_match(dna_sequence, subsequence)

    # Check database for matching profiles
    for person in database:
        match = True
        for subsequence in subsequences:
            # Compare integer values of STR counts
            if int(person[subsequence]) != results[subsequence]:
                match = False
                break

        if match:
            print(person['name'])
            return

    print("No match")

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0

        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length

            # Exit early if beyond sequence length
            if end > sequence_length:
                break

            if sequence[start:end] == subsequence:
                count += 1
            else:
                break

        longest_run = max(longest_run, count)

    return longest_run

if __name__ == "__main__":
    main()
