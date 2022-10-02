

def test_cookie(request):
    if request.method == 'GET':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            print('='*9)
            print('Web Browser accepts cookiies')
            print('='*9)
        else:
            print('='*9)
            print('Web Browser does not accepts cookiies!')
            print('='*9)
    request.session.set_test_cookie()
    # return render(request, 'testapp/test_cookie.html')