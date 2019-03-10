#!/usr/bin/python3
import requests


def send_notification(notification):
	payload = {
	  "app_key": "fq7BiSDaO5in2w6dGijW",
	  "app_secret": "x81t4jCpcYAQiKJAw5u8wSVrSDX1cJ6tTDG0qw988v5KOwu6KjZ6dRA0nhA4ii2I",
	  "target_type": "app",
	  "content": notification
	}
	r = requests.post("https://api.pushed.co/1/push", data=payload)
	return r.text


print(send_notification('hi, me'))