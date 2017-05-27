import socket
from slackclient import SlackClient

####################slack setup#######################
SLACK_TOKEN = 'insert token here' #deleted my token for github but to test place a token here
slack_client = SlackClient(SLACK_TOKEN)
user_slack_id = '@axelle' #change this to your own username for testing
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80)) #surf to google dns and see what ip it uses
ip = s.getsockname()[0]
s.close()

######################functions#######################
def send_msg(channel_id, msg):
	slack_client.api_call(
		"chat.postMessage",
		channel=channel_id,
		text=msg,
		username='pythonbot',
		icon_emoji=':robot_face:'
	)
