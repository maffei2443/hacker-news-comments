This project aims to crawl (possibly all) comments of [hacker-news](https://news.ycombinator.com/newcomments) and dump they into a local [*MongoDatabase*](https://www.mongodb.com/).

## hacker-news-comments
This little project aims to:

1. get all comments from [hacker news][hn] website;
2. Update such base from time to time;
3. Trigger a signal once some custom event occurs.
    - Currently, the only custom event is the occurence of specific words.

### How to use (assuming `sudo` access)

##### 1. Install dependencies
Change current directory to `tutorial`
```sh
pip install -r requirements.txt
```


##### 2. Change into directory and run
```sh
cd tutorial
  
# Crawl how much pages you prefer
scrapy crawl comments
    
# For download all comments not yet downloaded since the 
# last downloaded comment
scrapy crawl comments -s CLOSESPIDER_PAGECOUNT=0
```

#### 3. \[Optional\] Run mongodb on docker
```sh
docker-compose -f local-compose.yml up
```

Alternatively you can configure your own [mongodb][mongodb] server. Check **tutorial/tutorial/settings.py**
for eventual envirnoment variables that must be set.

#### 10. \[Optional\] Run tests
1. Install dependencies
    ```sh
    pip install pytest==6.0.2
    ```
2. Run tests
    ```sh
    pytest
    ```


### How to run on [Docker][docker]

1. Install [docker][get-docker]
2. Install [docker-compose][get-compose]
3. Run the application.
```sh
    docker-compose up -d
```
4. NOTE: if some modification is done on the source and you want to update
    the containerzed application then the follow steps are required:
    ```sh
        docker-compose down   # to stop the application
        docker-compose build  # rebuild the image
        docker-compose up     # start application again
    ```


### Limitations (a.k.a TODO)

1. Missing tests: could not implement automated tests for the main spider.
    - The only automated tests are for the **helper.py** file

2. Can not access `hn_comments_crawler` through localhost.
    - Could not configure the network correctly. At the moment it is not possible to access `hn_comments_crawler` container directly from *localhost* .

3. Currently the comments are crawled taking into account only the **id** field.
    - It would be very good to be able specify manually a lower bound for the IDs or another criteria
    such as date. However date was not take into account for performance reasons since it would be necessary
    to send a request for each comment crawled.
    - Also it would be interesting to have an option do crawl only specific comments


### Observations
1. The "alarm" consists of dumping the **id**s of comments containing the *linux* substring in the **linux_ids** collection. 
2. The database name is defined on the *settings.py* file.


### References

1. [Hacker news API (github)][hn-api]
2. [Hacker news API docs][hn2]
3. [DODFMiner][dodfminer] (for structuring the tests)
4. [Project template][pytemplate]
5. [Project structuring][structuring]
6. [hackeRnews][hackeRnews], an R package for getting data from HN
7. [Leap year][ly]
8. [xpath exact][xpath-e]
9. [xpath and css equivalences cheat sheet][cheatsheet]
10. [xpath cheatsheed][xpsheet]
11. [mongodb vs sql][no-vs-sql]
12. [pymongo docs][pymongo]
13. [Scrapy architecture overview][scrapy-arch]
14. [Scrapy+docker][scrapy-docker]
15. [Docker docs][docdoc]
16. [docker-cron][dcron]
17. [scrapyd][scpd]
18. [scrapy-client][sc-client]
19. [scrapyd-client installation][sc-client-install]

[hn-api]: https://github.com/HackerNews/API
[hn]: https://news.ycombinator.com/
[hn2]: https://hackernews.api-docs.io/v0/items/comment
[dodfminer]: https://github.com/UnB-KnEDLe/DODFMiner
[pytemplate]: https://realpython.com/python-application-layouts/#command-line-application-layouts
[structuring]: https://docs.python-guide.org/writing/structure/
[hackeRnews]: https://cran.r-project.org/web/packages/hackeRnews/vignettes/hackeRnews-specs.html 
[ly]: https://www.programiz.com/python-programming/examples/leap-year
[xpath-e]: https://bangladroid.wordpress.com/2018/05/24/xpath-how-to-locate-a-node-using-exact-text-match/
[cheatsheet]: https://en.wikibooks.org/wiki/XPath/CSS_Equivalents
[xpsheet]: https://devhints.io/xpath
[no-vs-sql]: https://www.xplenty.com/blog/mongodb-vs-mysql/
[pymongo]: https://pymongo.readthedocs.io/en/stable/tutorial.html
[scrapy-arch]: https://docs.scrapy.org/en/latest/topics/architecture.html
[scrapy-docker]: https://shinesolutions.com/2018/09/13/running-a-web-crawler-in-a-docker-container/
[docdoc]: https://docs.docker.com/
[dcron]: https://github.com/cheyer
[scpd]: https://github.com/scrapy/scrapyd
[sc-client]: https://github.com/scrapy/scrapyd-client
[sc-client-install]: https://stackoverflow.com/questions/45750739/scrapyd-client-command-not-found
[get-docker]: https://docs.docker.com/get-docker/
[get-compose]: https://docs.docker.com/compose/install/
[docker]: https://www.docker.com/
[mongodb]: https://www.mongodb.com/

