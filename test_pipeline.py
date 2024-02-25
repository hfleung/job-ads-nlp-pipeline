import sys
import libs
from nltk.tokenize import word_tokenize

# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    print("Usage: python3 test_pipeline.py <job ads file> <target keywords file>")
    sys.exit(1)

# Get the file names from the command line argument
job_ads_file = sys.argv[1]
target_keywords_file = sys.argv[2]

try:
    # Read the files in read mode
    with open(job_ads_file, 'r') as file:
        job_ads = file.read()
    with open(target_keywords_file, 'r') as file:
        target_keywords = file.read()
        target_keywords_list = target_keywords.split('\n')
        target_keywords_list = [keyword.lower() for keyword in target_keywords_list if keyword != '']

    # Extract keywords from the text
    keyword_map = libs.extract_keywords(job_ads)
    all_synonyms = set(item for sublist in keyword_map.values() for item in sublist)

    # Calculate stats
    num_words = len(word_tokenize(job_ads))
    num_target_keywords = len(target_keywords_list)
    num_matched_keywords = 0
    for keyword in target_keywords_list:
        if keyword in all_synonyms:
            num_matched_keywords += 1
    num_extracted_keywords = len(keyword_map.keys())
    num_unmatched_extracted_keywords = num_extracted_keywords - num_matched_keywords

    # Print stats
    print("Number of words in the job ads:", num_words)
    print("Number of target keywords:", num_target_keywords)
    print("Number of extracted keywords:", num_extracted_keywords)
    print("Number of matched keywords:", num_matched_keywords)
    print("Number of unmatched extracted keywords:", num_unmatched_extracted_keywords)
    print("Extracted keywords / Total number of words in ads:", round(num_extracted_keywords / num_words * 100, 2), "%")
    print("Matched keywords / Target keywords:", round(num_matched_keywords / num_target_keywords * 100, 2), "%")
    print("Unmatched extracted keywords / Extracted keywords:", round(num_unmatched_extracted_keywords / num_extracted_keywords * 100, 2), "%")

except FileNotFoundError:
    print("File not found!")
except Exception as e:
    print("An error occurred:", e)
