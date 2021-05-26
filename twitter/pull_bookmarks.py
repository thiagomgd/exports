


url = "https://api.twitter.com/2/timeline/bookmark.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweets=true&count=20&ext=mediaStats%2ChighlightedLabel%2CcameraMoment"

def extract_cursor(response):
    try:
        return response.json()['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
    except KeyError as e: 
        return None

initial = True
while True:
    if initial:
        response = api_request(url, headers, cookies)
        for tweet in response.json()['globalObjects']['tweets'].values():
            print(tweet['created_at'], tweet['id_str'], tweet['full_text'][:50])

        initial = False
    else:
        sleep(5)  # Apparently 4 is too fast and 6 is too slow... idk wtf is going on
        
        cursor_value = extract_cursor(response) 
        if cursor_value is None:
            break

        response = api_request(url + f'&cursor={cursor_value}', headers, cookies)
        print(response.status_code)

        if response.status_code != 200:
            break

        for tweet in response.json()['globalObjects']['tweets'].values():
            print(tweet['created_at'], tweet['id_str'], tweet['full_text'][:50])

pull_bookmarks