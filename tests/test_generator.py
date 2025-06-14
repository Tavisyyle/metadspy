from metadspy.generator import generate_code
from metadspy.parser import load_spec

def test_generate_code_creates_file(tmp_path):
    yaml_spec = tmp_path / "spec.yaml"
    out_file = tmp_path / "generated.py"
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
  type: ReAct
  use: TextSummarizerSignature
  tools: ["Search"]

llm:
  name: openai/gpt-4o-mini
  provider: openai
  api_key_env: OPENAI_API_KEY
  temperature: 0.5
  max_tokens: 3000

""")
    spec = load_spec(str(yaml_spec))
    generate_code(spec, output_path=str(out_file))
    assert out_file.exists()
    assert "import dspy" in out_file.read_text()
