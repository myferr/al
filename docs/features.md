## Features

- **Conversational AI**: Powered by a local Ollama model (defaulting to `llama3`), Al can engage in dynamic conversations.
- **Contextual Memory**: All user messages and Al's responses are saved to `memory.jsonl`, enabling the bot to learn from past interactions and maintain conversational context.
- **Flexible Interaction**: Al responds when directly pinged (`@Al your message`) or when a user replies to one of Al's messages. The ping does not need to be at the start of the message.
- **Customizable Personality**: A `SYSTEM_PROMPT` in the code defines Al's persona and tone.
- **Typing Indicator**: Al shows a "typing..." indicator while generating a response for a smoother user experience.
