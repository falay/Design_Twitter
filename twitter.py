from heapq import merge


class Twitter:

    class tweet_article(object):
        
        def __init__(self, author, tweet_id, time_stamp):
            
            self.author = author
            self.tweet_id = tweet_id
            self.time_stamp = time_stamp
    
    class User(object):
        
        def __init__(self, user_id):
            
            self.user_id = user_id
            self.posted_tweets = []
            self.news_feed = []
            self.followers = {}
            self.followees = {}
    
        def post_tweet(self, tweet_id, current_time):
            
            new_tweet = Twitter.tweet_article( self, tweet_id, current_time )
            self.posted_tweets.append( new_tweet )
            self.news_feed.append( new_tweet )
            for followee in self.followees:
                followee.news_feed.append( new_tweet )
                

        def follow(self, some_one):
            
            if some_one in self.followers:
                return
            
            self.followers[ some_one ] = True
            some_one.followees[ self ] = True
            
            self.news_feed = list( merge( self.news_feed, some_one.posted_tweets, key = lambda tweet : tweet.time_stamp  ) )
            
            
        def unfollow(self, some_one):
            
            if some_one not in self.followers:
                return
            
            self.followers.pop( some_one )
            some_one.followees.pop( self )
            
            update_news_feed = []
            for tweet in  self.news_feed:
                if tweet.author != some_one:
                    update_news_feed.append( tweet )
            self.news_feed = update_news_feed
        
                                  
        def get_news_feed(self):
            
            latest_tweets = list( reversed( self.news_feed ) )
            return_tweets = latest_tweets[:10] if len(latest_tweets) > 10 else latest_tweets
            return [ tweet.tweet_id for tweet in return_tweets ]
   
    
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.tweet_users = {}    
        self.current_time = 0
    
    def get_user(self, userId):
        
        if userId not in self.tweet_users:
            self.tweet_users[ userId ] = self.User( userId )
        
        #print( 'User', userId, 'has tweets:', self.tweet_users[ userId ].news_feed._tweets )
        
        return self.tweet_users[ userId ]  
            
    
    def postTweet(self, userId, tweetId):
        """
        Compose a new tweet.
        :type userId: int
        :type tweetId: int
        :rtype: void
        """
        user = self.get_user( userId )
        user.post_tweet( tweetId, self.current_time )
        self.current_time += 1
        
    
    def getNewsFeed(self, userId):
        """
        Retrieve the 10 most recent tweet ids in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user herself. Tweets must be ordered from most recent to least recent.
        :type userId: int
        :rtype: List[int]
        """
        user = self.get_user( userId )
        return user.get_news_feed()
    
    
    def follow(self, followerId, followeeId):
        """
        Follower follows a followee. If the operation is invalid, it should be a no-op.
        :type followerId: int
        :type followeeId: int
        :rtype: void
        """
        if followerId == followeeId:
            return
        user = self.get_user( followerId )
        user.follow( self.get_user(followeeId) )
        

    def unfollow(self, followerId, followeeId):
        """
        Follower unfollows a followee. If the operation is invalid, it should be a no-op.
        :type followerId: int
        :type followeeId: int
        :rtype: void
        """
        if followerId == followeeId:
            return
        user = self.get_user( followerId )
        user.unfollow( self.get_user(followeeId) )


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)