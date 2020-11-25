#!/usr/bin/env python3

# Copyright 2020 metaquarx, metaquarx@pm.me

# This file is part of i_rank_humans.
#
# i_rank_humans is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# i_rank_humans is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with i_rank_humans.  If not, see <https://www.gnu.org/licenses/>.

import config
import praw
import subprocess
from os.path import isfile
import json

def update_humans(name, change):
	subprocess.run(["git", "clone", config.db_repo, "./db/"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	data = {}
	if isfile("./db/db.json"):
		with open("./db/db.json") as dbfile:
			data = json.load(dbfile)

	if name not in data:
		data[name] = []
		data[name].append(0) # good human
		data[name].append(0) # bad human

	if change == 1:
		data[name][0] += 1
	elif change == -1:
		data[name][1] += 1

	with open("./db/db.json", "w") as outfile:
		json.dump(data, outfile)

	subprocess.run(["git", "add", "db.json"], cwd="./db/", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	subprocess.run(["git", "commit", "-m", "Update data"], cwd="./db/", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	subprocess.run(["git", "push", config.db_repo, "--all"], cwd="./db/", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	subprocess.run(["rm", "-rf", "./db/"])


def main():
	# Generate praw instance (read-only)
	reddit = praw.Reddit(
		client_id = config.praw["client_id"],
		client_secret = config.praw["client_secret"],
		user_agent = config.praw["user_agent"]
	)

	# Check that subreddits exist, add into a list
	approved_subreddits = []
	if not config.subreddits:
		approved_subreddits.append("all")
	else:
		for subreddit in config.subreddits:
			try:
				reddit.subreddits.search_by_name(subreddit, exact=True)
				approved_subreddits.append(subreddit)
			except NotFound:
				print("WARNING: Subreddit {} requested, but not found! Skipping.".format(subreddit))
	print("Listening on subreddits: {}".format(approved_subreddits))

	# Begin listening
	subreddits = reddit.subreddit("+".join(approved_subreddits))
	for comment in subreddits.stream.comments(skip_existing=True):
		change = 0
		if "good human" == comment.body.lower():
			change += 1
		elif "bad human" == comment.body.lower():
			change -= 1

		if change != 0:
			if comment.parent_id.startswith("t1_"): # Is not top level comment
				parent = reddit.comment(comment.parent_id[3:]).author
				if parent.id != comment.author.id:
					update_humans(parent.name, change)
					print("Awarded {} to {}".format(change, parent.name))

if __name__ == "__main__":
	main()
