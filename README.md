# metadspy

**Metadspy**: The framework for specifying―not programming―language models.

Generate complete, reusable DSPy programs by writing simple YAML specifications. It's that easy!

---

## Installation

```bash
pip install metadspy
```

## Quickstart

1. **Write a spec** (`spec.yaml`):

   ```yaml
   signature:
     name: SentimentClassifierSignature
     docstring: |
       Classify the overall sentiment (positive, negative or neutral) of a short text.
     inputs:
       - name: text
         kind: text
         desc: "User-provided text to analyse"
     outputs:
       - name: sentiment
         kind: choices
         choices: [positive, negative, neutral]
         desc: "Predicted sentiment label"
       - name: confidence
         kind: float
         desc: "Model confidence in [0, 1]"
     instructions: >
       Respond with one sentiment label and a confidence score between 0 and 1.

   module:
     name: SentimentClassifier
     type: Predict
     use: SentimentClassifierSignature

   llm:
     name: openai/gpt-4
     provider: openai
     api_key_env: OPENAI_API_KEY
     temperature: 0.0
     max_tokens: 1000
   ```

2. **Generate your DSPy program** from the CLI:

   ```bash
   metadspy spec.yaml --out sentiment_module.py
   ```

3. **Inspect the generated code** (`sentiment_module.py`):

   ```python
   import dspy
    from dotenv import load_dotenv
    from typing import Literal

    load_dotenv()

    class SentimentClassifierSignature(dspy.Signature):
        """Classify the overall sentiment (positive, negative or neutral) of a short text."""
        text: str = dspy.InputField(desc="User-provided text to analyse")
        sentiment: Literal['positive', 'negative', 'neutral'] = dspy.OutputField(desc="Predicted sentiment label")
        confidence: float = dspy.OutputField(desc="Model confidence in [0, 1]")

    SentimentClassifierSignature = SentimentClassifierSignature.with_instructions(
        "Respond with one sentiment label and a confidence score between 0 and 1.\n"
    )

    llm = dspy.LM(
        model="openai/gpt-4o-mini",
        model_type="chat",
        temperature=0.0,
        max_tokens=1000,
        **{}
    )

    dspy.configure(lm=llm)

    SentimentClassifier = dspy.Predict(
        SentimentClassifierSignature
    )
   ```

4. **Run it**:
    You will need to add something like:

    ```python
    print(SentimentClassifier(text="DSPy is so nice."))
    ```
    Then:

   ```bash
   python sentiment_program.py
   ```

   You’ll get a `Prediction(sentiment=…, confidence=…)` object back automatically.

---

## Python API

If you prefer to script it:

```python
from metadspy.parser import load_spec
from metadspy.generator import generate_code

# Load and validate
spec = load_spec("spec.yaml")

# Render and write the DSPy program
generate_code(spec, output_path="my_dspy_program.py")
```

---

### Why Metadspy?

* **Declarative**: Focus on *what* you want, not *how* to do it.
* **Modular**: Swap LLMs, modules (Predict, ReAct, etc.), or optimizers by editing YAML.
* **Reproducible**: YAML + code generation = consistent, shareable pipelines.
* **Extensible**: Drop in custom modules, callbacks, assertions, or optimization strategies.

---

Give it a try. Specify once, ship DSPy code everywhere! 🚀 We are sooooo baaaaack !

MIT License

Project still in early stages. Enjoy !
