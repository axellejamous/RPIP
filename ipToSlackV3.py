#print current ip address to slack

#imports
import socket
from slackclient import SlackClient
import os

SLACK_TOKEN = 'xoxp-143901355236-143911167621-143830738338-d262f929502e2245860a9866e2a5b3da'
slack_client = SlackClient(SLACK_TOKEN)
user_slack_id = 'axelle'
im_call = slack_client.api_call("im.list")
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#hostname = socket.gethostname()
#ip = socket.gethostbyname(hostname) #will return first ip found
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

				#search users IM channel ID 
				if im_call.get('ok'):
					print("im call success")
					for im in im_call.get('ims'):
						if im.get('user') == user_slack_id:
							im_channel = im.get('id')
							send_msg(channel[im_channel], "Test")

				f = open(os.path.join(__location__, 'ipFile.txt'), 'r')
				prev_ip = f.read()
				f.close()

				if prev_ip != '' and ip == prev_ip:
					send_msg(channel['id'], "IP is the same as last time!")
				else:
					send_msg(channel['id'], "IP: " + ip)
					send_msg(channel[user_slack_id], "IP: " + ip) 
			
					f = open(os.path.join(__location__, 'ipFile.txt'),'w')
					f.write(ip)
					f.close()
		print('-----')
	else:
		print("Unable to authenticate.")
