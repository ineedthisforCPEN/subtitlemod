# subtitlemod
`subtitlemod` is a quick and simple tool that modifies subtitle file timings.

Turns out VLC does time shifting for you, so this might not be useful at all...

## Supported Files
* .srt (SubRip Subtitle File)

## Current Feature Set
* CLI arguments
  * Set output file
  * Set shift value
  * Set stretch factor
* Time formating (i.e. "ms", "s", "m", "h")

## TODO
[x] Add command-line options (argparse)
[x] CLI Option: set input file
[x] CLI Option: set output file
[x] CLI Option: set shift time
[x] CLI Option: set stretch factor
[x] Stretch timings by a given factor
[x] "Pretty" time string for shift/stretch time (e.g. 10s for 10 seconds)