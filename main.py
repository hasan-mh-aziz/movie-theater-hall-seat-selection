import sys
import getopt
import os
from Codes import movieTheater


def main(argv):
    movie_theater = movieTheater.MovieTheater(10, 20)

    # If the directory has spaces in it then argv will consider each part as separate arguments
    input_file_path = " ".join(argv)

    try:
        output_contents = []
        with open(input_file_path, "r") as f:
            for line in f:
                input_parts = line.split(" ")
                reservation_id, reservation_size = input_parts[0], int(input_parts[1])
                current_assigned_seats = movie_theater.reserve_seats(reservation_size)
                print(movie_theater)
                output_contents.append(" ".join([reservation_id, current_assigned_seats]))

        print(output_contents)
        input_path_parts = input_file_path.split("\\")
        input_file_name = input_path_parts.pop()
        output_directory = "/".join(input_path_parts + [f"output_for_{input_file_name}"])
        print(output_directory)
        with open(output_directory, 'w') as f:
            f.write("\n".join(output_contents))

        print("output file:", output_directory)
    except OSError:
        print("Could not open/read file:", input_file_path)
        sys.exit()


if __name__ == "__main__":
    # main(sys.argv[1:])
    main(["D:\marquetteOneDrive\OneDrive - Marquette University\Codes\pyCharmProjects\MovieTheaterSeating\Files\input1.txt"])
