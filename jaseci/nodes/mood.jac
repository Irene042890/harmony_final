// mood.jac - OSP node classes (Jac 0.18 style)
node class User {
    has str username = "guest";
}

node class MoodEntry {
    has str mood;
    has str note;
    has int ts;
}

node class EmotionCategory {
    has str name;
    has str description;
}

node class Suggestion {
    has str text;
    has str generated_by = "system";
}
