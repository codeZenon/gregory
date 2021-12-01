# Gregory
Gregory aggregates searches in JSON and outputs to a Hugo static site

[TOC]

# Live Version

https://gregory-ms.com

# Install

## Server Requirements

- [ ] [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)
- [ ] [Hugo](https://gohugo.io/) 
- [ ] [Mailgun](https://www.mailgun.com/)
- [ ] [Node JS v14.18.1](https://nodejs.org/en/)
- [ ] [SQLite](https://www.sqlite.org/index.html)

## Setup the environment

Execute `python3 setup.py`. The script will check if you have all the requirements and run the Node-RED container.

Edit the build.py file's variables to reflect your environment.

Finally, build the site with `python3 ./build.py`.

# Node-RED

This is where all of the processing of information happens. Node-RED provides a set of API endpoints to access the information it collects.

The following tabs have been configured to divide the flows:

1. Research (Collect data from different sources)
2. Email Digest (Sent to the admin and to subscribers)
3. API
4. Tests

`data/articles.json` and `data/trials.json` are generated from a Node-Red flow available in the `flows.json` file.

# Mailgun

Currently, we are using Mailgun to send emails to the admin and subscribers. These nodes can be found on the Email Digest tab of Node-RED and have been disabled.

To enable them, you will need a mailgun account, or you can replace them with another way to send emails.

# Database

The path `/api/articles.json` and `/api/trials.json` includes the full database export.

The same information is available in excel format: `/api/articles.xlsx` and `/api/trials.xlsx`.

# Roadmap

New sources we would like to add:
 - RNEC
 - FirstWord Pharma
 - [EMA](https://www.ema.europa.eu/en/human-regulatory/research-development/clinical-trials/clinical-trials-information-system-training-support) (CTIS system to be made available online on January 2022)
 - Champalimaud Foundation
 - CEIC (Doesn't seem to have any public database)


# Thank you to
@[Antoniolopes](https://github.com/antoniolopes) for helping with the Machine Learning script.
@[Chbm](https://github.com/chbm) for help in keeping the code secure.    
@[Jneves](https://github.com/jneves) for help with the build script    
@[Melo](https://github.com/melo) for showing me [Hugo](https://github.com/gohugoio/hugo)    
@[Nurv](https://github.com/nurv) for the suggestion in using Spacy.io    
@[RainerChiang](https://github.com/RainerChiang) for the [Simplesness theme](https://github.com/RainerChiang/simpleness)    
@[Rcarmo](https://github.com/rcarmo) for showing me [Node-RED](https://github.com/node-red/node-red)       

And the **Lobsters** at [One Over Zero](https://github.com/oneoverzero)

