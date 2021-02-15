# hacker-news-comments
This little project aims to:

    1. get all comments from [hacker news][hn] website;
    2. Update such base from time to time;
    3. Trigger a signal once some custom event occurs.
        - Currently, the only custom event is the occurence of specific words.

###### References
    1. [Hacker news API (github)][hn]
    2. [Hacker news API docs][hn2]
    3. [DODFMiner][dodfminer] (for structuring the tests)
    4. [Project template][pytemplate]
    5. [Project structuring][structuring]
    6. [hackeRnews][hackeRnews], an R package for getting data from HN
    7. [Leap year][ly]
    8. [xpath exact][xpath-e]
    9. [xpath and css equivalences cheat sheet][cheatsheet]


[hn]: https://news.ycombinator.com/
[hn2]: https://hackernews.api-docs.io/v0/items/comment
[dodfminer]: https://github.com/UnB-KnEDLe/DODFMiner
[pytemplate]: https://realpython.com/python-application-layouts/#command-line-application-layouts
[structuring]: https://docs.python-guide.org/writing/structure/
[hackeRnews]: https://cran.r-project.org/web/packages/hackeRnews/vignettes/hackeRnews-specs.html 
[ly]: https://www.programiz.com/python-programming/examples/leap-year
[xpath-e]: https://bangladroid.wordpress.com/2018/05/24/xpath-how-to-locate-a-node-using-exact-text-match/
[cheatsheet]: https://en.wikibooks.org/wiki/XPath/CSS_Equivalents
