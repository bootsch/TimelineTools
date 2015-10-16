# file : edlClasses.py
#
# This file defines an EDL Class and some other used subclasses
# Written for use with Minoes by Bos Bros.
#
# The above is the original line when writing this module back in 2001 for the VFX pipeline
# It contains a more or less general usable edl set but it contains plenty of free exentsion to the edl concept
# generally not used by standard software applications such as Avid, Final Cut, Premiere, daVinci Resolve and other
# high end grading software.
#
# More or less general since it's really bad on the speeds and effects side of edl's and audio was completely ignored
# when writing the module and has never been required over the years it's been used in other production pipelines.
#
# Allthough I long had the intention to put it into the public domain it just never happened until this year
# a student production desperately could use it's function to build their own edit update tools to daily deliver an
# updated timeline of their film
#
# 
#
# Author: Paul Boots
# Copyright 2001 - 2015


import os, string, re, Timecode

debug = 1

# Some globals used with these classes; mainly for printing
tab     = "\t"
# Only the unix style is used for output - it should be possible to read any style edl
newline = "\n"
#newline = os.linesep
space   = " "
space2  = "  "
space3  = "   "

TRUE   = 1
FALSE  = 0
TR_RECORD = {'tape_no': '', 'reel_no': ''}

# Change 'unstorables', characters that don't work with most filesystem
def changeUnstorables (thestring):
    # Change "\" to "/"
    # Change "/" to "_"
    # Change " " to "-"
    return string.replace (string.replace (string.replace (thestring, '\\', '/'), '/', '_'), ' ', '-')
	
# Sort Function to sort on events by event id
def sortByEvent (event_1, event_2):
	if event_1.getEventID () == event_2.getEventID ():
		if event_1.getRecordOut () < event_2.getRecordIn ():
			result = -1
		elif event_1.getRecordIn () > event_2.getRecordOut ():
			result = 1
		elif event_1.getRecordIn () == event_2.getRecordOut ():
			result = 0
	elif event_1.getEventID () < event_2.getEventID ():
		result =  -1
	elif event_1.getEventID () > event_2.getEventID ():
		result =  1
		
	return result

# Sort Function to sort on events by reel id
def sortByReel (event_1, event_2):
	if event_1.getReelNumber () == event_2.getReelNumber ():
		if event_1.getSourceOut () < event_2.getSourceIn ():
			result = -1
		elif event_1.getSourceIn () > event_2.getSourceOut ():
			result = 1
		else:
			result = 0
	elif event_1.getReelNumber () < event_2.getReelNumber ():
		result =  -1
	elif event_1.getReelNumber () > event_2.getReelNumber ():
		result =  1
		
	return result

# Class to hold an EDL Event
class AN_EDL_EVENT:
    """
    Class defintion for an edl event found in edl's
    """
    def __init__(self, event_id, tape_id, eventType, cutType, \
                    si = "", so = "", ri = "", ro = "", cn = "", scn = "", shn = "", shi = "", ln = "", sn = "", reel_id=""):
        self.event_id    = event_id		# Event number - unique in EDL (NOT)
        self.reel_id     = tape_id		# Reel containing online material
        self.tape_id     = tape_id		# Reel containing online material
        self.eventType   = eventType	# Type of event: v(ideo)/a(udio)/bl(ack)
        self.cutType     = cutType		# Type of cut: c(ut):d(issolve) etc.
        self.source_in   = si			# Source timecode inpoint
        self.source_out  = so			# Source timecode outpoint
        self.record_in   = ri			# Record timecode inpoint
        self.record_out  = ro			# Record timecode outpoint
        self.clipName    = cn			# Clipname for this event
        self.keyClipName  = cn          # Clipname used in key
        self.fromClipName = ""
        self.toClipName = ""
        self.isEffectElement = False    # Is this event part of a video effect: dissolve, wipe
        self.effectDuration = 0         # Duration of the effect in frames
        self.hasSpeedChange = False     # Does this event have a speed change
        self.newFPS = 0.0               # The FPS for the new speed
        self.sceneNumber = scn			# Scene number
        self.shotNumber  = shn
        self.shotInstance = shi
        self.layerNumber = ln
        self.slateNumber = sn			# Slate number as used in clip id
        self.takeNumber  = ""	        # Take number as used in clip id
        self.blackevent  = False
        self.duration = ""
        self.commentList = list ()      #  List of comments for this event

    def getEventID (self):
        return (self.event_id)
        
    def setClipName (self, cn):
        self.clipName = cn
        
    def getClipName (self, format="original"):
        if format == "original":
            return (self.clipName)
        elif format == "filesystem":
            return changeUnstorables (self.clipName)
    
    def setKeyClipName (self, cn):
        self.keyClipName = cn
        
    def getKeyClipName (self, format="original"):
        if format == "original":
            return (self.keyClipName)
        elif format == "filesystem":
            return changeUnstorables (self.keyClipName)

    def setFromClipName (self, cn):
        self.fromClipName = cn

    def getFromClipName (self, format="original"):
        if format == "original":
            return (self.fromClipName)
        elif format == "filesystem":
            return changeUnstorables (self.fromClipName)
    
    def setToClipName (self, cn):
        self.toClipName = cn
        
    def getToClipName (self, format="original"):
        if format == "original":
            return (self.toClipName)
        elif format == "filesystem":
            return changeUnstorables (self.toClipName)
                
    def setSceneNumber (self, sn):
        self.sceneNumber = sn

    def getSceneNumber (self):
        return (self.sceneNumber)

    def setShotNumber (self, sn):
        self.shotNumber = sn

    def getShotNumber (self):
        return (self.shotNumber)

    def setShotInstance (self, si):
        self.shotInstance = si

    def getShotInstance (self):
        return (self.shotInstance)

    def setLayerNumber (self, sn):
        self.layerNumber = sn

    def getLayerNumber (self):
        return (self.layerNumber)

    def setSlateNumber (self, sn):
        self.slateNumber = sn

    def getSlateNumber (self):
        return (self.slateNumber)

    def setTakeNumber (self, tn):
        self.takeNumber = tn

    def getTakeNumber (self):
        return (self.takeNumber)

    def setTapeNumber (self, number):
        self.tape_id = number

    def getTapeNumber (self):
        return self.tape_id

    def setReelNumber (self, number):
        self.reel_id = number

    def getReelNumber (self):
        return self.reel_id

    def getSourceIn (self):
        return (self.source_in)
        
    def getSourceOut (self):
        return (self.source_out)
        
    def setSourceOut (self, source_out):
        self.source_out = source_out
        
    def getRecordIn (self):
        return (self.record_in)
        
    def getRecordOut (self):
        return (self.record_out)
        
    def addCommentLine (self, commentline):
        self.commentList.append (commentline)

    def getCommentList (self):
        return (self.commentList)

    def shiftTimeCode (self, shiftAmount, sourceOrRecord):
        if sourceOrRecord == "source":
            self.source_in = Timecode.frameCount2timeCode (Timecode.timeCode2frameCount(self.source_in) + shiftAmount)
            self.source_out = Timecode.frameCount2timeCode (Timecode.timeCode2frameCount(self.source_out) + shiftAmount)
        elif sourceOrRecord == "record":
            self.record_in = Timecode.frameCount2timeCode (Timecode.timeCode2frameCount(self.record_in) + shiftAmount)
            self.record_out = Timecode.frameCount2timeCode (Timecode.timeCode2frameCount(self.record_out) + shiftAmount)
            
    def addHeadsAndTails (self, handleLenght, sourceOrRecord):
        if sourceOrRecord == "source":
            self.source_in = Timecode.frameCount2timeCode (Timecode.timeCode2frameCount(self.source_in) - handleLenght)
            self.source_out = Timecode.frameCount2timeCode (Timecode.timeCode2frameCount(self.source_out) + handleLenght)
        elif sourceOrRecord == "record":
            self.record_in = Timecode.frameCount2timeCode (Timecode.timeCode2frameCount(self.record_in) - handleLenght)
            self.record_out = Timecode.frameCount2timeCode (Timecode.timeCode2frameCount(self.record_out) + handleLenght)
            
    def renumber (self, newEventNumber):
        self.event_id = newEventNumber

    def printAsString (self):
        # print event as string
        print self.event_id + space2 + self.reel_id, "  ",self.eventType, "   ",self.cutType, "      ", self.source_in, self.source_out, self.record_in, self.record_out
        print "* FROM CLIP NAME: ", self.slateNumber + "/" + self.takeNumber

    def getTabSeparatedRecord (self):
        # return tab separated record
        theLine = self.event_id + "\t" + self.reel_id + "\t" + self.eventType
        theLine = theLine + "\t" + self.cutType + "\t"
        theLine = theLine + self.source_in + "\t" + self.source_out + "\t"
        theLine = theLine + self.record_in + "\t" + self.record_out + "\t"
        theLine = theLine + self.slateNumber + "\t" + self.takeNumber + "\t"
        theLine = theLine + str(Timecode.timeCode2frameCount(self.record_out) - Timecode.timeCode2frameCount(self.record_in)) + newline
        return (theLine)

    def getGrassValleyRecord (self):
        # return tab separated record
        theLine = self.event_id + " " + self.reel_id + "    " + \
                  self.eventType + "      " + self.cutType + "        " + \
                  self.source_in + " " + self.source_out + "  " + \
                          self.record_in + " " + self.record_out + newline
        theLine = theLine + "* FROM CLIP NAME:  " + self.slateNumber + "/" + self.takeNumber + newline
        return (theLine)

    def getCMXRecord (self, a1 = 0, a2 = 0):
        # return tab separated record
        theLine = string.zfill (string.atoi (self.event_id), 3) + "  " + string.ljust (self.reel_id, 2) + "    "
        event = ""
        if a1:
            event = "A"
        if a2:
            event = event + "A"
        if event != "":
            event = event + "/"
        
        event = event + self.eventType
        
        theLine = theLine + string.ljust(event, 3)
        theLine = theLine + "   " + self.cutType + "    "
        if (self.duration != ""):
            theLine = theLine + self.duration + " "
        else:
            theLine = theLine + "    "
            
        theLine = theLine + self.source_in + " " + self.source_out + " " + \
                            self.record_in + " " + self.record_out + newline
        if self.reel_id != "BL" and self.reel_id != "AX" and self.blackevent != 1:
            if self.slateNumber != "":
                theLine = theLine + "* FROM CLIP NAME:  " + self.slateNumber
                if self.takeNumber:
                    theLine = theLine + "/" + string.strip (self.takeNumber)
            #theLine = theLine + newline
        for comment in self.commentList:
            if comment != "" and comment != newline:
                theLine = theLine + string.strip (comment) + newline
        
            
        return (theLine)
        
    def getBlackEvent (self, event_id, recordIn, recordOut, duration = 25, gvg = 0):
        if gvg:
            pad = 4
        else:
            pad = 3
        theLine = string.zfill (event_id, pad) + "  BL    V     C        " 
        theLine = theLine + "00:00:00:00 00:00:02:00 " + recordIn + " " + recordOut + newline
        return (theLine)

		
# Class to hold "Source Reel" identifier
class A_EDL_SOURCE_ID:
	def __init__(self, reelDataList):
		self.reel_1   = ""	# First reelnumber
		self.reel_2   = ""	# Second reelnumber
		self.reelCode = ""	# Code found at end of source line (?) An Avid thing?

		i = 0
		l = len (reelDataList)
		#print "lenght of list:", l
		while i < l:
			#print "i=", i
			if i == 2:
				self.reel_1 = reelDataList [i]
			elif i == 3:
				self.reel_2 = reelDataList [i]				
			elif i == 4:
				self.reelCode = reelDataList [i]
			i = i + 1
		
	def printAsString (self):
		print ">>> SOURCE", self.reel_1, "  ", self.reel_2, "          ", self.reelCode 
		return ("")

	def getAsString (self):
		return (">>> SOURCE " + self.reel_1 + "  " + self.reel_2 + "          " + self.reelCode + newline)

# 


# Class for an EDL
class AN_EDL:
    """
    Ad EDL class that allows you to work with edl in python.
    """
    def __init__(self, name, title):
        self.name  = name
        self.title = title
        self.fcm = ""           # Signifies drop or non-dropframe
        self.fps = 24           # Edl frames frames per second
        self.total_events = 0
        self.header = []
        self.eventList = list ("")
        self.sourceReelList = list ("")
        self.tapeList = []
        self.reelList = []
        self.clipList = []
        self.state = "raw" # State can be 'raw' - ''
    
    def initFromFile (self, edlfilename):
        """
        edlfilename: the full path to an edl file
        
        Init this edl object from the given edl file
        Long overdue making the EDL class finally pytonic after all these years
        Cheating a bit because for now we will just use the module methods :-)
        """
        self.name = edlfilename
        edlfile = open (edlfilename)
        parseEDL2object2 (edlfile, edlfilename, edlobject = self)
        parseRawEDL2 (self)
    
    def getEvents (self):
        return (self.eventList)

    def getEventsByReel (self):
        self.eventList.sort (sortByReel)
        return (self.eventList)
        
    def getEvent (self, id):
        a = self.getEvents ()
        for event in a:
            if string.atoi (event.getEventID ()) == id:
                return event
                
    def getTotalEvents (self):
        return (self.total_events)
        
    def getSourceReels (self):
        return (self.sourceReelList)
        
    def printAsString (self):
        # format gives the type of edl
        print "TITLE:  ", self.title
        print "* spit out by an edl object. PB hackware"
        for event in self.eventList:
            event.printAsString ()
        for sourcereel in self.sourceReelList:
            sourcereel.printAsString ()
        return ()
        
    def getAsString (self):
        # format gives the type of edl
        edlString = "TITLE:  " + self.title + newline
        edlString = edlString + newline
        edlString = edlString + newline.join (self.header)
        for event in self.eventList:
            edlString = edlString + event.getCMXRecord ()
            
        for sourcereel in self.sourceReelList:
            edlString = edlString + sourcereel.getAsString ()

        return (edlString)
        
    def getTapeList (self):
        """
        Get a list of unique tape numbers - not Aux sources
        """
        if (self.tapeList == []):
            for event in self.getEvents ():
                tn = event.getTapeNumber ()
                
                #if re.match (r'\d\d\d', tn):
                if (tn not in self.tapeList):
                    self.tapeList.append (tn)
                    
        return self.tapeList

    def getReelList (self):
        """
        Get a list of unique reel numbers - not Aux sources
        """
        if (self.reelList == []):
            for event in self.getEvents ():
                tn = event.getReelNumber ()
                if re.match (r'\d\d\d', tn):
                    if (tn not in self.reelList):
                        self.reelList.append (tn)

        self.reelList.sort ()			
        return self.reelList

    def getClipList (self):
        """
        Get a list of unique clipnames - not Aux sources
        """
        if (self.clipList == []):
            for event in self.getEvents ():
                tn = event.getClipName ()
                if (tn not in self.clipList):
                    self.clipList.append (tn)
        
        self.clipList.sort ()
        return self.clipList


# actual parsing
def parseEDL2object (edl_file, filename, shiftEventCount = 0, fillGaps = TRUE, gvg = 0, edlobject = None):
    """
    parseEDL2object
    """
    l = edl_file.readline ()
    firstline  = TRUE
    firstevent = TRUE
    eventindex = 0
    lastEvent  = 0
    lastRecOut = 0
    step = 0
    ne = ""
    le = ""

    lookfor = r'\d\d\d'
    if gvg == 1:
        lookfor = r'\d\d\d\d'
        
    while l != "":
        # Check for leading carriage return
        if re.match (r'\r',l):
            l = re.sub (r'\r', '', l)
            if debug > 3:
                print "Carriage return at start of line! My god. Stripped now."

        # Look for TITLE: first
        if firstline == TRUE:
            ls = string.split (l, ':', 2)
            if ls[0] != "TITLE":
                check = re.findall (r'\s', l)
                if debug > 2:
                    print "Check =", check, "lenght =", len(check)
                if len (check) > 0:
                    l = edl_file.readline ()
                    continue

            if edlobject:
                edl = edlobject
                edl.title = string.strip (ls[1])
            else:
                edl = AN_EDL (filename, string.strip (ls[1]))
            edl.total_events = 0
            #print "New EDL instanced. Filename:", edl.name, "Title:", edl.title
            firstline = FALSE
            
        if firstline == FALSE:
            if debug > 3:
                print string.strip(l)
                
            ls = string.split (l)
            
            # First look for an event number
            if re.match (lookfor, l):

                if ls[0] == lastEvent:
                    continuedEvent = 1
                else:
                    continuedEvent = 0
                    lastEvent = ls[0]
                
                # Apr. 2004 - Leave event number untouched now
                if continuedEvent:
                    nn = string.atoi(lastEvent)
                    # nn = string.atoi(lastEvent) + shiftEventCount
                else:
                    nn = string.atoi(ls[0]) + shiftEventCount
                    edl.total_events = edl.total_events + 1
                
                if debug > 3:
                    print "Original number:", string.atoi(ls[0]),"Converted number:", nn
                    
                ne = AN_EDL_EVENT (string.zfill(nn, 3), ls[1], ls[2], ls[3])
                le = ""
                
                if ls[1] == "BL":
                    ne.blackevent = 1
                else:
                    ne.blackevent = 0
                if ls[3] == "D":
                    if debug > 2:
                        print "Found dissolve"
                    ne.duration = ls[4]
                    indexShift = 1
                elif ls[3] == "K":
                    indexShift = 1
                else:
                    indexShift = 0
                
                ne.source_in  = ls[4 + indexShift]	# Source timecode inpoint
                ne.source_out = ls[5 + indexShift]	# Source timecode outpoint
                ne.record_in  = ls[6 + indexShift]	# Record timecode inpoint
                ne.record_out = ls[7 + indexShift]	# Record timecode outpoint
                
                if debug > 3:
                    print "Source In: %s Out: %s   Record In: %s Out:%s" % (ne.source_in, ne.source_out, ne.record_in, ne.record_out)
                edl.eventList.append (ne)
                
                # Compare Last record out and new record out
                # For a regular cut the should be equal
                # If the Last out point is before the current one we have a gap
                # If the Last out is later - we have overlap and will need to trim
                if debug > 3:
                    print "Check last and new record out...",ls[6 + indexShift], lastRecOut
                if firstevent == FALSE:
                    # compare last record out to record in for gaps
                    if Timecode.timeCodeCompare (ls[6 + indexShift], lastRecOut) != 0:
                        # Insert additional in/out for black event
                        # Take last record out for new rec. in and current
                        # record in for new rec. out.
                        # and don't forget to riple the event count
                        if debug > 3:
                            print "Found time gap in record timecode"
                
                lastRecOut = ls[7 + indexShift]
                    
                if firstevent:
                    firstevent = FALSE
                
                eventindex = eventindex + 1
                ne = ""

            # Look for a comment line
            elif re.match (r'\* ', l):
                # True if we found a comment
                if debug > 2:
                    print "Eventindex: %s" % eventindex
                ei = eventindex - 1
                edl.eventList [ei].addCommentLine (l)

            elif re.match (r'>>> SOURCE', l):
                sourcereel = A_EDL_SOURCE_ID (ls)
                edl.sourceReelList.append (sourcereel)
                if debug > 3:
                    print "Found source reel line", sourcereel.reel_1, sourcereel.reel_2, sourcereel.reelCode
            
            else:
                try:
                    if (le ==""):
                        le = eventindex - 1
                        
                    edl.eventList [le].commentList.append (l)
                    
                except:
                    pass
                    
        l = edl_file.readline ()
    else:
        pass
        #print "done"

    return (edl)
	

# New version of edl parsing
def parseEDL2object2 (edl_file, filename, shiftEventCount = 0, fillGaps = False, gvg = 0, edlobject = None):
    """
    parseEDL2object
    """
    
    # Keep track of position in file before each readline
    last_line = 0
    stop = False
    
    new_event = None
    last_event = None
    
    # Keep track of lowest and highest record time codes
    lowestRecordTC = None
    highestRecordTC = None
    
    firstline  = TRUE
    firstevent = TRUE
    eventindex = 0
    #lastEvent  = 0
    last_event = AN_EDL_EVENT (None, None, None, None)

    lastRecOut = 0
    step = 0
    ne = ""
    le = ""

    #print "debug: %s" % debug
    
    lookfor = r'\d\d\d'
    if gvg == 1:
        lookfor = r'\d\d\d\d'
    
    # Create an empty edl
    if edlobject:
        edl = edlobject
    else:
        edl = AN_EDL (filename, "")
    
    # Read the header, title and whatever upto first event number
    while not stop:
        last_line = edl_file.tell ()
        l = edl_file.readline ().strip ()
        if l.startswith ("TITLE:"):
            junk, essence = l.split (":")
            edl.title = essence.strip ()
        elif l.startswith ("FCM:"):
            junk, essence = l.split (":")
            edl.fcm = essence.strip ()
        elif re.match (lookfor, l):
            # found event number - quit parsing header
            edl_file.seek (last_line)
            stop = True
        else:
            # Addition comments/text in header before first event
            edl.header.append (l.strip ())

    #return edl
    stop = False
    # Read the edl body
    while not stop:
            
        last_line = edl_file.tell ()
        l = edl_file.readline ()
        
        if l == '':
            break
        else:
            l = l.strip()
        
        # First look for an event number
        if re.match (lookfor, l):

            # We found an event - process this event line
            # Split the line into separate elements
            ls = l.split ()
                            
            ne = AN_EDL_EVENT (ls[0], ls[1], ls[2], ls[3])
            le = ""
            
            # Check for blackevents
            if ls[1] == "BL":
                ne.blackevent = True
            else:
                ne.blackevent = False
            if ls[3] == "D":
                if debug > 2:
                    print "Found dissolve"
                ne.duration = ls[4]
                ne.isEffectElement = True
                ne.effectDuration = int(ls[4])
                indexShift = 1
            elif ls[3].startswith ("W"):
                if debug > 2:
                    print "Found wipe"
                ne.duration = ls[4]
                ne.isEffectElement = True
                ne.effectDuration = int(ls[4])
                indexShift = 1
            elif ls[3] == "K":
                indexShift = 1
            else:
                indexShift = 0
            
            ne.source_in  = ls[4 + indexShift]	# Source timecode inpoint
            ne.source_out = ls[5 + indexShift]	# Source timecode outpoint
            ne.record_in  = ls[6 + indexShift]	# Record timecode inpoint
            ne.record_out = ls[7 + indexShift]	# Record timecode outpoint
            
            if debug > 3:
                print "Source In: %s Out: %s   Record In: %s Out:%s" % (ne.source_in, ne.source_out, ne.record_in, ne.record_out)
            edl.eventList.append (ne)
            
            # Compare Last record out and new record out
            # For a regular cut the should be equal
            # If the Last out point is before the current one we have a gap
            # If the Last out is later - we have overlap and will need to trim
            if debug > 3:
                print "Check last and new record out...",ls[6 + indexShift], lastRecOut
            if firstevent == FALSE:
                # compare last record out to record in for gaps
                if Timecode.timeCodeCompare (ls[6 + indexShift], lastRecOut) != 0:
                    # Insert additional in/out for black event
                    # Take last record out for new rec. in and current
                    # record in for new rec. out.
                    # and don't forget to riple the event count
                    if debug > 3:
                        print "Found time gap in record timecode"
            
            lastRecOut = ls[7 + indexShift]
                
            if firstevent:
                firstevent = FALSE
            
            # Point last event to the just created and filled event object
            last_event = ne
            # By using the event object itself, the event index becomes obsolete
            eventindex = eventindex + 1
            ne = ""

        # Look for a motion effect line
        elif re.match (r'\M2 ', l):
            # True if we found a comment
            if debug > 2:
                print "Found Motion effect"
            last_event.hasSpeedChange = True
            last_event.newFPS = float (l.split ()[2])
            
        # Look for a comment line
        elif re.match (r'\* ', l):
            # True if we found a comment
            if debug > 2:
                print "Eventindex: %s" % eventindex
            ei = eventindex - 1
            edl.eventList [ei].addCommentLine (l)

        elif re.match (r'>>> SOURCE', l):
            sourcereel = A_EDL_SOURCE_ID (ls)
            edl.sourceReelList.append (sourcereel)
            if debug > 3:
                print "Found source reel line", sourcereel.reel_1, sourcereel.reel_2, sourcereel.reelCode
        
        else:
            try:
                if (le ==""):
                    le = eventindex - 1
                    
                edl.eventList [le].commentList.append (l)
                
            except:
                pass
                

    return (edl)
	

def parseRawEDL (edl):
    """
    Parse a 'raw' EDL object - probably right after creating the object from an edl file
    It store clipname and keyclip name data in the eventobjects
    """
    for event in edl.eventList:
        for comment in event.commentList:
            # Check if we have the clipname
            if re.match (r'\* FROM CLIP', comment):
                # Get the clipname part
                cn = string.strip (string.split (comment, ':') [1])
                event.setClipName (cn)
            # Check if we have the key clip name, with more info
            if re.match (r'\* KEY CLIP NAME', comment):
                # Get the name part seperated by a ':'
                cn = string.strip (string.split (comment, ':') [1])
                event.setKeyClipName (cn)
    """
    l = len (edl.eventList)
    for i in range (l):
        event = edl.eventList [i]
        try:
            next_event = edl.eventList [i + 1]
        except:
            next_event = None

        if (next_event):
            if (event.event_id == next_event.event_id):
                event.setClipName (next_event.clipName)
                event.setKeyClipName (next_event.keyClipName)
    """
    

def parseRawEDL2 (edl):
    """
    Another version of parsing a 'raw' EDL object. The edl must be sorted by event for
    this to work correctly.
    It store clipname and keyclip name data in the eventobjects
    """
    last_event_index = -1
    
    from_clip = None
    to_clip = None
    key_clip = None
    
    l = len (edl.eventList)
    for i in range (l):
    #for event in edl.eventList:

        event = edl.eventList [i]
        if last_event_index != -1 and last_event_index < l:
            last_event = edl.eventList [last_event_index]
        else:
            last_event = AN_EDL_EVENT (None, None, None, None)
        
        if debug > 3:
            print "process event: %s - id in list: %s" % (event.getEventID(), edl.eventList[i].getEventID())
            print event.printAsString ()
        for comment in event.commentList:
            # Check if we have the clipname
            if re.match (r'\* FROM CLIP NAME', comment):
                # Get the clipname part
                from_clip = string.strip (string.split (comment, ':') [1])
            if re.match (r'\* TO CLIP NAME', comment):
                # Get the clipname part
                to_clip = string.strip (string.split (comment, ':') [1])
            # Check if we have the key clip name, with more info
            if re.match (r'\* KEY CLIP NAME', comment):
                # Get the name part seperated by a ':'
                key_clip = string.strip (string.split (comment, ':') [1])
            
        if event.cutType != "C":
            # Check for a black event - which doesn't need a clipname
            if not event.blackevent:
                # Set the to 'to clip' to use as clipname for this event
                if to_clip:
                    event.setClipName (to_clip)
                    event.setToClipName (to_clip)
                else:
                    print "Warning: event %s has no 'to clip' to use in comment list %s" % (event.event_id, event.commentList)

            if event.event_id == last_event.event_id:
                # Check for a black event - which doesn't need a clipname
                if not last_event.blackevent:
                    if from_clip:
                        # Set the 'from clip' to use as clipname for the last event
                        last_event.setClipName (from_clip)
                        # Compute correct source out for the last event based on effect duration
                        if debug > 3:
                            print "Source out original: %s" % last_event.getSourceOut ()
                        source_out = Timecode.timeCodeAddFrames (last_event.getSourceOut (), event.effectDuration, fps=edl.fps)
                        last_event.setSourceOut (source_out)
                        # Set the 'from clip' for the current event
                        event.setFromClipName (from_clip)
                    else:
                        print "Warning: event %s has no 'from clip' to use in comment list %s" % (event.event_id, event.commentList)
                    
        else:
            # We have a regular cut event
            if from_clip:
                # Set the 'from clip' to use as clipname
                event.setClipName (from_clip)
            else:
                print "Warning: event %s has no 'from clip' to use in comment list %s" % (event.event_id, event.commentList)
                
        # Set processed event to be last_event
        last_event_index += 1
            
"""
ci = string.split (string.split (cn)[0], '/')

if (len (ci) == 3):
	try:
		edl.eventList [ei].setTakeNumber  (ci[2])
	except:
		print "no go setTakeNumber"
		edl.eventList [ei].setTakeNumber  ("")
if (len (ci) > 2):
	try:
		edl.eventList [ei].setSlateNumber (ci[1])
	except:
		print "no go setSlate from:", ci
		edl.eventList [ei].setSlateNumber ("N/A")

try:
	edl.eventList [ei].setSceneNumber (ci[0])
except:
	print "no go setSlate from:", ci
	edl.eventList [ei].setSceneNumber ("N/A")

if debug > 2:
	print "scene: %s, slate: %s, take: %s" % (edl.eventList [ei].getSceneNumber (), edl.eventList [ei].getSlateNumber (),edl.eventList [ei].getTakeNumber ())
"""
			
"""
# Check if we have the key clip name, with more info
if re.match (r'\* KEY CLIP NAME', l):
	# Get the name part seperated by a ':'
	cn = string.strip (string.split (l, ':') [1])
	ci = string.split (cn)
	
	print "ci: %s" % ci
	# Try to get the layer info from the shot id
	try:
		edl.eventList [ei].setLayerNumber (ci [2])
	except:
		edl.eventList [ei].setLayerNumber ("N/A")
		if debug > 2:
			print "no go setLayerNumber from:", ci
	
	# See if there is additional shot instance data in the shot id
	try:
		tci = string.split (ci[1], "/")
	except:
		tci = (ci[1])
		
	if (len (tci) > 1):
		edl.eventList [ei].setShotInstance (tci [1])
	else:
		edl.eventList [ei].setShotInstance (1)
	
	edl.eventList [ei].setShotNumber (tci[0])
	if debug > 2:
		print "event: %s; shot id: %s;" % (ei, edl.eventList [ei].shotNumber)
"""
	
