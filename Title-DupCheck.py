from fuzzywuzzy import fuzz

# Function to clean up book names
def clean_book_name(book_name):
    # Strip whitespace and lowercase book name
    cleaned_name = book_name.strip().lower()
    # Replace any double spaces with single spaces
    cleaned_name = cleaned_name.replace("  ", " ")
    # Remove any non-alphanumeric characters
    cleaned_name = ''.join(e for e in cleaned_name if e.isalnum() or e.isspace())
    return cleaned_name

# Read in book names from text file
with open("book_names.txt", "r") as f:
    book_names = f.readlines()

# Clean up book names
cleaned_book_names = [clean_book_name(name) for name in book_names]

# Create a dictionary to hold cleaned book names
cleaned_book_dict = {}

# Loop through book names and compare against each other
for i in range(len(cleaned_book_names)):
    for j in range(i + 1, len(cleaned_book_names)):
        # Calculate similarity score using fuzzywuzzy library
        similarity_score = fuzz.token_sort_ratio(cleaned_book_names[i], cleaned_book_names[j])
        # If similarity score is greater than or equal to 80%, prompt user to remove redundant book name
        if similarity_score >= 80:
            print(f"Similarity score of {similarity_score}% between \"{book_names[i].strip()}\" and \"{book_names[j].strip()}\"")
            print("Please choose which book name to keep (1 or 2), or enter 0 to keep both:")
            print(f"1: {book_names[i].strip()}")
            print(f"2: {book_names[j].strip()}")
            choice = input()
            if choice == "1":
                cleaned_book_dict[i] = cleaned_book_names[i]
            elif choice == "2":
                cleaned_book_dict[i] = cleaned_book_names[j]
            elif choice == "0":
                # If user chooses to keep both, combine the two book names
                combined_name = f"{book_names[i].strip()} and {book_names[j].strip()}"
                cleaned_book_dict[i] = clean_book_name(combined_name)
            else:
                print("Invalid choice, keeping both book names.")
                combined_name = f"{book_names[i].strip()} and {book_names[j].strip()}"
                cleaned_book_dict[i] = clean_book_name(combined_name)
        else:
            # If similarity score is below 80%, add book name to cleaned_book_dict
            cleaned_book_dict[i] = cleaned_book_names[i]

# Output cleaned up book names to text file
with open("cleaned_book_names.txt", "w") as f:
    for i in range(len(cleaned_book_dict)):
        f.write(f"{book_names[i].strip()} --> {cleaned_book_dict[i]}\n")
