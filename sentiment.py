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
        except NotADirectoryError:
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
    click.secho(sentiment, fg=color, bold=True)

    chart_char = '▇'
    chart_width = 50
    click.echo('positive: ' + click.style(chart_char * round(positive * chart_width), fg='green') + f' {positive:.2f}')
    click.echo('negative: ' + click.style(chart_char * round(negative * chart_width), fg='red') + f' {negative:.2f}')
    click.echo('mixed   : ' + click.style(chart_char * round(mixed * chart_width), fg='yellow') + f' {mixed:.2f}')
    click.echo('neutral : ' + click.style(chart_char * round(neutral * chart_width), fg='white') + f' {neutral:.2f}')


if __name__ == '__main__':
    cli()
