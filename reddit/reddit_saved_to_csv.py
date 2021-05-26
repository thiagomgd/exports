#! python3
# reddit_saved_to_csv.py - Exports your saved Posts and Comments on Reddit to a csv file.
import praw, csv, codecs, json, datetime, pprint

client_id=''
client_secret=''
username=''
password=''

reddit = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent='Saved posts scraper by /u/' + username,
                    username=username,
                    password=password)

reddit_home_url = 'https://www.reddit.com'

saved_models = reddit.user.me().saved(limit=100) # models: Comment, Submission

# reddit_saved_csv = codecs.open('reddit_saved.csv', 'w', 'utf-8') # creating our csv file

# # CSV writer for better formatting
# saved_csv_writer = csv.writer(reddit_saved_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
# saved_csv_writer.writerow(['ID', 'Name', 'Subreddit', 'Type', 'URL', 'NoSFW']) # Column names

saved_posts = {}
saved_comments = {}

def post_dict(model):
    post = {
        'subreddit': model.subreddit.name,
        'subr_name': model.subreddit.display_name,
        'url': reddit_home_url + model.permalink,
        'title': model.title,
        'nsfw': str(model.over_18),
        'author': model.author.name if model.author else 'deleted',
        'is_original': model.is_original_content,
        'flair': model.link_flair_text,
        'created': model.created_utc
    }

    return post

def comment_dict(model):
    comment = {
        'subreddit': model.subreddit.name,
        'subr_name': model.subreddit.display_name,
        'url': reddit_home_url + model.permalink,
        'title': model.submission.title,
        'nsfw': str(model.submission.over_18),
        'author': model.author.name if model.author else 'deleted',
        'is_original': model.submission.is_original_content,
        'flair': model.submission.link_flair_text,
        'created': model.created_utc
    }

    return comment


def handle(saved_models):
    count = 0
    for model in saved_models:
        count += 1
        print(reddit_home_url + model.permalink)
        subreddit = model.subreddit.name # Subreddit model that the Comment/Submission belongs to

        if isinstance(model, praw.models.Submission): # if the model is a Submission
            if subreddit not in saved_posts:
                saved_posts[subreddit] = []

            saved_posts[subreddit].append(post_dict(model))
        else: # if the model is a Comment
            if subreddit not in saved_comments:
                saved_comments[subreddit] = []
            
            saved_comments[subreddit].append(comment_dict(model))

        # saved_csv_writer.writerow([str(count), title, subr_name, model_type, url, noSfw])

    print(count)

    time_stamp =  datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")

    with open('saved_posts_{}.json'.format(time_stamp), "w") as f:
        json.dump(saved_posts, f, indent=4)

    with open('saved_comments_{}.json'.format(time_stamp), "w") as f:
        json.dump(saved_comments, f, indent=4)
        # print("Wrote {len(saved_posts)} entries to {saved_posts}")
    
# def delete(saved_models):
    # for model in saved_models:
        # pprint.pprint(model)
        # cmmt = reddit.comment(id=model.id)
        # cmmt.unsave()
        # model.unsave()

handle(saved_models)
# delete(saved_models)
# reddit_saved_csv.close()

print("\nCOMPLETED!")
# print("Your saved posts are available in reddit_saved.csv file.")
