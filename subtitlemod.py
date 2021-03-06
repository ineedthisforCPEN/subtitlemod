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
DEFAULT_SHIFT = "0"
DEFAULT_STRETCH = "1.0"
TIME_EXTENSION = {"":1, "ms":1, "s":1000, "m":60*1000, "h":60*60*1000}
VERSION = "1.0.0"

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
    t = max(t, 0)
    return "{h:02}:{m:02}:{s:02},{mm:03}".format(
        h=int(t/(60*60*1000)),
        m=int((t/(60*1000))%60),
        s=int((t/1000)%60),
        mm=int(t%1000))
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
    parser.add_argument("-s", "--shift", default=DEFAULT_SHIFT, type=str,
                        help="The amount by which to shift all subtitle "
                            +"timings (default: 0 milliseconds)")
    parser.add_argument("-x", "--stretch", default=DEFAULT_STRETCH, type=str,
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
        split_time = re.split(r"(\d+)", args.shift)
        args.shift = int(split_time[1]) * TIME_EXTENSION[split_time[2]]
    except ValueError:
        errstr = "The SHIFT value must be an integer with a valid extension "
        errstr += "(i.e. ms, s, m, or h)"
        raise ValueError(errstr) from None
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
    print("subtitlemod ver. " + VERSION)

    print("")
    print("Subtitle file: " + args.subfile)
    print("Output file:   " + args.output_file)
    print("Shift:         " + str(args.shift) + "ms")
    print("Stretch:       " + str(args.stretch))

    with open(args.subfile, "r") as subfile:
        content = subfile.read()
        matches = re.findall(PATTERN_TIMESTAMP, content)

        for m in matches:
            newtime = time_to_str(args.stretch*str_to_time(m) - args.shift)
            content = content.replace(m, newtime)
        #/for

        with open(args.output_file, "w") as outfile:
            outfile.write(content)
        #/with
    #/with
#/def


if __name__ == "__main__":
    main()
#/if