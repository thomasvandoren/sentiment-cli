# sentiment-cli
CLI utility for easily running sentiment analysis on text.

Configure your terminal to use AWS Comprehend, e.g. by setting AWS_PROFILE env var or running `aws configure`.

```
pipenv install
pipenv run python sentiment.py # when there are no args, it uses pasteboard
pipenv run pythhon sentiment.py "oh hi, i'm surprised to meet you here"
```

Example (if the terminal supports color output, it will be marked up):
```
$ pipenv run python sentiment.py "oh hi, i'm surprised to meet you here"
oh hi, i'm surprised to meet you here
Sentiment: POSITIVE
positive: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 0.68
negative:  0.01
mixed   :  0.00
neutral : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 0.31
```
