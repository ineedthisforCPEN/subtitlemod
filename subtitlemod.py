"""
subtitlemod

A quick and simple tool that modifies subtitle file timings.
"""

###############################################################################
# Imports and Constants
###############################################################################
import argparse
import re
import time

# Default arguments
DEFAULT_SHIFT = 0
DEFAULT_STRETCH = 1.0

# Note about patterns:
#   Shift: can be any negative or positive integer
#   Stretch: can only be positive, non-zero integer or float
#   Timestamp: fixed to SRT format - may require changes
PATTERN_STR_SHIFT = r"^-?\d+(ms|s|m|h)?$"
PATTERN_STR_STRETCH = r"^(0*[1-9][0-9]*(\.[0-9]+)?|0+\.[0-9]*[1-9][0-9]*)$"
PATTERN_STR_TIMESTAMP = r"\d{2}:\d{2}:\d{2},\d{3}"

PATTERN_SHIFT = re.compile(PATTERN_STR_SHIFT)
PATTERN_STRETCH = re.compile(PATTERN_STR_STRETCH)
PATTERN_TIMESTAMP = re.compile(PATTERN_STR_TIMESTAMP)


###############################################################################
# Helper Functions: Conversion and Formatting
###############################################################################
def str_to_time(s):
    """
    Convert a string with the format HH:MM:SS,mmm (m being
    milliseconds) into the equivalent number of milliseconds.

    Note: currently hardcoded to this format, may need to be
    updated.
    """
    hours, minutes, seconds = s.strip().split(":")
    seconds, millis = seconds.strip().split(",")

    total_time = int(millis)
    total_time += int(seconds) * 1000
    total_time += int(minutes) * 60 * 1000
    total_time += int(hours) * 60 * 60 * 1000
    return total_time
#/def


def time_to_str(t):
    """
    Convert time as a number of milliseconds into the format
    HH:MM:SS,mmm (m being milliseconds).

    Note: currently hardcoded to this format, may need to be
    updated.
    """
    return "{h:02}:{m:02}:{s:02},{mm:03}".format(
        h=t//(60*60*1000),
        m=(t//(60*1000))%60,
        s=(t//1000)%60,
        mm=t%1000)
#/def


###############################################################################
# Main Functions: Argument Handling and Main Function
###############################################################################
def argument_parse():
    """
    A wrapper for Python argparse. The wrapper initialized the argument
    parser, reads them from the command line, then verifies and
    modifies the arguments as required.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("subfile", type=str,
                        help="The subtitle file whose timings to modify")
    parser.add_argument("-o", "--output-file", type=str,
                        help="The output file containing the modified content"
                            +" (default: [original_name]_modified.[extension])")
    parser.add_argument("-s", "--shift", default="0", type=str,
                        help="The amount by which to shift all subtitle "
                            +"timings (default: 0 milliseconds)")
    parser.add_argument("-x", "--stretch", default="1.0", type=str,
                        help="The factor by which to stretch subtitle timings "
                            +"(default: 1.0)")
    args = parser.parse_args()

    # Create an output file if one is not provided
    if args.output_file is None:
        split_input = args.subfile.split(".")
        args.output_file = ".".join(split_input[:-1]) + "_modified." + split_input[-1]
    #/if

    # Ensure that the stretch and shift times are valid entries
    try:
        args.shift = int(args.shift, 10)
    except ValueError:
        raise ValueError("The SHIFT value must be a valid integer") from None
    #/try

    try:
        args.stretch = float(args.stretch)
    except ValueError:
        raise ValueError("The STRETCH value must be a valid float") from None
    #/try

    # Forward the (now confirmed to be valid) arguments
    return args
#/def


def main():
    args = argument_parse()
    print("subtitlemod ver " + VERSION)

    # Warn users of unimplemented CLI options they may have input
    if args.shift != DEFAULT_SHIFT:
        print("WARNING\t SHIFT option not implemented")
    if args.stretch != DEFAULT_STRETCH:
        print("WARNING\t STRETCH option not implemented")
    #/if
    delayed = ""

    with open("./subs.srt", "r") as srt_file:
        file_content = srt_file.read()
        matches = re.findall(PATTERN_TIMESTAMP, file_content)

        for m in matches:
            file_content = file_content.replace(m.strip(), time_to_str(str_to_time(m) - TIME_DELAY_MS))
        #/for

        with open("./delayed.srt", "w") as delayed_file:
            delayed_file.write(file_content)
        #/with
    #/with
#/def


if __name__ == "__main__":
    main()
#/if