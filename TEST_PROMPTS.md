# Test Prompts for Axiom Canvas

Test these prompts to verify all functionality is working correctly.

## Basic Plotting

### Simple Functions
1. "plot y = x^2"
2. "plot y = sin(x)"
3. "show me y = e^x"
4. "graph y = log(x)"

### Styled Functions
1. "plot y = x^2 in red"
2. "show me y = cos(x) in blue with a dashed line"
3. "graph y = -x^2 + 4 in green"

### Multiple Functions
1. "plot y = x, y = x^2, and y = x^3"
2. "show me sin(x) and cos(x) in different colors"
3. "graph y = 2^x and y = 3^x"

## Mathematical Concepts

### Derivatives
1. "explain the derivative of x^2"
   - Expected: Shows f(x) = x^2 and f'(x) = 2x
2. "what's the derivative of sin(x)?"
   - Expected: Shows sin(x) and cos(x) with explanation
3. "show me the tangent line to y = x^3 at x = 1"

### Trigonometry
1. "explain the relationship between sin and cos"
2. "show me the unit circle"
3. "what is the period of tan(x)?"

### Calculus
1. "show me the area under y = x^2 from 0 to 2"
2. "explain integration with a visual example"
3. "what does f'(x) = 0 mean visually?"

## Graph Manipulation

### Viewport Control
1. "zoom in on the region from -5 to 5"
2. "show me the graph from -10 to 10"
3. "focus on the area around the origin"

### Expression Management
1. "clear the graph"
2. "remove the parabola"
3. "start fresh"

### Points and Features
1. "mark the vertex of the parabola"
2. "show the intersection points"
3. "highlight where the function crosses the x-axis"

## Complex Scenarios

### Intersection Problems
1. "where do y = x^2 and y = 2x + 1 intersect?"
   - Expected: Plots both functions, marks intersection points
2. "find where y = sin(x) and y = cos(x) cross"

### Transformation Demonstrations
1. "show me y = x^2 and y = x^2 + 3"
   - Expected: Demonstrates vertical shift
2. "compare y = x^2 and y = 2x^2"
   - Expected: Shows vertical stretch
3. "show the difference between y = x^2 and y = (x-2)^2"
   - Expected: Demonstrates horizontal shift

### Educational Explanations
1. "what is a parabola?"
2. "explain what makes a function even or odd"
3. "show me why the derivative is the slope"

## RAG (PDF Upload) Tests

### Prerequisites
Upload a PDF file (e.g., a math textbook chapter)

### Test Prompts
1. "summarize the main concepts from the uploaded document"
2. "explain the quadratic formula from the PDF"
3. "show me an example from chapter 2"
4. "what does the document say about derivatives?"
5. "visualize the example on page 5"

## Edge Cases

### Invalid/Ambiguous Requests
1. "plot something cool"
   - Expected: AI suggests a function
2. "help me with math"
   - Expected: AI asks what specifically
3. "show me calculus"
   - Expected: AI gives a calculus example

### Error Handling
1. Send empty message
   - Expected: Nothing happens
2. Very long message (1000+ words)
   - Expected: Handles gracefully
3. "plot xyz + abc"
   - Expected: AI explains invalid function

### Complex LaTeX
1. "plot y = \\frac{1}{x}"
2. "show me y = \\sqrt{x}"
3. "graph y = x^{2} + 2x + 1"

## Progressive Conversation

Have a multi-turn conversation:

1. User: "plot y = x^2"
2. AI: [plots parabola]
3. User: "now add its derivative"
4. AI: [adds y = 2x]
5. User: "show me a tangent line at x = 2"
6. AI: [adds tangent line]
7. User: "what's the slope at that point?"
8. AI: [explains slope = 4]

## Color and Style Tests

1. "plot y = x in red"
2. "plot y = x^2 in blue with dashed line"
3. "show me y = sin(x) in green"
4. "graph multiple functions in different colors"

## Performance Tests

1. "plot y = x, y = x^2, y = x^3, y = x^4, y = x^5"
   - Tests multiple simultaneous expressions
2. Rapid succession of messages
   - Tests loading states and queuing
3. Upload large PDF (5-10 MB)
   - Tests chunking and embedding

## Expected Behaviors

### Successful Response Format
```json
{
  "chatResponse": "Natural language explanation...",
  "graphCommands": [
    {
      "command": "setExpression",
      "params": {
        "id": "unique_id",
        "latex": "y=x^2",
        "color": "#2563eb"
      }
    }
  ]
}
```

### Error Response Format
```json
{
  "chatResponse": "I encountered an error... [explanation]",
  "graphCommands": []
}
```

## Visual Verification Checklist

After each test, verify:
- [ ] Graph renders correctly
- [ ] Colors match description
- [ ] Line styles are correct
- [ ] Chat response is clear and educational
- [ ] No console errors
- [ ] Loading indicator appears/disappears
- [ ] Message scrolls into view
- [ ] Input clears after sending

## Regression Tests

After making changes, test these critical paths:

1. **Basic Plot**: "plot y = x^2"
2. **Styled Plot**: "plot y = sin(x) in red"
3. **Clear**: "clear the graph"
4. **Explain**: "explain derivatives"
5. **Multi-turn**: Follow-up questions work
6. **PDF Upload**: Upload and query

## Browser Compatibility

Test in:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)
- [ ] Mobile browsers

## Responsive Design

Test at different screen sizes:
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

## Performance Metrics

Monitor:
- Response time: < 3 seconds typical
- Graph render time: < 500ms
- PDF processing: < 10 seconds for 5MB file
- Memory usage: Stable over time

## Known Issues to Test

1. JSON parsing when AI wraps in markdown
2. Special characters in LaTeX
3. Very long chat history
4. Concurrent PDF uploads
5. Session expiration handling

---

Use this document to systematically test all features and ensure quality!
