from django.shortcuts import render,redirect
from . models import *
from django.utils import timezone
from django.contrib import messages
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from django.http import JsonResponse


import hashlib

# Generate a 32-byte key using a hash function (SHA-256)
KEY = hashlib.sha256(b'your_secret_key').digest()

# Ensure the key length is valid for AES encryption
# KEY = KEY[:32]  # Truncate or pad with zeros as necessary

# print("AES Key:", KEY)



def index(request):
    return render(request, 'index.html')

def home(request):
    login=request.session['login']
    # print(login)
    return render(request, 'home.html',{'login':login})

def AttributeAuthorityLogin(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        if email=='Attribute@gmail.com' and password=='Authority':
            request.session['login']='Attribute'
            return redirect('home')
        else:
            return render(request, 'AttributeAuthorityLogin.html', {'msg':'Invalid email or password'})
    return render(request, 'AttributeAuthorityLogin.html')

def userregistration(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        contact=request.POST['contact']
        address=request.POST['address']
        user=UsersModel.objects.filter(email=email).exists()
        if user:
            return render(request, 'userregistration.html', {'msg':'Email already exists'})
        else:
            user=UsersModel(name=name,email=email,password=password,contact=contact,address=address)
            user.save()
            return redirect('UsersLogin')
        
    return render(request, 'userregistration.html')

def UsersLogin(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user=UsersModel.objects.filter(email=email,password=password).exists()
        if user:
            data=UsersModel.objects.get(email=email)
            if data.status=='active':
                request.session['login']='User'
                request.session['email']=email
                return redirect('home')
            else:
                return render(request, 'UsersLogin.html', {'msg':'Your account is not activated By Attribute Authority'})
        else:
            return render(request, 'UsersLogin.html', {'msg':'Invalid email or password'})
    return render(request, 'UsersLogin.html')

def Logout(request):
    del request.session['login']
    return redirect('/')

def useractivation(request):
    login=request.session['login']
    reqsts=UsersModel.objects.filter(status='pending')
    return render(request, 'useractivation.html',{'reqsts':reqsts,'login':login})


def activate(request,id):
    user=UsersModel.objects.get(id=id)
    user.status='active'
    user.save()
    return redirect('useractivation')

def viewactiveusers(request):
    login=request.session['login']
    reqsts=UsersModel.objects.filter(status='active')
    return render(request, 'viewactiveusers.html',{'reqsts':reqsts,'login':login})

def ownerregistration(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        contact=request.POST['contact']
        address=request.POST['address']
        owner=OwnersModel.objects.filter(email=email).exists()
        if owner:
            return render(request, 'ownerregistration.html', {'msg':'Email already exists'})
        else:
            Owner=OwnersModel(name=name,email=email,password=password,contact=contact,address=address)
            Owner.save()
            return redirect('ownerlogin')
        
    return render(request, 'ownerregistration.html')


def ownerlogin(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        owner=OwnersModel.objects.filter(email=email,password=password).exists()
        if owner:
            request.session['login']='Owner'
            request.session['email']='email'
            return redirect('home') 
        else:
            return render(request, 'ownerlogin.html', {'msg':'Invalid email or password'})
    return render(request, 'ownerlogin.html')


def encrypt_data(data):
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

def decrypt_data(encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode('utf-8')

def uploadfile(request):
    # FileUploadModel.objects.all().delete()
    login=request.session['login']
    if request.method=="POST":
        email=request.session['email']
        keyword1 = encrypt_data(request.POST['Keyword1'])
        keyword2 = encrypt_data(request.POST['Keyword2'])
        keyword3 = encrypt_data(request.POST['Keyword3'])
        files=request.FILES['file']
        filename=files.name
        time=timezone.now()
        file=FileUploadModel(email=email,keyword1=keyword1,keyword2=keyword2,keyword3=keyword3,filename=filename,files=files,time=time)
        file.save()
        messages.success(request, 'File Uploaded Successfully')
        return redirect('uploadfile')
    return render(request,'uploadfile.html',{'login':login})

def myfiles(request):
    login=request.session['login']
    email=request.session['email']
    files=FileUploadModel.objects.filter(email=email)
    return render(request,'myfiles.html',{'files':files,'login':login})

def encryptedindex(request):
    login=request.session['login']
    login=request.session['login']
    email=request.session['email']
    files=FileUploadModel.objects.filter(email=email)
    
    return render(request,'encryptedindex.html',{'files':files,'login':login})
    

def csplogin(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        if email=='CSP@gmail.com' and password=='CSP':
            request.session['login']='CSP'
            return redirect('home')
        else:
            return render(request, 'CSPlogin.html', {'msg':'Invalid email or password'})
    return render(request,'CSPlogin.html')

def getsearch(request):
    login=request.session['login']
    email=request.session['email']
    if request.method=="POST":
        keyword = request.POST['Keyword']  
        data=SearchModel.objects.filter(keyword=keyword,email=email,status='verified').exists()
        if data:
            req=SearchModel.objects.get(keyword=keyword,email=email,status='verified')
            req.filerequest='requested'
            req.save()
            messages.success(request, 'Search Request Sent Successfully! ')
            return redirect('getsearch')
        time=timezone.now() 
        search=SearchModel(email=email,keyword=keyword,time=time)
        search.save()
        messages.success(request, 'Search Request Sent Successfully! ')
        return redirect('getsearch')
    return render(request,'getsearch.html',{'login':login})

def searchrequest(request):
    login=request.session['login']
    search=SearchModel.objects.filter(status='waiting')
    return render(request,'searchrequests.html',{'search':search,'login':login})

def getsearchverification(request,id):
    # login=request.session['login']
    search=SearchModel.objects.get(id=id)
    search.status='pending'
    search.save()
    return redirect('searchrequest')

    
def VerificationAuthorityLogin(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        if email=='VA@gmail.com' and password=='VA':
            request.session['login']='Verification'
            return redirect('home')
        else:
            return render(request, 'verificationauthoritylogin.html', {'msg':'Invalid email or password'})
    return render(request,'verificationauthoritylogin.html')

def searchaccessrequest(request):
    login=request.session['login']
    search=SearchModel.objects.filter(status='pending')
    return render(request,'searchaccessrequests.html',{'search':search,'login':login})

def verify(request,id):
    # login=request.session['login']
    search=SearchModel.objects.get(id=id)
    search.status='verified'
    search.save()
    return redirect('searchaccessrequest')

def myrequests(request):
    login=request.session['login']
    email=request.session['email']
    search=SearchModel.objects.filter(email=email,status='verified')
    return render(request,'myrequests.html',{'search':search,'login':login})

def verifiedrequests(request):
    login=request.session['login']
    search=SearchModel.objects.filter(status='verified',filerequest='requested')
    ser=FileUploadModel.objects.all()
    # sear=[(i.id, i.email, i.status, i.time, i.keyword) for i in search]
    # print('--------------------------------------------------------')

    # print(type(sear))
    # print(sear)
    # keyword=[]
    # for j in search:
    #     for i in ser:
    #         x=decrypt_data(i.keyword1)
    #         y=decrypt_data(i.keyword2)
    #         z=decrypt_data(i.keyword3)
    #         if x==j.keyword:
    #             keyword.append(x)
    #         elif y==j.keyword:
    #             keyword.append(y)
    #         elif z==j.keyword:
    #             keyword.append(z)
    decrypted_keywords = [(decrypt_data(i.keyword1), decrypt_data(i.keyword2), decrypt_data(i.keyword3)) for i in ser]

    keyword = []
    for j in search:
        for x, y, z in decrypted_keywords:
            if j.keyword in (x, y, z):
                keyword.append(j.keyword)
    # print('--------------------------------------------------------')
    # print(type(search))
    # print(type(keyword))
    # # print(keyword)
    # Ziplist=zip(keyword,search)


    return render(request,'verifiedrequests.html',{'search':search,'login':login,})

def sendresults(request,id):
    login=request.session['login']
    search=SearchModel.objects.get(id=id)
    search.filerequest='sent'
    search.status='Approved'
    ser=FileUploadModel.objects.all()

    for i in ser:
        x=decrypt_data(i.keyword1)
        y=decrypt_data(i.keyword2)
        z=decrypt_data(i.keyword3)
        if x==search.keyword:
            search.files=i.files
            search.save()
        elif y==search.keyword:
            search.files=i.files
            search.save()
        elif z==search.keyword:
            search.files=i.files
            search.save()
    return redirect('verifiedrequests')

def verifiedresults(request):
    login=request.session['login']
    email=request.session['email']
    sear=SearchModel.objects.filter(status='Approved',email=email).exists()
    if sear:
        search=SearchModel.objects.filter(email=email,status='Approved')
        return render(request, 'verifiedresults.html',{'search':search,'login':login})
    else:
        return render(request, 'verifiedresults.html',{'login':login})
    

def download(request,id):
    login=request.session['login']
    print('----------------------------------------------')
    if login:
        search=SearchModel.objects.get(id=id)
        time=timezone.now()
        data=DownloadModel(
            email=search.email,
            files=search.files.name,
            time=time
        )
        data.save()
        print('hello')
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def viewdownloads(request):
    login=request.session['login']
    data=DownloadModel.objects.all()
    return render(request, 'viewdownloads.html',{'data':data,'login':login})

def allsearchrequests(request):
    login=request.session['login']
    data=SearchModel.objects.all()
    return render(request, 'allsearchrequest.html',{'data':data,'login':login})


            

    

    




    

    
    