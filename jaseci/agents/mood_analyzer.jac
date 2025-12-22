global analyze_mood = |mood, note| {
    if mood in ["sad", "angry", "tired"] {
        return {
            "sentiment": "negative",
            "confidence": 0.8
        };
    };

    return {
        "sentiment": "neutral",
        "confidence": 0.5
    };
};
