from django.shortcuts import render


def main_page(request):
    context = {}
    return render(request, 'main/main_page.html', context=context)
