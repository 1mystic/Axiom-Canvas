# Developer quickstart

import {
  Assistant,
  Camera,
  ChatTripleDots,
  Code,
  Bolt,
  Speed,
  SquarePlus,
} from "@components/react/oai/platform/ui/Icon.react";


















The OpenAI API provides a simple interface to state-of-the-art AI [models](https://developers.openai.com/api/docs/models) for text generation, natural language processing, computer vision, and more. Get started by creating an API Key and running your first API call. Discover how to generate text, analyze images, build agents, and more.

## Create and export an API key



StatsigClient.logEvent("quickstart_create_api_key_click", null, null)
  }
>
  Create an API Key


<p></p>
Before you begin, create an API key in the dashboard, which you'll use to
securely [access the API](https://developers.openai.com/api/docs/api-reference/authentication). Store the key
in a safe location, like a [`.zshrc`
file](https://www.freecodecamp.org/news/how-do-zsh-configuration-files-work/) or
another text file on your computer. Once you've generated an API key, export it
as an [environment variable](https://en.wikipedia.org/wiki/Environment_variable)
in your terminal.



<div data-content-switcher-pane data-value="macOS">
    <div class="hidden">macOS / Linux</div>
    Export an environment variable on macOS or Linux systems

```bash
export OPENAI_API_KEY="your_api_key_here"
```

  </div>
  <div data-content-switcher-pane data-value="windows" hidden>
    <div class="hidden">Windows</div>
    Export an environment variable in PowerShell

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

  </div>



OpenAI SDKs are configured to automatically read your API key from the system environment.

## Install the OpenAI SDK and Run an API Call



<div data-content-switcher-pane data-value="javascript">
    <div class="hidden">JavaScript</div>
    </div>
  <div data-content-switcher-pane data-value="python" hidden>
    <div class="hidden">Python</div>
    </div>
  <div data-content-switcher-pane data-value="csharp" hidden>
    <div class="hidden">.NET</div>
    </div>
  <div data-content-switcher-pane data-value="java" hidden>
    <div class="hidden">Java</div>
    </div>
  <div data-content-switcher-pane data-value="golang" hidden>
    <div class="hidden">Go</div>
    </div>


<a
  href="https://github.com/openai/openai-responses-starter-app"
  target="_blank"
  rel="noreferrer"
>
  

<span slot="icon">
      </span>
    Start building with the Responses API.


</a>

[

<span slot="icon">
      </span>
    Learn more about prompting, message roles, and building conversational apps.

](https://developers.openai.com/api/docs/guides/text)

## Add credits to keep building



StatsigClient.logEvent("quickstart_add_credits_billing_click", null, null)
  }
>
  Go to billing


{/* prettier-ignore */}
<div className="mt-2">Congrats on running a free test API request! Start building real applications with higher limits and use <a href="/api/docs/models" target="_blank">our models</a> to generate text, audio, images, videos and more.</div>

<div className="mt-2">
  Access dashboard features designed to help you ship faster:
</div>
<a
  href="https://platform.openai.com/chat"
  target="_blank"
  rel="noreferrer"
  onClick={() =>
    StatsigClient.logEvent(
      "quickstart_add_credits_chat_playground_click",
      null,
      null
    )
  }
>
  

<span slot="icon">
      </span>
    Build & test conversational prompts and embed them in your app.


</a>
<a
  href="https://platform.openai.com/agent-builder"
  target="_blank"
  rel="noreferrer"
  onClick={() =>
    StatsigClient.logEvent(
      "quickstart_add_credits_agent_builder_click",
      null,
      null
    )
  }
>
  

<span slot="icon">
      </span>
    Build, deploy, and optimize agent workflows.


</a>

## Analyze images and files

Send image URLs, uploaded files, or PDF documents directly to the model to extract text, classify content, or detect visual elements.



<div data-content-switcher-pane data-value="image-url">
    <div class="hidden">Image URL</div>
    </div>
  <div data-content-switcher-pane data-value="file-url" hidden>
    <div class="hidden">File URL</div>
    Use a file URL as input

```bash
curl "https://api.openai.com/v1/responses" \\
    -H "Content-Type: application/json" \\
    -H "Authorization: Bearer $OPENAI_API_KEY" \\
    -d '{
        "model": "gpt-5",
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Analyze the letter and provide a summary of the key points."
                    },
                    {
                        "type": "input_file",
                        "file_url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf"
                    }
                ]
            }
        ]
    }'
```

```javascript
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-5",
    input: [
        {
            role: "user",
            content: [
                {
                    type: "input_text",
                    text: "Analyze the letter and provide a summary of the key points.",
                },
                {
                    type: "input_file",
                    file_url: "https://www.berkshirehathaway.com/letters/2024ltr.pdf",
                },
            ],
        },
    ],
});

console.log(response.output_text);
```

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Analyze the letter and provide a summary of the key points.",
                },
                {
                    "type": "input_file",
                    "file_url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf",
                },
            ],
        },
    ]
)

print(response.output_text)
```

```csharp
using OpenAI.Files;
using OpenAI.Responses;

string key = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
OpenAIResponseClient client = new(model: "gpt-5", apiKey: key);

using HttpClient http = new();
using Stream stream = await http.GetStreamAsync("https://www.berkshirehathaway.com/letters/2024ltr.pdf");
OpenAIFileClient files = new(key);
OpenAIFile file = files.UploadFile(stream, "2024ltr.pdf", FileUploadPurpose.UserData);

OpenAIResponse response = (OpenAIResponse)client.CreateResponse([
    ResponseItem.CreateUserMessageItem([
        ResponseContentPart.CreateInputTextPart("Analyze the letter and provide a summary of the key points."),
        ResponseContentPart.CreateInputFilePart(file.Id),
    ]),
]);

Console.WriteLine(response.GetOutputText());
```

  </div>
  <div data-content-switcher-pane data-value="file-upload" hidden>
    <div class="hidden">Upload file</div>
    Upload a file and use it as input

```bash
curl https://api.openai.com/v1/files \\
    -H "Authorization: Bearer $OPENAI_API_KEY" \\
    -F purpose="user_data" \\
    -F file="@draconomicon.pdf"

curl "https://api.openai.com/v1/responses" \\
    -H "Content-Type: application/json" \\
    -H "Authorization: Bearer $OPENAI_API_KEY" \\
    -d '{
        "model": "gpt-5",
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": "file-6F2ksmvXxt4VdoqmHRw6kL"
                    },
                    {
                        "type": "input_text",
                        "text": "What is the first dragon in the book?"
                    }
                ]
            }
        ]
    }'
```

```javascript
import fs from "fs";
import OpenAI from "openai";
const client = new OpenAI();

const file = await client.files.create({
    file: fs.createReadStream("draconomicon.pdf"),
    purpose: "user_data",
});

const response = await client.responses.create({
    model: "gpt-5",
    input: [
        {
            role: "user",
            content: [
                {
                    type: "input_file",
                    file_id: file.id,
                },
                {
                    type: "input_text",
                    text: "What is the first dragon in the book?",
                },
            ],
        },
    ],
});

console.log(response.output_text);
```

```python
from openai import OpenAI
client = OpenAI()

file = client.files.create(
    file=open("draconomicon.pdf", "rb"),
    purpose="user_data"
)

response = client.responses.create(
    model="gpt-5",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": file.id,
                },
                {
                    "type": "input_text",
                    "text": "What is the first dragon in the book?",
                },
            ]
        }
    ]
)

print(response.output_text)
```

```csharp
using OpenAI.Files;
using OpenAI.Responses;

string key = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
OpenAIResponseClient client = new(model: "gpt-5", apiKey: key);

OpenAIFileClient files = new(key);
OpenAIFile file = files.UploadFile("draconomicon.pdf", FileUploadPurpose.UserData);

OpenAIResponse response = (OpenAIResponse)client.CreateResponse([
    ResponseItem.CreateUserMessageItem([
        ResponseContentPart.CreateInputFilePart(file.Id),
        ResponseContentPart.CreateInputTextPart("What is the first dragon in the book?"),
    ]),
]);

Console.WriteLine(response.GetOutputText());
```

  </div>



[

<span slot="icon">
      </span>
    Learn to use image inputs to the model and extract meaning from images.

](https://developers.openai.com/api/docs/guides/images)

[

<span slot="icon">
      </span>
    Learn to use file inputs to the model and extract meaning from documents.

](https://developers.openai.com/api/docs/guides/file-inputs)

## Extend the model with tools

Give the model access to external data and functions by attaching [tools](https://developers.openai.com/api/docs/guides/tools). Use built-in tools like web search or file search, or define your own for calling APIs, running code, or integrating with third-party systems.



<div data-content-switcher-pane data-value="web-search">
    <div class="hidden">Web search</div>
    </div>
  <div data-content-switcher-pane data-value="file-search" hidden>
    <div class="hidden">File search</div>
    Search your files in a response

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="What is deep research by OpenAI?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["<vector_store_id>"]
    }]
)
print(response)
```

```javascript
import OpenAI from "openai";
const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "What is deep research by OpenAI?",
    tools: [
        {
            type: "file_search",
            vector_store_ids: ["<vector_store_id>"],
        },
    ],
});
console.log(response);
```

```csharp
using OpenAI.Responses;

string key = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
OpenAIResponseClient client = new(model: "gpt-5", apiKey: key);

ResponseCreationOptions options = new();
options.Tools.Add(ResponseTool.CreateFileSearchTool(["<vector_store_id>"]));

OpenAIResponse response = (OpenAIResponse)client.CreateResponse([
    ResponseItem.CreateUserMessageItem([
        ResponseContentPart.CreateInputTextPart("What is deep research by OpenAI?"),
    ]),
], options);

Console.WriteLine(response.GetOutputText());
```

  </div>
  <div data-content-switcher-pane data-value="function-calling" hidden>
    <div class="hidden">Function calling</div>
    </div>
  <div data-content-switcher-pane data-value="remote-mcp" hidden>
    <div class="hidden">Remote MCP</div>
    Call a remote MCP server

```bash
curl https://api.openai.com/v1/responses \\ 
-H "Content-Type: application/json" \\ 
-H "Authorization: Bearer $OPENAI_API_KEY" \\ 
-d '{
  "model": "gpt-5",
    "tools": [
      {
        "type": "mcp",
        "server_label": "dmcp",
        "server_description": "A Dungeons and Dragons MCP server to assist with dice rolling.",
        "server_url": "https://dmcp-server.deno.dev/sse",
        "require_approval": "never"
      }
    ],
    "input": "Roll 2d4+1"
  }'
```

```javascript
import OpenAI from "openai";
const client = new OpenAI();

const resp = await client.responses.create({
  model: "gpt-5",
  tools: [
    {
      type: "mcp",
      server_label: "dmcp",
      server_description: "A Dungeons and Dragons MCP server to assist with dice rolling.",
      server_url: "https://dmcp-server.deno.dev/sse",
      require_approval: "never",
    },
  ],
  input: "Roll 2d4+1",
});

console.log(resp.output_text);
```

```python
from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-5",
    tools=[
        {
            "type": "mcp",
            "server_label": "dmcp",
            "server_description": "A Dungeons and Dragons MCP server to assist with dice rolling.",
            "server_url": "https://dmcp-server.deno.dev/sse",
            "require_approval": "never",
        },
    ],
    input="Roll 2d4+1",
)

print(resp.output_text)
```

```csharp
using OpenAI.Responses;

string key = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
OpenAIResponseClient client = new(model: "gpt-5", apiKey: key);

ResponseCreationOptions options = new();
options.Tools.Add(ResponseTool.CreateMcpTool(
    serverLabel: "dmcp",
    serverUri: new Uri("https://dmcp-server.deno.dev/sse"),
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(GlobalMcpToolCallApprovalPolicy.NeverRequireApproval)
));

OpenAIResponse response = (OpenAIResponse)client.CreateResponse([
    ResponseItem.CreateUserMessageItem([
        ResponseContentPart.CreateInputTextPart("Roll 2d4+1")
    ])
], options);

Console.WriteLine(response.GetOutputText());
```

  </div>



[

<span slot="icon">
      </span>
    Learn about powerful built-in tools like web search and file search.

](https://developers.openai.com/api/docs/guides/tools)

[

<span slot="icon">
      </span>
    Learn to enable the model to call your own custom code.

](https://developers.openai.com/api/docs/guides/function-calling)

## Stream responses and build realtime apps

Use server‑sent [streaming events](https://developers.openai.com/api/docs/guides/streaming-responses) to show results as they’re generated, or the [Realtime API](https://developers.openai.com/api/docs/guides/realtime) for interactive voice and multimodal apps.

[

<span slot="icon">
      </span>
    Use server-sent events to stream model responses to users fast.

](https://developers.openai.com/api/docs/guides/streaming-responses)

[

<span slot="icon">
      </span>
    Use WebRTC or WebSockets for super fast speech-to-speech AI apps.

](https://developers.openai.com/api/docs/guides/realtime)

## Build agents

Use the OpenAI platform to build [agents](https://developers.openai.com/api/docs/guides/agents) capable of taking action—like [controlling computers](https://developers.openai.com/api/docs/guides/tools-computer-use)—on behalf of your users. Use the Agents SDK for [Python](https://openai.github.io/openai-agents-python) or [TypeScript](https://openai.github.io/openai-agents-js) to create orchestration logic on the backend.

[

<span slot="icon">
      </span>
    Learn how to use the OpenAI platform to build powerful, capable AI agents.

](https://developers.openai.com/api/docs/guides/agents)

Frontier models
OpenAI's most advanced models, recommended for most tasks.
gpt-5.4
GPT-5.4
Best intelligence at scale for agentic, coding, and professional workflows
gpt-5.4-pro
GPT-5.4 pro
Version of GPT-5.4 that produces smarter and more precise responses.
gpt-5-mini
GPT-5 mini
Near-frontier intelligence for cost sensitive, low latency, high volume workloads
gpt-5-nano
GPT-5 nano
Fastest, most cost-efficient version of GPT-5
gpt-5
GPT-5
Previous intelligent reasoning model for coding and agentic tasks with configurable reasoning effort
gpt-4.1
GPT-4.1
Smartest non-reasoning model
Image
Models for image generation and editing.
gpt-image-1.5
GPT Image 1.5
State-of-the-art image generation model.
chatgpt-image-latest
chatgpt-image-latest
Image model used in ChatGPT.
gpt-image-1
GPT Image 1
Our previous image generation model
gpt-image-1-mini
gpt-image-1-mini
A cost-efficient version of GPT Image 1
dall-e-3
DALL·E 3
Deprecated
Previous generation image generation model
dall-e-2
DALL·E 2
Deprecated
Our first image generation model
Video
Models for video generation.
sora-2
Sora 2
Flagship video generation with synced audio
sora-2-pro
Sora 2 Pro
Most advanced synced-audio video generation
Realtime & audio
Models for realtime, speech, and audio workflows.
gpt-realtime-1.5
gpt-realtime-1.5
The best voice model for audio in, audio out.
gpt-realtime
gpt-realtime
Model capable of realtime text and audio inputs and outputs
gpt-realtime-mini
gpt-realtime-mini
A cost-efficient version of GPT Realtime
gpt-audio-1.5
gpt-audio-1.5
The best voice model for audio in, audio out with Chat Completions.
gpt-audio
gpt-audio
For audio inputs and outputs with Chat Completions API
gpt-audio-mini
gpt-audio-mini
A cost-efficient version of GPT Audio
gpt-4o-audio-preview
GPT-4o Audio
GPT-4o models capable of audio inputs and outputs
gpt-4o-mini-audio-preview
GPT-4o mini Audio
Smaller model capable of audio inputs and outputs
gpt-4o-realtime-preview
GPT-4o Realtime
Model capable of realtime text and audio inputs and outputs
gpt-4o-mini-realtime-preview
GPT-4o mini Realtime
Smaller realtime model for text and audio inputs and outputs
gpt-4o-transcribe
GPT-4o Transcribe
Speech-to-text model powered by GPT-4o
gpt-4o-mini-transcribe
GPT-4o mini Transcribe
Speech-to-text model powered by GPT-4o mini
gpt-4o-transcribe-diarize
GPT-4o Transcribe Diarize
Transcription model that identifies who's speaking when
gpt-4o-mini-tts
GPT-4o mini TTS
Text-to-speech model powered by GPT-4o mini
tts-1
TTS-1
Text-to-speech model optimized for speed
tts-1-hd
TTS-1 HD
Text-to-speech model optimized for quality
whisper-1
Whisper
General-purpose speech recognition model
Coding
Models optimized for software engineering tasks.
gpt-5-codex
GPT-5-Codex
A version of GPT-5 optimized for agentic coding in Codex
gpt-5.3-codex
GPT-5.3-Codex
The most capable agentic coding model to date.
gpt-5.2-codex
GPT-5.2-Codex
Our most intelligent coding model optimized for long-horizon, agentic coding tasks.
gpt-5.1-codex
GPT-5.1 Codex
A version of GPT-5.1 optimized for agentic coding in Codex.
gpt-5.1-codex-max
GPT-5.1-Codex-Max
A version of GPT-5.1-codex optimized for long running tasks.
gpt-5.1-codex-mini
GPT-5.1 Codex mini
Smaller, more cost-effective, less-capable version of GPT-5.1-Codex
codex-mini-latest
codex-mini-latest
Deprecated
Fast reasoning model optimized for the Codex CLI
Deep research
Models built for deep research tasks.
o3-deep-research
o3-deep-research
Our most powerful deep research model
o4-mini-deep-research
o4-mini-deep-research
Faster, more affordable deep research model
Open-weight models
Open-weight models under a permissive Apache 2.0 license.
gpt-oss-120b
gpt-oss-120b
Most powerful open-weight model, fits into an H100 GPU
gpt-oss-20b
gpt-oss-20b
Medium-sized open-weight model for low latency
More models
Diverse models for a variety of tasks.
gpt-5.2
GPT-5.2
Previous frontier model for professional work with configurable reasoning effort
gpt-5.1
GPT-5.1
The best model for coding and agentic tasks with configurable reasoning effort
gpt-5.2-pro
GPT-5.2 pro
Previous pro model for professional work that produces smarter and more precise responses.
gpt-5-pro
GPT-5 pro
Version of GPT-5 that produces smarter and more precise responses
o3-pro
o3-pro
Version of o3 with more compute for better responses
o3
o3
Reasoning model for complex tasks, succeeded by GPT-5
o4-mini
o4-mini
Fast, cost-efficient reasoning model, succeeded by GPT-5 mini
gpt-4.1-mini
GPT-4.1 mini
Smaller, faster version of GPT-4.1
gpt-4.1-nano
GPT-4.1 nano
Fastest, most cost-efficient version of GPT-4.1
o1-pro
o1-pro
Version of o1 with more compute for better responses
computer-use-preview
computer-use-preview
Specialized model for computer use tool
gpt-4o-mini-search-preview
GPT-4o mini Search Preview
Fast, affordable small model for web search
gpt-4o-search-preview
GPT-4o Search Preview
GPT model for web search in Chat Completions
gpt-4.5-preview
GPT-4.5 Preview (Deprecated)
Deprecated large model.
o3-mini
o3-mini
A small model alternative to o3
o1
o1
Previous full o-series reasoning model
omni-moderation-latest
omni-moderation
Identify potentially harmful content in text and images
o1-mini
o1-mini
Deprecated
A small model alternative to o1
o1-preview
o1 Preview
Deprecated
Preview of our first o-series reasoning model
gpt-4o
GPT-4o
Fast, intelligent, flexible GPT model
gpt-4o-mini
GPT-4o mini
Fast, affordable small model for focused tasks
gpt-4-turbo
GPT-4 Turbo
An older high-intelligence GPT model
babbage-002
babbage-002
Deprecated
Replacement for the GPT-3 ada and babbage base models
chatgpt-4o-latest
ChatGPT-4o
Deprecated
GPT-4o model used in ChatGPT
davinci-002
davinci-002
Deprecated
Replacement for the GPT-3 curie and davinci base models
gpt-3.5-turbo
GPT-3.5 Turbo
Legacy GPT model for cheaper chat and non-chat tasks
gpt-4
GPT-4
An older high-intelligence GPT model
gpt-4-turbo-preview
GPT-4 Turbo Preview
Deprecated
An older fast GPT model
gpt-5.3-chat-latest
GPT-5.3 Chat
GPT-5.3 Instant model used in ChatGPT
gpt-5.2-chat-latest
GPT-5.2 Chat
GPT-5.2 model used in ChatGPT
gpt-5.1-chat-latest
GPT-5.1 Chat
GPT-5.1 model used in ChatGPT
gpt-5-chat-latest
GPT-5 Chat
GPT-5 model used in ChatGPT
text-embedding-3-large
text-embedding-3-large
Most capable embedding model
text-embedding-3-small
text-embedding-3-small
Small embedding model
text-embedding-ada-002
text-embedding-ada-002
Older embedding model
text-moderation-latest
text-moderation
Deprecated
Previous generation text-only moderation model
text-moderation-stable
text-moderation-stable
Deprecated
Previous generation text-only moderation model
ChatGPT models
Models used in ChatGPT, not recommended for API use.
gpt-5-chat-latest
GPT-5 Chat
GPT-5 model used in ChatGPT
chatgpt-4o-latest
ChatGPT-4o
Deprecated
GPT-4o model used in ChatGPT