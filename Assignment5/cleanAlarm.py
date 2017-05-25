import doorAlarm as alarm

def cleanupTool():
    #read all lines in the file then close it
    lines = alarm.readFile("timeFile.txt")

    #Offer user two modes in which he can cleanup the file
    mode=input("Type 1 to clean up line per line, type 2 to clean up a certain range: ")
    if(mode=="1"):
        print("Cleaning line per line")
        for line in list(lines):
            print(line)
            rm=input("Do you want to remove this line? (y)")
            if(rm=="y"):
                lines.remove(line)
    elif(mode=="2"):
        print("".join(lines))
        startdate=time.strptime(input("Select start date to remove"),"%a, %d %b %Y %H:%M:%S")
        enddate=time.strptime(input("Select end date to remove"),"%a, %d %b %Y %H:%M:%S")
        print("Start: " + startdate + " End: " + enddate)
        for line in list(lines):
            dateLine=strptime(line.rstrip("\n"),"%a, %d %b %Y %H:%M:%S")
            if(startdate<=dateLine<=enddate):
                lines.remove(line)

    #Write changes to the file:
    print("Writing changes to file.")
    alarm.writeFile("timeFile.txt","".join(lines))


def main():
	try:
		cleanupTool()
	except KeyboardInterrupt:
		print("Closing.")
	else:
		pass
	finally:
		pass

if __name__ == "__main__":
    main()
