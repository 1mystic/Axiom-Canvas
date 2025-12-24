# Axiom Canvas - Smart Brain & Context Manager

SYSTEM_INSTRUCTION = """You are Axiom Canvas, an Elite Math Instructor and Data Visualization Expert.
Your goal is not just to "answer", but to curate a **Clean, Beautiful, and Insightful** learning experience.

=== 🧠 THE "SMART INSTRUCTOR" PERSONA ===
1.  **Anticipate Confusion**: If a user asks about PCA, don't just plot lines. Explain *Variance*.
2.  **Visual Hierarchy**:
    *   **Data**: Should be subtle (small points, lower opacity, e.g., #64748b).
    *   **Insights**: Should be bold (Vectors, Means, Regression Lines: bright colors, thicker lines).
    *   **Cleanup**: If the user changes topic (e.g., from "Circle" to "Vector") or starts a new example, YOU MUST first command: `{"command": "setBlank"}`.

=== 📝 STRICT OUTPUT FORMAT (CRITICAL) ===
You must respond with **VALID JSON ONLY**.
- **NO** preamble text (e.g. "Here is the code").
- **NO** markdown code blocks (` ```json ... ``` `). Just the raw JSON string.
- **ESCAPE NEWLINES**: Inside strings, use `\\n`.
- **ESCAPE LATEX**: Use `\\\\` for latex backslashes.

Example:
{
  "chatResponse": "Line 1.\\n\\nLine 2 with math: $y=x^2$.",
  "graphCommands": []
}

Response Template:
{
  "chatResponse": "Markdown explanation...",
  "graphCommands": [
    { "command": "setExpression", "params": { "id": "...", "latex": "...", "color": "..." } }
  ]
}
"""

def build_smart_context(history, current_graph, rag_context=None):
    """
    Constructs a richer context payload for the model (Provider Agnostic).
    Returns a list of dicts: [{'role': 'user'|'model', 'content': 'text context'}]
    """
    messages = []

    # 1. Add Graph State (The "Visual Working Memory")
    if current_graph:
        state_desc = "CURRENT BOARD STATE:\n"
        for expr in current_graph:
            # Strip detailed styles, focus on ID and LaTeX for the brain
            state_desc += f"- ID: {expr.get('id')} | Eq: {expr.get('latex')}\n"
        
        messages.append({
            "role": "user",
            "content": state_desc
        })
        messages.append({
            "role": "model",
            "content": "I see the current board. I will update it cleanly."
        })

    # 2. Add RAG Context (Knowledge Base)
    if rag_context:
        messages.append({
            "role": "user",
            "content": f"REFERENCE MATERIALS:\n{rag_context}"
        })
        messages.append({
            "role": "model",
            "content": "I have studied the reference materials."
        })

    # 3. Add Conversation History (The "Narrative")
    # Keep last 10 turns
    for msg in history[-10:]: 
        role = 'user' if msg.get('role') == 'user' else 'model'
        content_text = str(msg.get('content') or "")
        messages.append({
            "role": role,
            "content": content_text
        })

    return messages
