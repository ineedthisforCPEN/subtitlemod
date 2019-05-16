"""
subtitlemod

A quick and simple tool that modifies subtitle file timings.
"""

import argparse
import re
import time

TIME_DELAY_MS = 500

def str_to_time(s):
    hours, minutes, seconds = s.strip().split(":")
    seconds, millis = seconds.strip().split(",")

    total_time = int(millis)
    total_time += int(seconds) * 1000
    total_time += int(minutes) * 60 * 1000
    total_time += int(hours) * 60 * 60 * 1000
    return total_time
#/def

def time_to_str(t):
    return "{h:02}:{m:02}:{s:02},{mm:03}".format(
        h=t//(60*60*1000),
        m=(t//(60*1000))%60,
        s=(t//1000)%60,
        mm=t%1000)
#/def

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
    pattern_timestamp = re.compile(r"\d{2}:\d{2}:\d{2},\d{3}")
    delayed = ""

    with open("./subs.srt", "r") as srt_file:
        file_content = srt_file.read()
        matches = re.findall(pattern_timestamp, file_content)

        for m in matches:
            file_content = file_content.replace(m.strip(), time_to_str(str_to_time(m) - TIME_DELAY_MS))
        #/for

        with open("./delayed.srt", "w") as delayed_file:
            delayed_file.write(file_content)
        #/with
    #/with
#/def

if __name__ == "__main__":
    args = argument_parse()
#/if