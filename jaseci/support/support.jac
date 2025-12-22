walker analyze_support {
    has mood;
    has note;

    can start {
        mood = ctx.mood ?? "unspecified";
        note = ctx.note ?? "";

        response = by_llm(
            model="gpt-4o-mini",
            prompt=f"""
You are an empathetic mental health support assistant.

User mood: {mood}
User note: {note}

Generate:
1. sentiment (positive / neutral / negative)
2. confidence (0–1)
3. a supportive message tailored to BOTH mood and note

Return STRICT JSON:
{
  "analysis": { "sentiment": "...", "confidence": 0.X },
  "support": "..."
}
"""
        );

        report response;
    }
}
