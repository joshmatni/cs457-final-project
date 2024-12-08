import math

def split_csv(input_file, output_prefix, num_files=50):
    # Step 1: Count total lines in input file
    with open(input_file, 'r', encoding='utf-8', newline='') as f:
        total_lines = sum(1 for line in f)

    # Assume first line is header
    header_count = 1
    data_lines = total_lines - header_count

    # Calculate how many lines per file (excluding header)
    lines_per_file = math.ceil(data_lines / num_files)

    # Step 2: Split the file
    with open(input_file, 'r', encoding='utf-8', newline='') as f:
        header = next(f)  # Read the header line

        file_count = 1
        line_count = 0

        # Initialize the first output file
        out_file = open(f"{output_prefix}_{file_count}.csv", 'w', encoding='utf-8', newline='')
        out_file.write(header)

        for line in f:
            out_file.write(line)
            line_count += 1

            # If we reached the lines_per_file limit, start a new file
            if line_count >= lines_per_file and file_count < num_files:
                out_file.close()
                file_count += 1
                line_count = 0
                out_file = open(f"{output_prefix}_{file_count}.csv", 'w', encoding='utf-8', newline='')
                out_file.write(header)

        # Close the last file
        out_file.close()

    print(f"Split complete. Created {file_count} files.")

if __name__ == "__main__":

    input_file = "processed_transactions.csv"
    output_prefix = "split_data"    # The prefix for the output CSV files
    num_files = 50                 
    split_csv(input_file, output_prefix, num_files)
