> [!TIP]
> **Using a coding agent?** Your agent may not know the latest Gemini API. Run `npx skills add google-gemini/gemini-skills --skill gemini-api-dev --global` to keep it current. [Set up your coding agent →](https://ai.google.dev/gemini-api/docs/coding-agents)

This quickstart shows you how to install our [libraries](https://ai.google.dev/gemini-api/docs/libraries)
and make your first Gemini API request.

## Before you begin

Using the Gemini API requires an API key, you can create one for free to get started.

[Create a Gemini API Key](https://aistudio.google.com/app/apikey)

## Install the Google GenAI SDK

### Python

Using [Python 3.9+](https://www.python.org/downloads/), install the
[`google-genai` package](https://pypi.org/project/google-genai/)
using the following
[pip command](https://packaging.python.org/en/latest/tutorials/installing-packages/):

    pip install -q -U google-genai

### JavaScript

Using [Node.js v18+](https://nodejs.org/en/download/package-manager),
install the
[Google Gen AI SDK for TypeScript and JavaScript](https://www.npmjs.com/package/@google/genai)
using the following
[npm command](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm):

    npm install @google/genai

### Go

Install
[google.golang.org/genai](https://pkg.go.dev/google.golang.org/genai) in
your module directory using the [go get command](https://go.dev/doc/code):

    go get google.golang.org/genai

### Java

If you're using Maven, you can install
[google-genai](https://github.com/googleapis/java-genai) by adding the
following to your dependencies:

    <dependencies>
      <dependency>
        <groupId>com.google.genai</groupId>
        <artifactId>google-genai</artifactId>
        <version>1.0.0</version>
      </dependency>
    </dependencies>

### C#

Install
[googleapis/go-genai](https://googleapis.github.io/dotnet-genai/) in
your module directory using the [dotnet add command](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-package-add)

    dotnet add package Google.GenAI

### Apps Script

1. To create a new Apps Script project, go to [script.new](https://script.google.com/u/0/home/projects/create).
2. Click **Untitled project**.
3. Rename the Apps Script project **AI Studio** and click **Rename**.
4. Set your [API key](https://developers.google.com/apps-script/guides/properties#manage_script_properties_manually)
   1. At the left, click **Project Settings** ![The icon for project settings](https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/settings/default/24px.svg).
   2. Under **Script Properties** click **Add script property**.
   3. For **Property** , enter the key name: `GEMINI_API_KEY`.
   4. For **Value**, enter the value for the API key.
   5. Click **Save script properties**.
5. Replace the `Code.gs` file contents with the following code:

## Make your first request

Here is an example that uses the
[`generateContent`](https://ai.google.dev/api/generate-content#method:-models.generatecontent) method
to send a request to the Gemini API using the Gemini 2.5 Flash model.

If you [set your API key](https://ai.google.dev/gemini-api/docs/api-key#set-api-env-var) as the
environment variable `GEMINI_API_KEY`, it will be picked up automatically by the
client when using the [Gemini API libraries](https://ai.google.dev/gemini-api/docs/libraries).
Otherwise you will need to [pass your API key](https://ai.google.dev/gemini-api/docs/api-key#provide-api-key-explicitly) as
an argument when initializing the client.

Note that all code samples in the Gemini API docs assume that you have set the
environment variable `GEMINI_API_KEY`.

### Python

    from google import genai

    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
    )
    print(response.text)

### JavaScript

    import { GoogleGenAI } from "@google/genai";

    // The client gets the API key from the environment variable `GEMINI_API_KEY`.
    const ai = new GoogleGenAI({});

    async function main() {
      const response = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: "Explain how AI works in a few words",
      });
      console.log(response.text);
    }

    main();

### Go

    package main

    import (
        "context"
        "fmt"
        "log"
        "google.golang.org/genai"
    )

    func main() {
        ctx := context.Background()
        // The client gets the API key from the environment variable `GEMINI_API_KEY`.
        client, err := genai.NewClient(ctx, nil)
        if err != nil {
            log.Fatal(err)
        }

        result, err := client.Models.GenerateContent(
            ctx,
            "gemini-3-flash-preview",
            genai.Text("Explain how AI works in a few words"),
            nil,
        )
        if err != nil {
            log.Fatal(err)
        }
        fmt.Println(result.Text())
    }

### Java

    package com.example;

    import com.google.genai.Client;
    import com.google.genai.types.GenerateContentResponse;

    public class GenerateTextFromTextInput {
      public static void main(String[] args) {
        // The client gets the API key from the environment variable `GEMINI_API_KEY`.
        Client client = new Client();

        GenerateContentResponse response =
            client.models.generateContent(
                "gemini-3-flash-preview",
                "Explain how AI works in a few words",
                null);

        System.out.println(response.text());
      }
    }

### C#

    using System.Threading.Tasks;
    using Google.GenAI;
    using Google.GenAI.Types;

    public class GenerateContentSimpleText {
      public static async Task main() {
        // The client gets the API key from the environment variable `GEMINI_API_KEY`.
        var client = new Client();
        var response = await client.Models.GenerateContentAsync(
          model: "gemini-3-flash-preview", contents: "Explain how AI works in a few words"
        );
        Console.WriteLine(response.Candidates[0].Content.Parts[0].Text);
      }
    }

### Apps Script

    // See https://developers.google.com/apps-script/guides/properties
    // for instructions on how to set the API key.
    const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
    function main() {
      const payload = {
        contents: [
          {
            parts: [
              { text: 'Explain how AI works in a few words' },
            ],
          },
        ],
      };

      const url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent';
      const options = {
        method: 'POST',
        contentType: 'application/json',
        headers: {
          'x-goog-api-key': apiKey,
        },
        payload: JSON.stringify(payload)
      };

      const response = UrlFetchApp.fetch(url, options);
      const data = JSON.parse(response);
      const content = data['candidates'][0]['content']['parts'][0]['text'];
      console.log(content);
    }

### REST

    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H 'Content-Type: application/json' \
      -X POST \
      -d '{
        "contents": [
          {
            "parts": [
              {
                "text": "Explain how AI works in a few words"
              }
            ]
          }
        ]
      }'

## What's next

Now that you made your first API request, you might want to explore the
following guides that show Gemini in action:

- [Text generation](https://ai.google.dev/gemini-api/docs/text-generation)
- [Image generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Image understanding](https://ai.google.dev/gemini-api/docs/image-understanding)
- [Thinking](https://ai.google.dev/gemini-api/docs/thinking)
- [Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Long context](https://ai.google.dev/gemini-api/docs/long-context)
- [Embeddings](https://ai.google.dev/gemini-api/docs/embeddings)

---

# Models Available : 


*** ** * ** ***

> [!WARNING]
> **Warning:** Gemini 3 Pro Preview is [deprecated](https://ai.google.dev/gemini-api/docs/deprecations) and has been shut down March 9, 2026. Migrate to [Gemini 3.1 Pro Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview) to avoid service disruption.

## Gemini 3

[### Gemini 3.1 Pro
Advanced intelligence, complex problem-solving skills, and powerful agentic and vibe coding capabilities.
New Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview) [### Gemini 3 Flash
Frontier-class performance rivaling larger models at a fraction of the cost.
Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3-flash-preview) [### Gemini 3.1 Flash-Lite
Frontier-class performance rivaling larger models at a fraction of the cost.
New Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-preview) [### Nano Banana 2
Powerful, high-efficiency image generation and editing, optimized for speed and high-volume use cases.
Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image-preview) [### Nano Banana Pro
State-of-the-art image generation and editing models for highly contextual native image creation.
Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview)

*** ** * ** ***

## Gemini 2.5 Flash

### [Gemini 2.5 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash)

Our best price-performance model for low-latency, high-volume tasks that require reasoning.

### [Nano Banana](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image)

State-of-the-art native image generation and editing designed for fast, creative workflows.

### [Gemini 2.5 Flash Live Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-native-audio-preview-12-2025)

Optimized for real-time conversational agents with sub-second native audio streaming.

### [Gemini 2.5 Flash TTS Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-preview-tts)

Controllable text-to-speech audio generation with fine control over style and pacing.

*** ** * ** ***

## Gemini 2.5 Flash-Lite

### [Gemini 2.5 Flash-Lite](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-lite)

The fastest and most budget-friendly multimodal model in the 2.5 family.

*** ** * ** ***

## Gemini 2.5 Pro

### [Gemini 2.5 Pro](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro)

Our most advanced model for complex tasks, featuring deep reasoning and coding capabilities.

### [Gemini 2.5 Pro TTS Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro-preview-tts)

High-fidelity speech synthesis optimized for quality in structured workflows like podcasts and audiobooks.

*** ** * ** ***

## Audio models

*This section contains all audio models, including ones that may already be listed in other sections*

### [Gemini 2.5 Flash Live Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-native-audio-preview-12-2025)

Our flagship Live API model for low-latency, bidirectional voice and video agents with native audio reasoning.

### [Gemini 2.5 Flash TTS Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-preview-tts)

Fast and controllable text-to-speech for low-latency, cost-efficient applications and real-time assistants.

### [Gemini 2.5 Pro TTS Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro-preview-tts)

High-fidelity speech synthesis optimized for quality in structured workflows like podcasts and audiobooks.

### [Lyria Experimental](https://ai.google.dev/gemini-api/docs/models/lyria-realtime-exp)

High-fidelity music generation model providing granular creative control over instruments, BPM, and complex compositions.

*** ** * ** ***

## Generative media models

*This section contains all generative media models, including ones that may already be listed in other sections*

### [Nano Banana 2 Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image-preview)

High-efficiency production-scale visual creation, combining the intelligence of the Gemini 3 series with lightning-fast generation speeds.

### [Veo 3.1 Preview](https://ai.google.dev/gemini-api/docs/models/veo-3.1-generate-preview)

State-of-the-art cinematic video generation with advanced creative controls and natively synchronized audio.

### [Nano Banana Pro Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview)

A professional design engine with a reasoning core for studio-quality 4K visuals, complex layouts, and precise text rendering.

### [Lyria Experimental](https://ai.google.dev/gemini-api/docs/models/lyria-realtime-exp)

High-fidelity music generation model providing granular creative control over instruments, BPM, and complex compositions.

### [Nano Banana](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image)

State-of-the-art native image generation and editing designed for fast, creative workflows.

### [Imagen 4](https://ai.google.dev/gemini-api/docs/models/imagen)

Text-to-image model yet, featuring fast and ultra-fast generation and exceptional clarity up to 2K resolution.

*** ** * ** ***

## Tool and agent models

### [Computer Use Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-computer-use-preview-10-2025)

A specialized model that can "see" a digital screen and perform UI actions like clicking, typing, and navigating to automate complex browser tasks.

### [Gemini Deep Research Preview](https://ai.google.dev/gemini-api/docs/models/deep-research-pro-preview-12-2025)

An agentic model that autonomously plans and executes multi-step research across hundreds of sources to produce cited, interactive reports.

*** ** * ** ***

## Specialized task models

### [Gemini Embedding 2 Preview](https://ai.google.dev/gemini-api/docs/models/gemini-embedding-2-preview)

Our first multimodal embedding model, mapping text, images, video, audio, and PDFs into a unified embedding space for advanced semantic search and RAG systems.

### [Gemini Embedding](https://ai.google.dev/gemini-api/docs/models/gemini-embedding-001)

High-dimensional vector representations for advanced semantic search, text classification, and RAG systems.

### [Gemini Robotics Preview](https://ai.google.dev/gemini-api/docs/models/gemini-robotics-er-1.5-preview)

Advanced embodied reasoning model that understands physical spaces and plans multi-step tasks for robotic agents.

*** ** * ** ***

## Previous models

> [!WARNING]
> These models are [deprecated](https://ai.google.dev/gemini-api/docs/deprecations) and will be shut down soon; migrate to newer models to prevent service interruptions.

### [Gemini 2.0 Flash Deprecated](https://ai.google.dev/gemini-api/docs/models/gemini-2.0-flash)

Our second generation workhorse model, with next-gen features and improved capabilities, including superior speed, native tool use, and a 1M token context window.

### [Gemini 2.0 Flash-Lite Deprecated](https://ai.google.dev/gemini-api/docs/models/gemini-2.0-flash-lite)

Our fastest second generation model, optimized for cost efficiency and low latency.

### [Gemini 3 Pro Preview Shut down](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-preview)

Our state-of-the-art reasoning model, with advanced multimodal understanding.

*** ** * ** ***

## Model version name patterns

Gemini models are available in either *stable* , *preview* , *latest* , or
*experimental* versions.

> [!NOTE]
> **Note:** The following list refers to the model string naming convention as of September, 2025. Models released prior to that may have different naming conventions. Refer to the exact model string if you are using an older model.

### Stable

Points to a specific stable model. Stable models usually don't change. Most
production apps should use a specific stable model.

For example: `gemini-2.5-flash`.

### Preview

Points to a preview model which may be used for production. Preview models will
typically have billing enabled, might come with more restrictive rate limits and
will be deprecated with at least 2 weeks notice.

For example: `gemini-2.5-flash-preview-09-2025`.

### Latest

Points to the latest release for a specific model variation. This can be a
stable, preview or experimental release. This alias will get hot-swapped with
every new release of a specific model variation. A **2-week notice** will
be provided through email before the version behind latest is changed.

For example: `gemini-flash-latest`.

### Experimental

Points to an experimental model which will typically be not be suitable for
production use and come with more restrictive rate limits. We release
experimental models to gather feedback and get our latest updates into the hands
of developers quickly.

Experimental models are not stable and availability of model endpoints is
subject to change.

## Model deprecations

For information about model deprecations, visit the [Gemini deprecations](https://ai.google.dev/gemini-api/docs/deprecations) page.