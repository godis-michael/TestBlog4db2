from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from blog.forms import SignUpForm
from .tokens import account_activation_token
from .models import User, Article
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .filters import ArticleFilter


@login_required
def home(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    filter = ArticleFilter(request.GET, queryset=Article.objects.all())
    filtered_qs = filter.qs
    # Provide Paginator with the request object for complete querystring generation
    paginator = Paginator(filtered_qs, per_page=8, request=request)
    articles = paginator.page(page)
    return render(request, 'blog/home.html', {'articles': articles, 'filter': filter})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('blog/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'blog/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'blog/account_activation_invalid.html')


def article_detailed(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blog/article_detailed.html', {'article': article})


def article_new(request):
    return None


def image(request):
    articles = Article()
    variables = RequestContext(request, {
        'articles': articles
    })
    return render_to_response('blog/article_detailed.html', variables)
