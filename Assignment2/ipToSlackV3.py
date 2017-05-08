#Axelle Jamous 2EA1 s090603

#imports
import socket
from slackclient import SlackClient
import os
from time import sleep

sleep(60)

SLACK_TOKEN = 'insert token here' #deleted my token for github but to test place a token here
slack_client = SlackClient(SLACK_TOKEN)
user_slack_id = '@axelle' #change this to your own username for testing
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80)) #surf to google dns and see what ip it uses
print('Used IP: ' + s.getsockname()[0])
ip = s.getsockname()[0]
s.close()


#functions
def list_channels():
	channels_call = slack_client.api_call("channels.list")
	if channels_call.get('ok'):
		return channels_call['channels']
	return None

def send_msg(channel_id, msg):
	slack_client.api_call(
		"chat.postMessage",
		channel=channel_id,
		text=msg,
		username='pythonbot',
		icon_emoji=':robot_face:'
	)

def send_priv_msg(msg):
	slack_client.api_call(
		"chat.postMessage",
		asuser = True,
		channel=user_slack_id,
		text=msg
	)

#main
#we will send a message both in the general channel and as dm
if __name__ == '__main__':
	channels = list_channels()
	if channels:
		print("Slack Channels: ")
		for channel in channels:
			print(channel['name'] + " (" + channel['id'] + ")")

			if channel['name'] == 'general':
				send_msg(channel['id'], "Hello " + channel['name'] + '!')

				f = open(os.path.join(__location__, 'ipFile.txt'), 'r')
				prev_ip = f.read()
				f.close()

				if prev_ip != '' and ip == prev_ip:
					send_msg(channel['id'], "IP is the same as last time! ->" + ip)
					send_priv_msg("IP is the same as last time! ->" + ip)
				else:
					send_msg(channel['id'], "Your IP: " + ip)
					send_priv_msg("Your IP: " + ip)
			
					f = open(os.path.join(__location__, 'ipFile.txt'),'w')
					f.write(ip)
					f.close()
		print('-----')
	else:
		print("Unable to authenticate.")
