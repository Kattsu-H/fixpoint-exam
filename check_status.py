import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.Path(exists=True))
def q1(input):
    from apps.question1 import detect_failuer

    detect_failuer(input)


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("n", type=int)
def q2(input, n):
    from apps.question2 import detect_failuer

    detect_failuer(input, n)


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("n", type=int)
@click.argument("m", type=int)
@click.argument("t", type=int)
def q3(input, n, m, t):
    from apps.question3 import detect_failuer

    detect_failuer(input, n, m, t)


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("n", type=int)
@click.argument("m", type=int)
@click.argument("t", type=int)
def q4(input, n, m, t):
    from apps.question4 import detect_failuer

    detect_failuer(input, n, m, t)


if __name__ == "__main__":
    cli()
