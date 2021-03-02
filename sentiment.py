import boto3
import click
import subprocess

@click.command()
@click.argument('text', nargs=-1)
def cli(text):
    combined_text = ' '.join(text)
    if len(combined_text) == 0:
        try:
            pbpaste_result = subprocess.check_output(['pbpaste'])
            combined_text = str(pbpaste_result, 'utf8')
        except (FileNotFoundError, subprocess.SubprocessError):
            combined_text = 'hi, how are you? it is lovely to meet'

    aws_session = boto3.Session()
    comprehend_client = aws_session.client('comprehend')

    resp = comprehend_client.detect_sentiment(
        LanguageCode='en',
        Text=combined_text
    )
    sentiment = resp['Sentiment']
    scores = resp['SentimentScore']
    positive = scores['Positive']
    negative = scores['Negative']
    neutral = scores['Neutral']
    mixed = scores['Mixed']

    if sentiment == 'POSITIVE':
        color = 'green'
    elif sentiment == 'NEGATIVE':
        color = 'red'
    elif sentiment == 'MIXED':
        color = 'yellow'
    else:
        color = 'white'
    click.echo(combined_text)
    click.echo('Sentiment: ', nl='')
    sentiment_styled = click.style(sentiment, fg=color, bold=True)
    click.echo(sentiment_styled)

    chart_char = '▇'
    chart_width = 50
    click.echo('positive: ' + click.style(chart_char * round(positive * chart_width), fg='green') + f' {positive:.2f}')
    click.echo('negative: ' + click.style(chart_char * round(negative * chart_width), fg='red') + f' {negative:.2f}')
    click.echo('mixed   : ' + click.style(chart_char * round(mixed * chart_width), fg='yellow') + f' {mixed:.2f}')
    click.echo('neutral : ' + click.style(chart_char * round(neutral * chart_width), fg='white') + f' {neutral:.2f}')

    word_count = len(combined_text.split())
    _reminders(word_count, sentiment_styled)


def _reminders(word_count: int, sentiment_styled: str):
    click.echo()
    click.echo('\tTips for communicating over slack and email:')

    word_count_color = 'green'
    if word_count < 10:
        word_count_color = 'red'
    elif word_count < 30:
        word_count_color = 'yellow'

    click.echo(click.style('\t\t1. Is my email/slack too brief?', bold=True) + click.style(f' Words: {word_count}', fg=word_count_color))
    click.echo(click.style('\t\t2. Are there any typos?', bold=True))  # FIXME: check for typos 2021-03-01
    click.echo(click.style('\t\t3. What tone am I projecting?', bold=True) + f' Sentiment is {sentiment_styled}')
    click.echo(click.style('\t\t4. Would it be helpful to talk instead?', bold=True))
    click.echo(f'\t\t\tProbably! Make sure to consider this especially if this thread has gone back and forth more than twice.')
    click.echo()


if __name__ == '__main__':
    cli()
