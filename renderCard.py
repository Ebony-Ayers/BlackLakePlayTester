LINE_HORIZONTAL = ["─", "━", "═"]
LINE_VERTICAL = ["│", "┃", "║"]
CORNER_TOP_LEFT = ["┌", "┏", "╔"]
CORNER_TOP_RIGHT = ["┐", "┓", "╗"]
CORNER_BOTTOM_LEFT = ["└", "┗", "╚"]
CORNER_BOTTOM_RIGHT = ["┘", "┛", "╝"]
T_HORIZONTAL_LEFT = ["├", "┠", "╟"]
T_HORIZONTAL_RIGHT = ["┤", "┨", "╢"]


def renderCard(title, text, width, height, outline):
	output = ""
	#top line
	output += CORNER_TOP_LEFT[outline] + LINE_HORIZONTAL[outline]*(width-2) + CORNER_TOP_RIGHT[outline] + "\n"
	#title line
	output += LINE_VERTICAL[outline] + " " + title[:width-4] + " "*(width-3-len(title)) + LINE_VERTICAL[outline] + "\n"
	#title seperator
	output += T_HORIZONTAL_LEFT[outline] + LINE_HORIZONTAL[0]*(width-2) + T_HORIZONTAL_RIGHT[outline] + "\n"
	
	#keep track of how many characters the currently writing line has on it
	charactersOnLine = 0
	#keep track of the number of lines used which is different to the length of lines due to text wrapping
	numLines = 0
	lines = text.split("\n")
	for line in lines:
		#each line starts with a verticle
		output += LINE_VERTICAL[outline]
		words = line.strip().split(" ")
		for word in words:
			#if the word will fit on the line put it there
			if charactersOnLine + len(word) + 4 <= width:
				charactersOnLine += len(word) + 1
				output += " " + word
			#if the word will not fit on a line fill the remainder of the line with spaces then the ending verticle then a new line and a new verticle
			else:
				output += " "*(width - 2 - charactersOnLine) + LINE_VERTICAL[outline] + "\n" + LINE_VERTICAL[outline] + " " + word
				numLines += 1
				charactersOnLine = len(word) + 1
		#at the end of a line in the input text force a new line
		output += " "*(width - 2 - charactersOnLine) + LINE_VERTICAL[outline] + "\n"
		numLines += 1
		charactersOnLine = 0
	
	#draw the empty rows
	output += (LINE_VERTICAL[outline] + " "*(width-2) + LINE_VERTICAL[outline] + "\n")*(height - 4 - numLines)
	#bottom of the card
	output += CORNER_BOTTOM_LEFT[outline] + LINE_HORIZONTAL[outline]*(width-2) + CORNER_BOTTOM_RIGHT[outline]
	return output
