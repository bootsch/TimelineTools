#! /usr/bin/env python
#
# $Name:  $ Timecode.py
#
#  $Author: bootsch $
#  $Revision: 409 $
#
#  Paul Boots
#  Copyright (c) bootsmaat, 2001 - 2016
#

"""A small tool set of Timecode functions.

The Timecode module has functions to convert between timecode and framecount, add and subtract,
compare and get durations. All functions take the 'fps' variable. The default value is 25 and
can be changed in the 'DEFAULT_FPS_VALUE' global variable. Calculation is done with framecount.
Be careful to provide the correct fps value!

Note on FrameCount: framecount is NOT the same as the actual number of frames! Framecount is 
absolute and as such the frame equavalent of SMPTE timecode. Framecount starts at zero (0) and
the maximum framecount for 25 fps time code is 2159999, 23.59.59.24 in timecode. For 24 fps the
maximum number is 2073599

Frames are the actual frames of which you have at least one, if you want picture that is.
"""

import string
from enum import Enum

DEFAULT_FPS_VALUE = 24

class INIT_TYPES (Enum):
    NOINIT     = 0
    FRAMECOUNT = 1
    TIMECODE   = 2

VALID_FRAMERATES = (24, 25, 30, 48, 50, 60)

MAX_VALUES = {
    24: {'max_frame': 23, 'max_framecount': 2073599},
    25: {'max_frame': 24, 'max_framecount': 2159999},
    30: {'max_frame': 29, 'max_framecount': 2591999},
    48: {'max_frame': 47, 'max_framecount': 4147199},
    50: {'max_frame': 49, 'max_framecount': 4319999},
    60: {'max_frame': 59, 'max_framecount': 5183999},
}

class FrameConversionError (Exception):
    """
    Error raised when the number passed as frames is not valid
    Frames must be 1 or larger and signify
    """

def assert_valid_frame_rate (fps):
    """
    Make sure we only work with valid values
    """
    assert fps in VALID_FRAMERATES, "Not a valid framerate: %r; Must be one of %s" % (fps, VALID_FRAMERATES)

def assert_valid_framecount (framecount, fps):
    max = MAX_VALUES [fps]['max_framecount']
    assert framecount >= 0 and framecount <= max, "Invalid framecount number: %r; Framecount must be between 0 and %d" % (framecount, maxs)

def assert_valid_timecode_frame (FF, fps):
    maxframe = MAX_VALUES [fps]['max_frame']
    assert FF >= 0 and FF <= maxframe,  "Invalid value for Frames: %r; Frames must be between 0 and %d" % (SS. maxframe)

def assert_valid_timecode (HH, MM, SS, FF, fps):
    """
    0 >= HH <= 23
    0 >= MM <= 59
    0 >= SS <= 59
    FF is framerate depended and found in MAX_VALUES
    """
    assert HH >= 0 and HH <= 23,  "Invalid value for Hours: %r; Hours must be between 0 and 23" % HH
    assert MM >= 0 and MM <= 59,  "Invalid value for Minutes: %r; Minutes must be between 0 and 59" % MM
    assert SS >= 0 and SS <= 59,  "Invalid value for Seconds: %r; Seconds must be between 0 and 59" % SS
    assert_valid_timecode_frame (FF, fps)

def get_max_timecode (fps):
    """
    Return the maximum timecode string
    >>> get_max_timecode (24)
    '23:59:59:23'
    """
    assert_valid_frame_rate (fps)
    return "23:59:59:%s" % MAX_VALUES [fps]['max_frame']

def get_max_framecount (fps):
    """
    Return the maximum framecount number
    """
    assert_valid_frame_rate (fps)
    return timeCode2frameCount ("23:59:59:%s" % MAX_VALUES [fps]['max_frame'], fps)

def compute_max_values ():
    for fps in VALID_FRAMERATES:
        print fps, get_max_timecode (fps), get_max_framecount (fps)

#
#  First part of this code are the separate functions in the module
#  Second part are the Class definition(s), a work in progress in an infant state
#  Third part is main which run the doc tests
#

#
#  Part 1
#
def timeCode2frameCount (timecode, fps = DEFAULT_FPS_VALUE):
    """    
    Convert a timecode string to (absolute) framecount. Provide frames per second in variable 'fps', default value is 25fps.
    See note on framecount above.
    
    >>> import Timecode
    
    >>> Timecode.timeCode2frameCount ("00:00:00:00", 25)
    0
    
    >>> Timecode.timeCode2frameCount ("00:00:00:01", 25)
    1
    
    >>> Timecode.timeCode2frameCount ("00:00:01:00", 25)
    25
    
    >>> Timecode.timeCode2frameCount ("00:00:01:00", 24)
    24
    
    >>> Timecode.timeCode2frameCount ("23:59:59:24", 25)
    2159999
    
    >>> Timecode.timeCode2frameCount ("23:59:59:23", 24)
    2073599
    
    """
    assert_valid_frame_rate (fps)
    # split timecode string into hours, minutes, seconds, frames
    tcList = string.split (timecode, ":")
    HH = string.atoi (tcList[0])
    MM = string.atoi (tcList[1])
    SS = string.atoi (tcList[2])
    FF = string.atoi (tcList[3])
    # Frame count = (hours * 60 * 60 + minutes * 60 + seconds) * fps + frames
    return ((HH*60*60 + MM * 60 + SS) * fps + FF)


def frameCount2timeCodeElements (frames, fps = DEFAULT_FPS_VALUE):
    """
        Convert a framecount to a timecode string. Provide fps in variable 'fps', default value is 25fps.
        This function is the inverse of timeCode2frameCount.
        
        """
    assert_valid_frame_rate (fps)
    FF = frames % fps
    frames = frames - FF
    if type (FF) == float:
        FF = int (round (FF))
    
    SS = (frames / fps) % 60
    frames = frames - (SS * fps)
    if type (SS) == float:
        SS = int (round (SS))
    
    MM = (frames / (fps * 60)) % 60
    frames = frames - (MM * fps * 60)
    if type (MM) == float:
        MM = int (round (MM))
    
    HH = (frames / (fps * 60 * 60)) % 24
    if type (HH) == float:
        HH = int (round (HH))
    
    return HH, MM, SS, FF

def frameCount2timeCode (frames, fps = DEFAULT_FPS_VALUE):
    """
    Convert a framecount to a timecode string. Provide fps in variable 'fps', default value is 25fps.
    This function is the inverse of timeCode2frameCount.
    
    >>> import Timecode
    
    >>> Timecode.frameCount2timeCode (0, 25)
    '00:00:00:00'
    
    >>> Timecode.frameCount2timeCode (1, 25)
    '00:00:00:01'
    
    >>> Timecode.frameCount2timeCode (25, 25)
    '00:00:01:00'
    
    >>> Timecode.frameCount2timeCode (24, 24)
    '00:00:01:00'
    
    >>> Timecode.frameCount2timeCode (2159999, 25)
    '23:59:59:24'
    
    >>> Timecode.frameCount2timeCode (2073599, 24)
    '23:59:59:23'
    
    """
    HH, MM, SS, FF = frameCount2timeCodeElements (frames, fps)
    return (string.zfill (HH, 2) + ":" + string.zfill (MM, 2) + ":"\
             + string.zfill (SS, 2) + ":" + string.zfill (FF, 2))


def frames2timeCodeElements (frames, fps = DEFAULT_FPS_VALUE):
    """
    Convert frames to separate timecode elements HH MM SS and FF
    
    >>> import Timecode
    >>> Timecode.frames2timeCodeElements (0)    
    Traceback (most recent call last):
    FrameConversionError: Invalid frame, frames must be 1 and larger

    >>> Timecode.frames2timeCodeElements (1)    
    (0, 0, 0, 0)
    
    """
    assert_valid_frame_rate (fps)
    if frames <= 0:
        raise FrameConversionError, "Invalid frame, frames must be 1 and larger"
    
    frames = frames - 1
    
    FF = frames % fps
    frames = frames - FF
    SS = (frames / fps) % 60
    frames = frames - (SS * fps)
    MM = (frames / (fps * 60)) % 60
    frames = frames - (MM * fps * 60)
    HH = (frames / (fps * 60 * 60)) % 24
    
    return HH, MM, SS, FF

# For backwards competability    
frames2tc = frames2timeCodeElements


def frameCount2timeCodeNumber (frames, fps = DEFAULT_FPS_VALUE):
    """
    frameCount2timeCodeNumber (timecode, fps)
    
    Convert a (absolute) framecount to a timecode integer. Provide fps in variable 'fps', default value is 25fps.
    """
    assert_valid_frame_rate (fps)
    HH, MM, SS, FF = frames2tc (frames, fps)
    return (string.zfill (HH, 2) + string.zfill (MM, 2) + string.zfill (SS, 2) + string.zfill (FF, 2))

def timeCodeMinus (tc_1, tc_2, fps = DEFAULT_FPS_VALUE):
    assert_valid_frame_rate (fps)
    return (frameCount2timeCode (timeCode2frameCount (tc_1, fps) - timeCode2frameCount (tc_2, fps), fps))

def timeCodeAdd (tc_1, tc_2, fps = DEFAULT_FPS_VALUE):
    assert_valid_frame_rate (fps)
    return (frameCount2timeCode (timeCode2frameCount (tc_1, fps) + timeCode2frameCount (tc_2, fps), fps))

def timeCodeAddFrames (tc_1, frames, fps = DEFAULT_FPS_VALUE):
    """
    Add number of frames to a timecode
    """
    assert_valid_frame_rate (fps)
    return (frameCount2timeCode (timeCode2frameCount (tc_1, fps) + frames, fps))
    
def timeCodeCompare (tc_1, tc_2, fps = DEFAULT_FPS_VALUE):
    """
    Compares the two timecodes.
    Returns 0 if they are equal
           -1 if tc_1 < tc_2
            1 if tc_1 > tc_2
    """
    assert_valid_frame_rate (fps)
    t1 = timeCode2frameCount (tc_1, fps)
    t2 = timeCode2frameCount (tc_2, fps)
    if t1 == t2:
        return (0)
    elif t1 < t2:
        return (-1)
    elif t1 > t2:
        return (1)

def timeCodeLargerThen (tc_1, tc_2, fps = DEFAULT_FPS_VALUE):
    """
    Returns true if tc_1 is larger then tc_2
    """
    assert_valid_frame_rate (fps)
    t1 = timeCode2frameCount (tc_1, fps)
    t2 = timeCode2frameCount (tc_2, fps)
    if t1 > t2:
        return (1)
    else:
        return (0)	

def timeCodeIsEqual (tc_1, tc_2, fps = DEFAULT_FPS_VALUE):
    """
    Returns true if tc_1 is equal to tc_2
    """
    assert_valid_frame_rate (fps)
    t1 = timeCode2frameCount (tc_1, fps)
    t2 = timeCode2frameCount (tc_2, fps)
    if t1 == t2:
        return (1)
    else:
        return (0)

def timeCodeSmallerThen (tc_1, tc_2, fps = DEFAULT_FPS_VALUE):
    """
    Returns true if tc_1 is smaller then tc_2
    """
    assert_valid_frame_rate (fps)
    t1 = timeCode2frameCount (tc_1, fps)
    t2 = timeCode2frameCount (tc_2, fps)
    if t1 < t2:
        return (1)
    else:
        return (0)	

def timeCodeIsInbetween (tc, tc_in, tc_out, fps=DEFAULT_FPS_VALUE):
    """
    Return true if tc is in between the tc_in and tc_out value
    """
    assert_valid_frame_rate (fps)
    compare_to_in = timeCodeCompare (tc, tc_in, fps=DEFAULT_FPS_VALUE)
    
    # If tc is smaller than tc_in - return fals right away
    if compare_to_in == -1:
        return False
    
    compare_to_out = timeCodeCompare (tc, tc_out, fps=DEFAULT_FPS_VALUE)
    
    # If tc is larger than tc_out - return false as well
    if compare_to_out == 1:
        return False
        
    return True

def timeCodeDuration (tc_1, tc_2, fps=DEFAULT_FPS_VALUE):
    """
    Return the duration as a timecode string
    """
    assert_valid_frame_rate (fps)
    if (timeCodeCompare (tc_1, tc_2, fps) > 0):
        t = tc_1
        tc_1 = tc_2
        tc_2 = t
    return frameCount2timeCode (timeCode2frameCount (tc_2, fps) - timeCode2frameCount (tc_1, fps))

timeCodeDifference = timeCodeDuration

def frameCountDuration (tc_1, tc_2, fps=DEFAULT_FPS_VALUE):
    """
    Return the duration in framecount
    """
    assert_valid_frame_rate (fps)
    if (timeCodeCompare (tc_1, tc_2, fps) > 0):
        t = tc_1
        tc_1 = tc_2
        tc_2 = t
    return timeCode2frameCount (tc_2, fps) - timeCode2frameCount (tc_1, fps)


#
#  Part 2
#
class Timecode (object):
    """
    Base timecode value
    
    >>> Timecode ()
    <Timecode.Timecode object at 0x...>
    
    """
    def __init__ (self, inittype=INIT_TYPES.NOINIT, initvalue=0, fps=DEFAULT_FPS_VALUE):
        """"
        """
        assert_valid_frame_rate (fps)
        self.fps = fps
        if inittype == INIT_TYPES.NOINIT:
            self._init_with_framecount (0)
        elif inittype == INIT_TYPES.FRAMECOUNT:
            self._init_with_framecount (initvalue)
        elif inittype == INIT_TYPES.TIMECODE:
            timecode_string = self._prepareTCString (timecode_string)
            self._setTCFromString (timecode_string)
            self.framecount = timeCode2frameCount (timecode_string, self.fps)

    def _init_with_framecount (self, framecount):
        assert_valid_framecount (framecount, self.fps)
        self.framecount = framecount
        self.HH, self.MM, self.SS, self.FF = frameCount2timeCodeElements (framecount, self.fps)
    
    def _prepareTCString (self, timecode_string):
        """
        There are three ways to in
        Parse a string into timecode values
        Be relaxed on the format - can be anything from
        - frames,
        - frames and seconds,
        - frames and seconds and minutes,
        - or all,
        
        As for the separator sign; can be either " " (space), ".", ";" or ":"
        """
        timecode_string = string.replace (timecode_string, ";", ":")
        timecode_string = string.replace (timecode_string, ".", ":")
        return string.replace (timecode_string, " ", ":")
        
    def _setTCFromString (self, timecode_string=""):
        e =  timecode_string.split (":")
        s = len(e)
        
        if not timecode_string == "":
            self.FF = string.atoi (e[s-1])
        else:
            self.FF = 0
            
        if s > 1:
            self.SS = string.atoi (e[s-2])
        else:
            self.SS = 0
        
        if s > 2:
            self.MM = string.atoi (e[s-3])
        else:
            self.MM = 0
        
        if s > 3:
            self.HH = string.atoi (e[s-4])
        else:
            self.HH = 0
    
    def addFrames (self, frames):
        """
        Add number of frames to this timecode
        """
        timecode_string = frameCount2timeCode (timeCode2frameCount (self.asString (), self.fps) + frames, self.fps)
        self._setTCFromString (timecode_string)

    def asString (self, separator=":"):
        return separator.join (( string.zfill (self.HH, 2), 
                                 string.zfill (self.MM, 2), 
                                 string.zfill (self.SS, 2),
                                 string.zfill (self.FF, 2)
                               ))
    
    def asFrameCount (self):
        # Frame count = (hours * 60 * 60 + minutes * 60 + seconds) * fps + frames
        return ((self.HH*60*60 + self.MM * 60 + self.SS) * self.fps + self.FF)


#
#  Part 3
#  Main runs the doctests
#
if __name__ == "__main__":
    print '**running standard doctest'
    import doctest, Timecode
    doctest.testmod(Timecode, verbose=True, optionflags=doctest.ELLIPSIS)

