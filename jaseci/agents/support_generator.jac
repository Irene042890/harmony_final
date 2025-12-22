global generate_support = |mood, note| {
    if mood in ["sad", "tired"] {
        return "I'm sorry you're feeling tired. Try resting and taking small breaks.";
    };

    return "You're doing okay. Keep going!";
};
