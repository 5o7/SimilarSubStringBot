import praw
import time

creds = {"client_id": "X",
         "client_secret": "X",
         "password": "X",
         "user_agent": "Find similar substrings in submissions.",
         "username": "5o7bot"}

reddit = praw.Reddit(client_id=creds["client_id"],
                     client_secret=creds["client_secret"],
                     password=creds["password"],
                     user_agent=creds["user_agent"],
                     username=creds["username"])

# Function receives a string and a set character length

def find_similar_substrings(string, length=64):
    similar_substrings = set()
    n = len(string)

    for i in range(n - length + 1):
        substring = string[i:i + length]
        for j in range(i + 1, n - length + 1):
            compare_substring = string[j:j + length]
            if substring == compare_substring:
                similar_substrings.add(substring)

    # If similar substrings found, return a list of them

    return similar_substrings

# List gets populated with submission titles to avoid rechecking

checked = []

# This loop runs every 20 minutes

while True:

    # Collect 10 submissions from various subreddits

    subreddits = []
    submissions = []
    subreddits.append("subreddit_name")

    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).__getattribute__("new")(limit=10):
            if not any(x in submission.title for x in checked):
                checked.append(submission.title)

                # Send the submission's body to the find_similar_substrings function

                similar_substrings = find_similar_substrings(submission.selftext)

                # If the function found similar substrings, a list of them gets returned

                if similar_substrings:

                    # Send a reply and remove submission

                    submission.reply("Post removed due to duplicate phrases. Please try again.")
                    submission.mod.remove()

                    # Print the list of similar substrings

                    print("Similar substrings found.")
                    for substring in similar_substrings:
                        print(substring)

                else:
                    print("No similar substrings found.")

    # Sleep for 20 minutes

    time.sleep(1200)