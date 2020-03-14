import wget, subprocess, os
from PyInquirer import prompt
from pathlib import Path

class Installer:

	__memory = None
	__server_directory = None
	__build_tools_filename = None

	def __init__(self):
		if self.is_java_installed() and self.is_git_installed():
			self.__server_directory = self.choose_server_directory()
			self.prepare_server_directory()
			self.__memory = self.java_memory_allocation()
			self.__build_tools_filename = self.download_build_tools()
			self.execute_build_tools()

	def is_java_installed(self):
		result = subprocess.run('java -version', shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
		if result.returncode == 0:
			return True
		else:
			print('Java not installed!')
			return False

	def is_git_installed(self):
		result = subprocess.run('git --version', shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
		if result.returncode == 0:
			return True
		else:
			print('Git not installed!')
			return False

	def choose_server_directory(self):
		question = [
			{
				'type': 'input',
				'name': 'server_directory',
				'message': 'Custom server directory',
				'default': 'server'
			}
		]
		answer = prompt(question)
		return answer['server_directory']

	def prepare_server_directory(self):
		buildtools = os.path.join(self.__server_directory, 'BuildTools.jar')
		Path(self.__server_directory).mkdir(parents=True, exist_ok=True)
		if os.path.exists(buildtools):
			os.remove(buildtools)

	def java_memory_allocation(self):
		question = [
			{
				'type': 'list',
				'name': 'memory',
				'message': 'Java memory allocation:',
				'choices': ['2048M', '1024M', '512M']
			}
		]
		answer = prompt(question)
		return answer['memory']

	def download_build_tools(self):
		print('\nDownloading BuildTools...')
		filename = wget.download('https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar', out=self.__server_directory)
		return os.path.basename(filename)

	def execute_build_tools(self):
		print('Installing BuildTools...')
		result = subprocess.run('java -Xmx{memory} -Xms{memory} -jar {filename}'.format(memory=self.__memory, filename=self.__build_tools_filename), shell=True, cwd=self.__server_directory)
		print('BuildTools installed!')

if __name__ == "__main__":
	Installer()