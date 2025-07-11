import csv
import sys


def main():

    # TODO: Check for command-line usage
    // if len(sys.argv) != 3:
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    database_file = sys.argv[1]
    sequence_file = sys.argv[2]
    database = []
    with open(database_file, 'r') as db_file:
        reader = csv.DictReader(db_file)
        for row in reader:
            database.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sequence_file, 'r') as seq_file:
        sequence = seq_file.read().strip()

    # TODO: Find longest match of each STR in DNA sequence
    str_counts = {}
    for str_name in database[0].keys():
        if str_name != 'name':
            str_counts[str_name] = longest_match(sequence, str_name)

    # TODO: Check database for matching profiles
    for person in database:
        match = True
        for str_name in str_counts:
            if int(person[str_name]) != str_counts[str_name]:
                match = False
                break
        if match:
            print(person['name'])
            return
    # If no match found, print "No match"
    print("No match")
    sys.exit(0)
    # If incorrect command-line usage, print usage message and exit
    # if len(sys.argv) != 3:
    #     print("Usage: python dna.py data.csv sequence.txt")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
