# Get started with Claude

Make your first API call to Claude and build a simple web search assistant.

---

## Prerequisites

- An Anthropic [Console account](/)
- An [API key](/settings/keys)

## Call the API

<Tabs>
  <Tab title="cURL">
    <Steps>
      <Step title="Set your API key">
        Get your API key from the [Claude Console](/settings/keys) and set it as an environment variable:

        ```bash
        export ANTHROPIC_API_KEY='your-api-key-here'
        ```
      </Step>

      <Step title="Make your first API call">
        Run this command to create a simple web search assistant:

        ```bash
        curl https://api.anthropic.com/v1/messages \
          -H "Content-Type: application/json" \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -d '{
            "model": "claude-opus-4-6",
            "max_tokens": 1000,
            "messages": [
              {
                "role": "user",
                "content": "What should I search for to find the latest developments in renewable energy?"
              }
            ]
          }'
        ```

        **Example output:**
        ```json
        {
          "id": "msg_01HCDu5LRGeP2o7s2xGmxyx8",
          "type": "message",
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "Here are some effective search strategies to find the latest renewable energy developments:\n\n## Search Terms to Use:\n- \"renewable energy news 2024\"\n- \"clean energy breakthrough\"\n- \"solar/wind/battery technology advances\"\n- \"green energy innovations\"\n- \"climate tech developments\"\n- \"energy storage solutions\"\n\n## Best Sources to Check:\n\n**News & Industry Sites:**\n- Renewable Energy World\n- GreenTech Media (now Wood Mackenzie)\n- Energy Storage News\n- CleanTechnica\n- PV Magazine (for solar)\n- WindPower Engineering & Development..."
            }
          ],
          "model": "claude-opus-4-6",
          "stop_reason": "end_turn",
          "usage": {
            "input_tokens": 21,
            "output_tokens": 305
          }
        }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Python">
    <Steps>
      <Step title="Set your API key">
        Get your API key from the [Claude Console](/settings/keys) and set it as an environment variable:

        ```bash
        export ANTHROPIC_API_KEY='your-api-key-here'
        ```
      </Step>

      <Step title="Install the SDK">
        Install the Anthropic Python SDK:

        ```bash
        pip install anthropic
        ```
      </Step>

      <Step title="Create your code">
        Save this as `quickstart.py`:

        ```python
        import anthropic

        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": "What should I search for to find the latest developments in renewable energy?",
                }
            ],
        )
        print(message.content)
        ```
      </Step>

      <Step title="Run your code">
        ```bash
        python quickstart.py
        ```

        **Example output:**
        ```python
        [
            TextBlock(
                text='Here are some effective search strategies for finding the latest renewable energy developments:\n\n**Search Terms to Use:**\n- "renewable energy news 2024"\n- "clean energy breakthroughs"\n- "solar/wind/battery technology advances"\n- "energy storage innovations"\n- "green hydrogen developments"\n- "renewable energy policy updates"\n\n**Reliable Sources to Check:**\n- **News & Analysis:** Reuters Energy, Bloomberg New Energy Finance, Greentech Media, Energy Storage News\n- **Industry Publications:** Renewable Energy World, PV Magazine, Wind Power Engineering\n- **Research Organizations:** International Energy Agency (IEA), National Renewable Energy Laboratory (NREL)\n- **Government Sources:** Department of Energy websites, EPA clean energy updates\n\n**Specific Topics to Explore:**\n- Perovskite and next-gen solar cells\n- Offshore wind expansion\n- Grid-scale battery storage\n- Green hydrogen production\n- Carbon capture technologies\n- Smart grid innovations\n- Energy policy changes and incentives...',
                type="text",
            )
        ]
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="TypeScript">
    <Steps>
      <Step title="Set your API key">
        Get your API key from the [Claude Console](/settings/keys) and set it as an environment variable:

        ```bash
        export ANTHROPIC_API_KEY='your-api-key-here'
        ```
      </Step>

      <Step title="Install the SDK">
        Install the Anthropic TypeScript SDK:

        ```bash
        npm install @anthropic-ai/sdk
        ```
      </Step>

      <Step title="Create your code">
        Save this as `quickstart.ts`:

```typescript
import Anthropic from "@anthropic-ai/sdk";

async function main() {
  const anthropic = new Anthropic();

  const msg = await anthropic.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 1000,
    messages: [
      {
        role: "user",
        content:
          "What should I search for to find the latest developments in renewable energy?"
      }
    ]
  });
  console.log(msg);
}

main().catch(console.error);
        ```
      </Step>

      <Step title="Run your code">
        ```bash
        npx tsx quickstart.ts
        ```

        **Example output:**
        ```javascript hidelines={1..2}
        const _ =
          // output
          {
            id: "msg_01ThFHzad6Bh4TpQ6cHux9t8",
            type: "message",
            role: "assistant",
            model: "claude-opus-4-6",
            content: [
              {
                type: "text",
                text:
                  "Here are some effective search strategies to find the latest renewable energy developments:\n\n" +
                  "## Search Terms to Use:\n" +
                  '- "renewable energy news 2024"\n' +
                  '- "clean energy breakthroughs"\n' +
                  '- "solar wind technology advances"\n' +
                  '- "energy storage innovations"\n' +
                  '- "green hydrogen developments"\n' +
                  '- "offshore wind projects"\n' +
                  '- "battery technology renewable"\n\n' +
                  "## Best Sources to Check:\n\n" +
                  "**News & Industry Sites:**\n" +
                  "- Renewable Energy World\n" +
                  "- CleanTechnica\n" +
                  "- GreenTech Media (now Wood Mackenzie)\n" +
                  "- Energy Storage News\n" +
                  "- PV Magazine (for solar)..."
              }
            ],
            stop_reason: "end_turn",
            usage: {
              input_tokens: 21,
              output_tokens: 302
            }
          }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Java">
    <Steps>
      <Step title="Set your API key">
        Get your API key from the [Claude Console](/settings/keys) and set it as an environment variable:

        ```bash
        export ANTHROPIC_API_KEY='your-api-key-here'
        ```
      </Step>

      <Step title="Install the SDK">
        Add the Anthropic Java SDK to your project. First find the current version on [Maven Central](https://central.sonatype.com/artifact/com.anthropic/anthropic-java).

        **Gradle:**
        ```groovy
        implementation("com.anthropic:anthropic-java:2.15.0")
        ```

        **Maven:**
        ```xml
        <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java</artifactId>
          <version>2.15.0</version>
        </dependency>
        ```
      </Step>

      <Step title="Create your code">
        Save this as `QuickStart.java`:

        ```java
        import com.anthropic.client.AnthropicClient;
        import com.anthropic.client.okhttp.AnthropicOkHttpClient;
        import com.anthropic.models.messages.Message;
        import com.anthropic.models.messages.MessageCreateParams;

        public class QuickStart {

          public static void main(String[] args) {
            AnthropicClient client = AnthropicOkHttpClient.fromEnv();

            MessageCreateParams params = MessageCreateParams.builder()
              .model("claude-opus-4-6")
              .maxTokens(1000)
              .addUserMessage(
                "What should I search for to find the latest developments in renewable energy?"
              )
              .build();

            Message message = client.messages().create(params);
            System.out.println(message.content());
          }
        }
        ```
      </Step>

      <Step title="Run your code">
        ```bash
        javac QuickStart.java
        java QuickStart
        ```

        **Example output:**
        
        ```java nocheck
        [ContentBlock{text=TextBlock{text=Here are some effective search strategies to find the latest renewable energy developments:

        ## Search Terms to Use:
        - "renewable energy news 2024"
        - "clean energy breakthroughs"
        - "solar/wind/battery technology advances"
        - "energy storage innovations"
        - "green hydrogen developments"
        - "renewable energy policy updates"

        ## Best Sources to Check:
        - **News & Analysis:** Reuters Energy, Bloomberg New Energy Finance, Greentech Media
        - **Industry Publications:** Renewable Energy World, PV Magazine, Wind Power Engineering
        - **Research Organizations:** International Energy Agency (IEA), National Renewable Energy Laboratory (NREL)
        - **Government Sources:** Department of Energy websites, EPA clean energy updates

        ## Specific Topics to Explore:
        - Perovskite and next-gen solar cells
        - Offshore wind expansion
        - Grid-scale battery storage
        - Green hydrogen production..., type=text}}]
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Next steps

You made your first API call. Next, learn the Messages API patterns you'll use in every Claude integration.

<Card title="Working with the Messages API" icon="messages" href="/docs/en/build-with-claude/working-with-messages">
  Learn multi-turn conversations, system prompts, stop reasons, and other core patterns.
</Card>

Once you're comfortable with the basics, explore further:

<CardGroup cols={3}>
  <Card title="Models overview" icon="brain" href="/docs/en/about-claude/models/overview">
    Compare Claude models by capability and cost.
  </Card>
  <Card title="Features overview" icon="list" href="/docs/en/build-with-claude/overview">
    Browse all Claude capabilities: tools, context management, structured outputs, and more.
  </Card>
  <Card title="Client SDKs" icon="code-brackets" href="/docs/en/api/client-sdks">
    Reference documentation for Python, TypeScript, Java, and other client libraries.
  </Card>
</CardGroup>


# Models overview

Claude is a family of state-of-the-art large language models developed by Anthropic. This guide introduces the available models and compares their performance.

---

## Choosing a model

If you're unsure which model to use, consider starting with **Claude Opus 4.6** for the most complex tasks. It is the latest generation model with exceptional performance in coding and reasoning.

All current Claude models support text and image input, text output, multilingual capabilities, and vision. Models are available via the Claude API, AWS Bedrock, and Google Vertex AI.

Once you've picked a model, [learn how to make your first API call](/docs/en/get-started).

### Latest models comparison

| Feature | Claude Opus 4.6 | Claude Sonnet 4.6 | Claude Haiku 4.5 |
|:--------|:----------------|:------------------|:-----------------|
| **Description** | The most intelligent model for building agents and coding | The best combination of speed and intelligence | The fastest model with near-frontier intelligence |
| **Claude API ID** | claude-opus-4-6 | claude-sonnet-4-6 | claude-haiku-4-5-20251001 |
| **Claude API alias** | claude-opus-4-6 | claude-sonnet-4-6 | claude-haiku-4-5 |
| **AWS Bedrock ID** | anthropic.claude-opus-4-6-v1 | anthropic.claude-sonnet-4-6 | anthropic.claude-haiku-4-5-20251001-v1:0 |
| **GCP Vertex AI ID** | claude-opus-4-6 | claude-sonnet-4-6 | claude-haiku-4-5@20251001 |
| **Pricing**<sup>1</sup> | \$5 / input MTok<br/>\$25 / output MTok | \$3 / input MTok<br/>\$15 / output MTok | \$1 / input MTok<br/>\$5 / output MTok |
| **[Extended thinking](/docs/en/build-with-claude/extended-thinking)** | Yes | Yes | Yes |
| **[Adaptive thinking](/docs/en/build-with-claude/adaptive-thinking)** | Yes | Yes | No |
| **[Priority Tier](/docs/en/api/service-tiers)** | Yes | Yes | Yes |
| **Comparative latency** | Moderate | Fast | Fastest |
| **Context window** | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> / <br/> <Tooltip tooltipContent="~750K words \ ~3.4M unicode characters">1M tokens</Tooltip> (beta)<sup>3</sup> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> / <br/> <Tooltip tooltipContent="~750K words \ ~3.4M unicode characters">1M tokens</Tooltip> (beta)<sup>3</sup> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> |
| **Max output** | 128K tokens | 64K tokens | 64K tokens |
| **Reliable knowledge cutoff** | May 2025<sup>2</sup> | Aug 2025<sup>2</sup> | Feb 2025 |
| **Training data cutoff** | Aug 2025 | Jan 2026 | Jul 2025 |

_<sup>1 - See the [pricing page](/docs/en/about-claude/pricing) for complete pricing information including batch API discounts, prompt caching rates, extended thinking costs, and vision processing fees.</sup>_

_<sup>2 - **Reliable knowledge cutoff** indicates the date through which a model's knowledge is most extensive and reliable. **Training data cutoff** is the broader date range of training data used. For more information, see [Anthropic's Transparency Hub](https://www.anthropic.com/transparency).</sup>_

_<sup>3 - Claude Opus 4.6 and Sonnet 4.6 support a [1M token context window](/docs/en/build-with-claude/context-windows#1m-token-context-window) when using the `context-1m-2025-08-07` beta header. [Long context pricing](/docs/en/about-claude/pricing#long-context-pricing) applies to requests exceeding 200K tokens.</sup>_

<Note>Models with the same snapshot date (e.g., 20240620) are identical across all platforms and do not change. The snapshot date in the model name ensures consistency and allows developers to rely on stable performance across different environments.</Note>

<Note>Starting with **Claude Sonnet 4.5 and all subsequent models** (including Claude Sonnet 4.6), AWS Bedrock and Google Vertex AI offer two endpoint types: **global endpoints** (dynamic routing for maximum availability) and **regional endpoints** (guaranteed data routing through specific geographic regions). For more information, see the [third-party platform pricing section](/docs/en/about-claude/pricing#third-party-platform-pricing).</Note>

<section title="Legacy models">

The following models are still available. Consider migrating to current models for improved performance:

| Feature | Claude Sonnet 4.5 | Claude Opus 4.5 | Claude Opus 4.1 | Claude Sonnet 4 | Claude Opus 4 | Claude Haiku 3 (deprecated) |
|:--------|:------------------|:----------------|:----------------|:----------------|:--------------|:----------------------------|
| **Claude API ID** | claude-sonnet-4-5-20250929 | claude-opus-4-5-20251101 | claude-opus-4-1-20250805 | claude-sonnet-4-20250514 | claude-opus-4-20250514 | claude-3-haiku-20240307 |
| **Claude API alias** | claude-sonnet-4-5 | claude-opus-4-5 | claude-opus-4-1 | claude-sonnet-4-0 | claude-opus-4-0 | N/A |
| **AWS Bedrock ID** | anthropic.claude-sonnet-4-5-20250929-v1:0 | anthropic.claude-opus-4-5-20251101-v1:0 | anthropic.claude-opus-4-1-20250805-v1:0 | anthropic.claude-sonnet-4-20250514-v1:0 | anthropic.claude-opus-4-20250514-v1:0 | anthropic.claude-3-haiku-20240307-v1:0 |
| **GCP Vertex AI ID** | claude-sonnet-4-5@20250929 | claude-opus-4-5@20251101 | claude-opus-4-1@20250805 | claude-sonnet-4@20250514 | claude-opus-4@20250514 | claude-3-haiku@20240307 |
| **Pricing** | \$3 / input MTok<br/>\$15 / output MTok | \$5 / input MTok<br/>\$25 / output MTok | \$15 / input MTok<br/>\$75 / output MTok | \$3 / input MTok<br/>\$15 / output MTok | \$15 / input MTok<br/>\$75 / output MTok | \$0.25 / input MTok<br/>\$1.25 / output MTok |
| **[Extended thinking](/docs/en/build-with-claude/extended-thinking)** | Yes | Yes | Yes | Yes | Yes | No |
| **[Priority Tier](/docs/en/api/service-tiers)** | Yes | Yes | Yes | Yes | Yes | No |
| **Comparative latency** | Fast | Moderate | Moderate | Fast | Moderate | Fast |
| **Context window** | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> / <br/> <Tooltip tooltipContent="~750K words \ ~3.4M unicode characters">1M tokens</Tooltip> (beta)<sup>1</sup> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> / <br/> <Tooltip tooltipContent="~750K words \ ~3.4M unicode characters">1M tokens</Tooltip> (beta)<sup>1</sup> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> |
| **Max output** | 64K tokens | 64K tokens | 32K tokens | 64K tokens | 32K tokens | 4K tokens |
| **Reliable knowledge cutoff** | Jan 2025<sup>2</sup> | May 2025<sup>2</sup> | Jan 2025<sup>2</sup> | Jan 2025<sup>2</sup> | Jan 2025<sup>2</sup> | <sup>3</sup> |
| **Training data cutoff** | Jul 2025 | Aug 2025 | Mar 2025 | Mar 2025 | Mar 2025 | Aug 2023 |

<Warning>
Claude Haiku 3 (`claude-3-haiku-20240307`) is deprecated and will be retired on April 19, 2026. Migrate to [Claude Haiku 4.5](/docs/en/about-claude/models/overview#latest-models-comparison) before the retirement date. See [model deprecations](/docs/en/about-claude/model-deprecations) for details.
</Warning>

_<sup>1 - Claude Sonnet 4.5 and Claude Sonnet 4 support a [1M token context window](/docs/en/build-with-claude/context-windows#1m-token-context-window) when using the `context-1m-2025-08-07` beta header. [Long context pricing](/docs/en/about-claude/pricing#long-context-pricing) applies to requests exceeding 200K tokens.</sup>_

_<sup>2 - **Reliable knowledge cutoff** indicates the date through which a model's knowledge is most extensive and reliable. **Training data cutoff** is the broader date range of training data used.</sup>_

_<sup>3 - Some Haiku models have a single training data cutoff date.</sup>_

</section>

## Prompt and output performance

Claude 4 models excel in:
- **Performance**: Top-tier results in reasoning, coding, multilingual tasks, long-context handling, honesty, and image processing. See the [Claude 4 blog post](http://www.anthropic.com/news/claude-4) for more information.
- **Engaging responses**: Claude models are ideal for applications that require rich, human-like interactions.

    - If you prefer more concise responses, you can adjust your prompts to guide the model toward the desired output length. Refer to the [prompt engineering guides](/docs/en/build-with-claude/prompt-engineering) for details.
    - For prompting best practices, see the [prompting best practices guide](/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).
- **Output quality**: When migrating from previous model generations to Claude 4, you may notice larger improvements in overall performance.

## Migrating to Claude 4.6

If you're currently using older Claude models, consider migrating to Claude Opus 4.6 to take advantage of improved intelligence and enhanced capabilities. For detailed migration instructions, see [Migrating to Claude 4.6](/docs/en/about-claude/models/migration-guide).

## Get started with Claude

If you're ready to start exploring what Claude can do for you, dive in! Whether you're a developer looking to integrate Claude into your applications or a user wanting to experience the power of AI firsthand, the following resources can help.

<Note>Looking to chat with Claude? Visit [claude.ai](http://www.claude.ai)!</Note>

<CardGroup cols={3}>
  <Card title="Intro to Claude" icon="check" href="/docs/en/intro">
    Explore Claude's capabilities and development flow.
  </Card>
  <Card title="Quickstart" icon="lightning" href="/docs/en/get-started">
    Learn how to make your first API call in minutes.
  </Card>
  <Card title="Claude Console" icon="code" href="/">
    Craft and test powerful prompts directly in your browser.
  </Card>
</CardGroup>

If you have any questions or need assistance, don't hesitate to reach out to the [support team](https://support.claude.com/) or consult the [Discord community](https://www.anthropic.com/discord).