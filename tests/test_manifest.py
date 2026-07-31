from fuzzer.utils.manifest import sha256_source_tree


def test_source_tree_hash_changes_with_executable_source(tmp_path):
    source = tmp_path / "src" / "fuzzer"
    source.mkdir(parents=True)
    module = source / "module.py"
    module.write_text("VALUE = 1\n", encoding="utf-8")

    first_hash = sha256_source_tree(tmp_path)
    module.write_text("VALUE = 2\n", encoding="utf-8")
    second_hash = sha256_source_tree(tmp_path)

    assert first_hash != second_hash


def test_source_tree_hash_ignores_runtime_output(tmp_path):
    source = tmp_path / "src" / "fuzzer"
    source.mkdir(parents=True)
    (source / "module.py").write_text("VALUE = 1\n", encoding="utf-8")

    first_hash = sha256_source_tree(tmp_path)
    output = tmp_path / "output"
    output.mkdir()
    (output / "results.json").write_text("[]\n", encoding="utf-8")

    assert sha256_source_tree(tmp_path) == first_hash
