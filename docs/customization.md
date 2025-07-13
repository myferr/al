## Customization

You can modify the following variables in `src/settings.py` or `src/ollama_client.py`:

| Variable        | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `OLLAMA_MODEL`  | Name of the model to use (`llama3`, `mistral`, `phi3`, etc.) |
| `OLLAMA_HOST`   | URL to your running Ollama server                            |
| `SYSTEM_PROMPT` | Defines Al’s personality and tone                            |
| `MEMORY_FILE`   | Path to Al’s message history file (default: `memory.jsonl`)  |

### Example: Custom SYSTEM_PROMPT

```python
SYSTEM_PROMPT = "You are Al, a helpful assistant that specializes in ancient history. You always respond with a historical fact."
```
