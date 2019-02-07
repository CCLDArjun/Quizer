import pickle

class ChallengeAttempt:
	time = None
	content = None
	pickle_loc = "databases/inputData.pickle"
	def __init__(self, time, content):
		self.time = time
		self.content = content

	def __repr__(self):
		return "<ChallengeAttempt Content: {}, Time: {}>\n".format(self.content, self.time)

	@staticmethod
	def save_content(example_dict):
		input_data_file = open(self.pickle_loc, "wb")
		pickle.dump(example_dict, input_data_file)
		input_data_file.close()

	@staticmethod
	def get_content():
		input_data_file = open(self.pickle_loc, "rb")
		example_dict = pickle.load(input_data_file)
		return example_dict

	@staticmethod
	def save_to_user(username, time, content):
		data = ChallengeAttempt.get_content()
		try:
			data[username].append(ChallengeAttempt(time, content))
		except KeyError:
			data[username] = [ChallengeAttempt(time, content)]
		ChallengeAttempt.save_content(data)
