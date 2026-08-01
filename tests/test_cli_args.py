from fuzzer.cli.args import parse_args


def test_deduplication_is_enabled_by_default():
    args = parse_args(["schema.yaml"])

    assert args.no_deduplicate is False


def test_deduplication_can_be_disabled():
    args = parse_args(["schema.yaml", "--no-deduplicate"])

    assert args.no_deduplicate is True
