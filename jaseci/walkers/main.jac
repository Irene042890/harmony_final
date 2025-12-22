// jaseci/walkers/main.jac

walker support_agent {
    with entry {
        m = ctx;

        if m == null {
            m = {
                "mood": "okay",
                "note": ""
            };
        }

        // ---- analyze mood inline ----
        analysis = {};

        if m["mood"] in ["sad", "angry", "tired"] {
            analysis = {
                "sentiment": "negative",
                "confidence": 0.8
            };
        } else {
            analysis = {
                "sentiment": "neutral",
                "confidence": 0.5
            };
        }

        // ---- generate support inline ----
        support = "";

        if m["mood"] in ["sad", "tired"] {
            support = "I'm sorry you're feeling tired. Try resting and taking small breaks.";
        } else {
            support = "You're doing okay. Keep going!";
        }

        report {
            "analysis": analysis,
            "support": support,
            "status": "ready"
        };
    }
}
