# Root Driving History

## Problem Statement

Let's write some code to track driving history for people.

The code will process an input file. You can either choose to accept the input 
via stdin (e.g. if you're using Ruby `cat input.txt | ruby yourcode.rb`), or as a 
file name given on the command line (e.g. `ruby yourcode.rb input.txt`). You can 
use any programming language that you want. Please choose a language that allows 
you to best demonstrate your programming ability.

Each line in the input file will start with a command. There are two possible commands.

The first command is Driver, which will register a new Driver in the app. 

Example: `Driver Dan`

The second command is Trip, which will record a trip attributed to a driver. The 
line will be space delimited with the following fields: the command (Trip), driver 
name, start time, stop time, miles driven. Times will be given in the format of 
hours:minutes. We'll use a 24-hour clock and will assume that drivers never drive 
past midnight (the start time will always be before the end time). 

Example: `Trip Dan 07:15 07:45 17.3`

Discard any trips that average a speed of less than 5 mph or greater than 100 mph.

Generate a report containing each driver with total miles driven and average speed. 
Sort the output by most miles driven to least. Round miles and miles per hour to the 
nearest integer.

Example input:
```
Driver Dan
Driver Lauren
Driver Kumi
Trip Dan 07:15 07:45 17.3
Trip Dan 06:12 06:32 21.8
Trip Lauren 12:01 13:16 42.0
```

Expected output:
```
Lauren: 42 miles @ 34 mph
Dan: 39 miles @ 47 mph
Kumi: 0 miles
```

## Approach

- I decided to create objects to represent the data collected from the logs to 
mimic what one might expect with working from objects in a database/ORM. In order
to describe how Drivers and Trips interacted, I created the TripLog object,
where a TripLog is instantiated with a Driver, and Trips can be added to the log
via the `add_trip` method. I liked how this produced an easy way to describe 
how each Driver can have several Trips without needing to tie the Trips directly
to a Driver - this piece is what was inspired by what you would find in a 
normalized database.
- To parse the text logs I decided to use a function instead of a class because
I didn't think there was a need to keep state after the log was parsed. This 
also made it easier to test since I only needed to vary the inputs to inspect
the final result. I chose to use a function for creating the report string for
similar reasons.
- For parsing the text logs I used regular expressions, where I am specifically
looking for "Driver" and "Trip" for the keywords, though the assumption of correct
capitalization could be easily relaxed by adding flags to the `re.findall` function.
- I also decided to forgo most documentation in this coding example and instead
focused on providing typing and clear function/class names.
