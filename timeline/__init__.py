#
# Package contains edl and timecode modules
# The edl module depends heavily on the timecode module of course.
# Besides the original filenames you can import these using the submodules (or aliases)
# defined in the package __init__ file
#

import edlClasses, Timecode

edl = edlClasses
edls = edlClasses
EDL = edlClasses
EDLs = edlClasses

timecode = Timecode
tc = Timecode
TC = Timecode
