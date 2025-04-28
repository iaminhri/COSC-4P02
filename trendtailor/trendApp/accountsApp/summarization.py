from transformers import pipeline

def summarize_article(article_text, model="facebook/bart-large-cnn", summary_length=100):
    summarizer = pipeline("summarization", model=model)
    summary = summarizer(article_text, max_length=summary_length, min_length=30, do_sample=False)
    return summary[0]["summary_text"]
