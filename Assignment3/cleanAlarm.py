import doorAlarm as alarm

def main():
	try:
		alarm.cleanupTool()
	except KeyboardInterrupt:
    	print("Closing.")
	else:
		pass
	finally:
		pass

if __name__ == "__main__":
    main()