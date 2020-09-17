from django.shortcuts import render, redirect
# Userモデルはdjangoが初めから用意しているモデルのため自分で用意する必要はない
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# requestオブジェクトを受け取る
def signupfunc(request):
    if request.method == 'POST':
        # POSTで渡ってきた('xxxxx')を変数へ入れる
        username2 = request.POST['username']
        password2 = request.POST['password']
        try:
            User.objects.get(username=username2)
            return render(request, 'signup.html', {'error' : 'このユーザーは登録されています'})
        except:
            # 下記は雛形(ユーザーネーム, メールアドレス, パスワード)
            user = User.objects.create_user(username2, '', password2)
            # render(request, 'class BasedViewにおけるtemplateで指定するhtmlに該当', {辞書型のデータ})
            return render(request, 'signup.html', {'some': 100})
    # requestを返さないとエラー(post以外の時の処理)
    return render(request, 'signup.html', {'some': 100})

def loginfunc(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        # 認証
        user = authenticate(request, username=username2, password=password2)
        if user is not None:
            # userがいる場合
            login(request, user)
            # urlにリクエストし直してページ遷移する時はredirect
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html')

@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html', {'object_list':object_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')

def detailfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object': object})

def goodfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    # post.good +=1 としても同じ意味になる
    post.good = post.good + 1
    post.save()
    return redirect('list')

def readfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    # ログインしているユーザー名を取得
    post2 = request.user.get_username()
    # BoardModel.readtextにpost2(ログインユーザー)が入っていた場合
    if post2 in post.readtext:
        return redirect('list')
    else:
        post.read += 1
        post.readtext = post.readtext + ' ' + post2
        post.save()
        return redirect('list')

class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    # 引っ張ってくるフィールドを指定
    fields = ('title', 'content', 'author', 'images', 'movie')
    # createでデータの作成が完了したときに遷移する画面
    success_url = reverse_lazy('list')