# tos-watchdog

Use GitHub to track changes in popular terms of service and privacy policy documents. Similar to [Docracy](http://www.docracy.com/) and [TOSBack](https://tosback.org/). This GitHub repository _is_ the live application. Periodically check the `content` folder to read documents as they change over time.

How it works
---
`urls.txt` contains URLs of terms/privacy documents for popular services. A cron job requests each document once an hour and publishes changes to this repository's `content` folder. Submit a pull request on `urls.txt` to add popular urls for tracking.

Some of the URLs were discovered with DOM heuristics implemented in `src/domains-to-urls.py`.
