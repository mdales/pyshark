import json
import os
import platform
import pkg_resources
import sys
from datetime import datetime, timezone
from typing import Any,Dict

import git

class Manifest:
	def __init__(self):
		self.start = datetime.now(timezone.utc)
		self.inputs = set()
		self.outputs = set()

	def append_input(self, filename: str) -> None:
		self.inputs.add(filename)

	def append_output(self, filename: str) -> None:
		self.outputs.add(filename)

	@staticmethod
	def get_python_env() -> Dict[str,Any]:
		return {
			"version": sys.version,
			"packages": {p.project_name:p.version for p in pkg_resources.working_set},
		}

	@staticmethod
	def get_platform() -> Dict[str,str]:
		uname = platform.uname()
		return {
			"system": uname.system,
			"release": uname.release,
			"version": uname.version,
			"machine": uname.machine,
			"processor": uname.processor,
		}

	@staticmethod
	def get_git_status() -> Dict[str,Any]:
		try:
			repo = git.Repo(search_parent_directories=True)
		except git.exc.InvalidgitRepository:
			return {"error": "no git repository found"}
		return {
			"branch": repo.active_branch.name,
			"commit": repo.head.object.hexsha,
			"dirty": repo.is_dirty(),
			"remotes": {
					r.name: [url for url in r.urls]
				for r in repo.remotes
			}
		}


	def save(self, filename: str) -> None:
		document = {
			"start": self.start.isoformat(),
			"end": datetime.now(timezone.utc).isoformat(),
			# "env": dict(os.environ),
			"inputs": list(self.inputs),
			"outputs": list(self.outputs),
			"git": self.get_git_status(),
			"uname": self.get_platform(),
			"python": self.get_python_env(),
		}
		print("Shark manifest:")
		print(json.dumps(document, indent=4))

manifest = Manifest()
