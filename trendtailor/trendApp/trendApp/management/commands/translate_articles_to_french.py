from django.core.management.base import BaseCommand
from deep_translator import GoogleTranslator
from UserPreferenceApp.models import Article, ArticleFrench

class Command(BaseCommand):
    help = 'Translate articles to French and save in ArticleFrench table'

    def handle(self, *args, **kwargs):
        translator = GoogleTranslator(source='auto', target='fr')
        articles = Article.objects.all()

        for article in articles:
            if hasattr(article, 'french'):
                continue  
            try:
                article_fr = ArticleFrench.objects.create(
                    original=article,
                    title=translator.translate(article.title),
                    description=translator.translate(article.description or ''),
                    contents=translator.translate(article.contents or ''),
                    url=article.url,
                    urlToImage=article.urlToImage,
                    topic=translator.translate(article.topic),
                )
                self.stdout.write(self.style.SUCCESS(f"Translated article: {article.title}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error translating article {article.id}: {e}"))
