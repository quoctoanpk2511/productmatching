from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    ListView,
    View
)
from django import template
from .models import (
    Product,
)

import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, fcluster

# Create your views here.
# @login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))

class ProductsView(ListView):

    template_name = 'products.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(cluster_id__lt=11)
        return context

    def post(self, request):
        response = HttpResponseRedirect('/')
        if request.method == 'POST':
            # products = Product.objects.values_list('title', flat=True).filter(cluster_id__lt=11)
            products = Product.objects.filter(cluster_id__lt=11)
            list_title = []
            for product in products:
                list_title.append(re.sub('(?<=\d) (?=gb)', '', product.title))
            stopwords = ['black', 'white', 'grey', 'silver', 'unlocked', 'sim', 'free', 'gold', 'rose', 'space',
                         'handset', 'only', 'mobile phone', 'phone', 'smartphone', 'in', 'mobile', 'single', 'cm', '4g',
                         '4.7', '5.5', '5.8']
            tfidf_vectorizer = TfidfVectorizer(max_df=0.7, max_features=20000, min_df=0.02, stop_words=stopwords,
                                               ngram_range=(1, 3), tokenizer=tokenize)
            tfidf_matrix = tfidf_vectorizer.fit_transform(list_title)
            dist = cosine_similarity(tfidf_matrix)
            linkage_matrix = linkage(dist, 'complete', metric='cosine')
            clusters = fcluster(linkage_matrix, t=0.65, criterion='distance')
            print(tfidf_matrix.shape)
            i = 0
            for product in products:
                product.new_cluster = clusters[i]
                product.save()
                i+= 1

            print(request.POST.get('matching'))
        return response

def tokenize(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    return tokens
