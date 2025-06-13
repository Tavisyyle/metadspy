from metadspy.parser import load_spec

def test_load_yaml_spec(tmp_path):
    # Write a minimal spec to disk
    yaml_spec = tmp_path / "test.yaml"
    yaml_spec.write_text("""
signature:
  name: SentimentClassifierSignature
  docstring: |
    Classify the overall sentiment (positive, negative or neutral) of a short text.
  inputs:
    - name: text
      kind: text                  # plain string
      desc: "User-provided text to analyse"
  outputs:
    - name: sentiment
      kind: choices               # ‹choices› → Literal[…]
      choices: [positive, negative, neutral]
      desc: "Predicted sentiment label"
    - name: confidence
      kind: float
      desc: "Model confidence in [0, 1]"
  instructions: >
    Respond with one sentiment label and a confidence score between 0 and 1.

module:
  name: SentimentClassifier
  type: Predict                   # DSPy.Predict
  use: SentimentClassifierSignature

llm:
  name: openai/gpt-4o-mini
  provider: openai
  api_key_env: OPENAI_API_KEY
  temperature: 0.0                # deterministic
  max_tokens: 1000
    """)

    spec = load_spec(str(yaml_spec))
    assert spec.signature.name == "SentimentClassifierSignature"
    assert spec.signature.docstring.startswith("Classify the overall sentiment")
    assert len(spec.signature.inputs) == 1
    assert spec.signature.inputs[0].name == "text"
    assert spec.signature.inputs[0].kind == "text"
    assert len(spec.signature.outputs) == 2
    assert spec.signature.outputs[0].name == "sentiment"
    assert spec.signature.outputs[0].kind == "choices"
    assert spec.signature.outputs[0].choices == ["positive", "negative", "neutral"]
    assert spec.signature.outputs[1].name == "confidence"
    assert spec.signature.outputs[1].kind == "float"
    assert spec.signature.instructions.startswith("Respond with one sentiment label")
    assert spec.llm.name == "openai/gpt-4o-mini"
    assert spec.llm.provider == "openai"
    assert spec.llm.inferred_model == "gpt-4o-mini"
    assert spec.llm.api_key_env == "OPENAI_API_KEY"
    assert spec.llm.temperature == 0.0
    assert spec.llm.max_tokens == 1000
    assert spec.module.name == "SentimentClassifier"
    assert spec.module.type == "Predict"
    assert spec.module.use == "SentimentClassifierSignature"
    assert spec.module.callbacks is None  # No callbacks defined
    assert spec.module.build is not None  # Build method should be present
