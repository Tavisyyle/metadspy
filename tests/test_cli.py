from metadspy.cli import app
from typer.testing import CliRunner

runner = CliRunner()

def test_cli_build(tmp_path):
    yaml_spec = tmp_path / "spec.yaml"
    out_file = tmp_path / "gen.py"
    yaml_spec.write_text("""
signature:
  name: TextSummarizerSignature
  docstring: |
    Summarize the text provided as input
  inputs:
    - name: text
      kind: text
      desc: "User-provided text to summarize"
  outputs:
    - name: summary
      kind: text
      desc: "The summary of the text provided by the user."
                         
module:
  name: TextSummarizer
  type: Predict
  use: TextSummarizerSignature

llm:
  name: openai/gpt-4o-mini
  provider: openai
  api_key_env: OPENAI_API_KEY
  temperature: 0.5
  max_tokens: 3000

""")
    result = runner.invoke(
        app,
        [str(yaml_spec), "--out", str(out_file)]
    )
    print("OUTPUT:", result.output)
    assert result.exit_code == 0
    assert "wrote" in result.output
    assert out_file.exists()
