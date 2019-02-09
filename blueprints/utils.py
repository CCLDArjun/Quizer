import pickle
import datetime
from datetime import date

pickle_loc = "databases/inputData.pickle"
class ChallengeAttempt:
	time = None
	content = None
	username = None
	challenge_name = None
	def __init__(self, time, content, username, challenge_name):
		self.time = time
		self.content = content
		self.username = username
		self.challenge_name = challenge_name

	def __repr__(self):
		return "<ChallengeAttempt Content: {}, Time: {}, User: {}, ChallengeName: {}>\n".format(self.content, self.time, self.username, self.challenge_name)

	'''DO NOT CALL THIS OUTSIDE'''
	@staticmethod
	def _save_content(example_dict):
		input_data_file = open(pickle_loc, "wb")
		pickle.dump(example_dict, input_data_file)
		input_data_file.close()

	'''DO NOT CALL THIS OUTSIDE'''
	@staticmethod
	def _get_raw_data():
		input_data_file = open(pickle_loc, "rb")
		try:
			example_dict = pickle.load(input_data_file)
			return example_dict
		except EOFError:
			return []

	@staticmethod
	def add(name, username, time, content):
		data = ChallengeAttempt._get_raw_data()
		data.append(ChallengeAttempt(time, content, username, name))
		ChallengeAttempt._save_content(data)

	@staticmethod
	def get_submissions():
		subs = ChallengeAttempt._get_raw_data()
		for submission in subs:
			delta = datetime.datetime.utcnow()-submission.time
			submission.time = round(float(delta.days*24 + delta.seconds/3600), 2)
		print(subs)
		return subs







