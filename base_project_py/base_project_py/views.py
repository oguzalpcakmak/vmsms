from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

def health_check(request):
    return JsonResponse({'status': 'ok'})

def main(request):
    # Redirect directly to the login page
    return redirect('vmsms:login')
