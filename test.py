def read_file_line_by_line(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# List of filenames you want to process
file_names = ['auth.log', 'syslog', 'log.txt']

# Loop through the list of filenames and read each file line by line
for file_name in file_names:
    print(f"Reading lines from '{file_name}':")
    for line in read_file_line_by_line(file_name):
        print(line)
    print()  # Print an empty line to separate the output of different files
