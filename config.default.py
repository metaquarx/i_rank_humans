# When editing this file, make sure you are using the tab character and not
# spaces, when indenting.

# Settings to use when authenticating with reddit. Check Reddit's quick start
# guide to create an id and secrethttps://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps],
# and Reddit's API wiki page to learn more about the user agent [https://github.com/reddit-archive/reddit/wiki/API]
praw = dict(
	client_id = "",
	client_secret = "",
	user_agent = ""
)

# A list of the subreddits to check and keep track of.
# Leave empty to select all subreddits.
subreddits = [
]

# Database repository. Should be in the format:
# https://username:password@repository.com/file.git
# If your password contains the "@" symobol, replace it with "%40".
db_repo = ""
