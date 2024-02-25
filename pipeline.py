import sys
import libs

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python3 pipeline.py <job ads file>")
    sys.exit(1)

# Get the file name from the command line argument
filename = sys.argv[1]

try:
    # Read the file in read mode
    with open(filename, 'r') as file:
        text = file.read()

    # Extract keywords from the text
    keyword_map = libs.extract_keywords(text)

    # Generate a query from the keyword map
    query = libs.generate_query(keyword_map)
    print(query)

except FileNotFoundError:
    print("File not found!")
except Exception as e:
    print("An error occurred:", e)
