import tweepy, yaml, re
from spotter import Spotter


class TwitterScraper(Spotter):


    DEFANG_URL_FINDER = re.compile(r"(?:ftp|h(?:xx|tt)ps?)://\S+")
    DEFANG_DOMAIN_FINDER = re.compile(r"\s((?=\S+\[\.\])((?:[a-z0-9-]+)(?:\.|\[\.\]))+[a-z]{2,}\S+)")

    def __init__(self):
        super(TwitterScraper, self).__init__()
        auth = tweepy.OAuthHandler(self.config['twitter']['consumer_key'], self.config['twitter']['consumer_secret'])
        auth.set_access_token(self.config['twitter']['access_token_key'], self.config['twitter']['access_token_secret'])
        self.api = tweepy.API(auth)


    def retweeted(self, data):
        text = None
        try: 
            text = data['retweeted_status']['extended_tweet']['full_text']
        except: 
            # Try for extended text of an original tweet, if RT'd (REST API)
            try: 
                text = data['retweeted_status']['full_text']
            except:
                # Try for extended text of an original tweet (streamer)
                try: 
                    text = data['extended_tweet']['full_text']
                except:
                    # Try for extended text of an original tweet (REST API)
                    try: 
                        text = data['full_text']
                    except:
                        # Try for basic text of original tweet if RT'd 
                        try: 
                            text = data['retweeted_status']['text']
                        except:
                            # Try for basic text of an original tweet
                            try: 
                                text = data['text']
                            except: 
                                # Nothing left to check for
                                text = ''
        return text

    def _extract_urls(self, string):
        return_list = []
        result = self.DEFANG_URL_FINDER.finditer(string)
        if result:
            for m in result:
                return_list.append(m.group())
        
        result = self.DEFANG_DOMAIN_FINDER.finditer(string)
        if result:
            for m in result:
                return_list.append(m.group())

        return return_list


    def on_status(self, tweet):
        if hasattr(tweet, "retweeted_status"):  # Check if Retweet
            try:
                return tweet.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                return tweet.retweeted_status.full_text
        else:
            try:
                return tweet.extended_tweet["full_text"]
            except AttributeError:
                return tweet.full_text

    def get(self, since_id=None):
        return_list = []
        for tweet in tweepy.Cursor(self.api.search,
                           q="#opendir OR #phishkit OR #phishingkit",
                           count=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en",
                           since_id=None if not since_id else since_id,
                           tweet_mode="extended").items():
            return_dict = {
                'id': tweet.id,
                'text': self.on_status(tweet)
            }
            
            tag_list = []
            for tag in tweet.entities['hashtags']:
                tag_list.append(tag['text'])
            return_dict.update({'tags': tag_list})
            
            url_list = []
            expanded_url_list = []
            try:
                for url in tweet.retweeted_status.entities['urls']:
                    return_dict['text'] = return_dict['text'].replace(url['url'], url['expanded_url'])
                    url_list.append(url['url'])
                    expanded_url_list.append(url['expanded_url'])
            except:
                pass
            
            
            return_dict.update({
                'urls': url_list,
                'expanded_urls': expanded_url_list,
                'extracted_urls': self._extract_urls(return_dict['text'])
            })

            return_list.append(return_dict)
        return return_list