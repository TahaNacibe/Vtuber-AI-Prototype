from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load model and tokenizer
model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Emotion labels from the model
id2label = model.config.id2label

def detect_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = F.softmax(logits, dim=-1)
    top_prob, top_label_id = torch.max(probs, dim=1)
    emotion = id2label[top_label_id.item()]
    confidence = top_prob.item()
    return emotion, confidence

# Test examples
examples = [
    "My cat Daniel died.",
    "It's okay, he was old. I still have Daniel Jr and I love him!",
    "I'm so excited to go hiking tomorrow!",
    "Why does everything always go wrong!?",
    "Just chilling today.",
    "I eaten a pice of chasse"
]

for text in examples:
    emotion, confidence = detect_emotion(text)
    print(f"[{emotion.upper()}] ({confidence:.2f}): {text}")
