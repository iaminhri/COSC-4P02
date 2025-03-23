from transformers import pipeline

def summarize_article(article_text, model="facebook/bart-large-cnn", summary_length=100):
    summarizer = pipeline("summarization", model=model)
    summary = summarizer(article_text, max_length=summary_length, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

# Example usage:
article_text = """
In a breakthrough study, scientists have discovered a new method to store renewable energy
more efficiently using advanced battery technology. This innovation is expected to reduce
reliance on fossil fuels and accelerate the transition to sustainable energy sources.
The research, conducted at a leading university, demonstrates that the new battery
composition increases energy retention by 50% compared to existing models. Experts believe
this could be a game-changer in the energy sector.
"""

summary = summarize_article(article_text)
print("Summary:", summary)
