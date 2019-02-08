import pickle

pickle_loc = "databases/inputData.pickle"
class ChallengeAttempt:
	time = None
	content = None
	username = None
	def __init__(self, time, content, username):
		self.time = time
		self.content = content
		self.username = username

	def __repr__(self):
		return "<ChallengeAttempt Content: {}, Time: {}, User: {}>\n".format(self.content, self.time, self.username)

	@staticmethod
	def save_content(example_dict):
		input_data_file = open(pickle_loc, "wb")
		pickle.dump(example_dict, input_data_file)
		input_data_file.close()

	@staticmethod
	def get_all_content():
		input_data_file = open(pickle_loc, "rb")
		try:
			example_dict = pickle.load(input_data_file)
			return example_dict
		except EOFError:
			return {}

	@staticmethod
	def save_to_challenge(name, username, time, content):
		data = ChallengeAttempt.get_all_content()
		try:
			data[name].append(ChallengeAttempt(time, content, username))
		except KeyError:
			data[name] = [ChallengeAttempt(time, content, username)]
		ChallengeAttempt.save_content(data)

	@staticmethod
	def get_from_challenge(name):
		data = ChallengeAttempt.get_all_content()
		try:
			return data[name]
		except KeyError:
			return None







