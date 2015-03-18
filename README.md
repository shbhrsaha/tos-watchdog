# tos-watchdog

Use GitHub to track changes in popular terms of service and privacy policy documents.

How it works
---
`urls.txt` contains URLs of terms/privacy documents for popular services. A background service requests each document once an hour and publishes any changes to this repository inside the `content` folder. Submit a pull request to add urls for tracking.

Some of the URLs were discovered with DOM heuristics implemented in `src/domains-to-urls.py`.