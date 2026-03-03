from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from .decorators import role_required
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages

# Create your views here.


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


@role_required(['admin'])
def Index(request):
    doctor = Doctor.objects.all()
    patient = Patient.objects.all()
    appointment = Appointment.objects.all()
    prescription = Prescription.objects.all()
    d = 0
    p = 0
    a = 0
    m = 0
    for i in doctor:
        d += 1
    for i in patient:
        p += 1
    for i in appointment:
        a += 1
    for i in prescription:
        m += 1
    d1 = {'d': d, 'p': p, 'a': a, 'm': m}
    return render(request, "index.html", d1)


def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST.get("uname", "").strip()
        p = request.POST.get("pwd", "")
        remember = request.POST.get("remember")

        if not u or not p:
            error = "Please enter both username and password"
        else:
            user = authenticate(username=u, password=p)
            if user is None:
                error = "Invalid username or password"
            else:
                # Allow any authenticated user to login; role-based access enforced elsewhere.
                login(request, user)
                if remember == "on":
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser-length session

                # Redirect user to a role-appropriate landing page
                role = getattr(getattr(user, 'profile', None), 'role', None)
                if role == 'admin':
                    return redirect('home')
                if role == 'doctor':
                    return redirect('view_patient')
                if role == 'nurse':
                    return redirect('view_appointment')
                if role == 'front_desk':
                    return redirect('view_appointment')
                if role == 'patient':
                    return redirect('view_appointment')
                # Fallback
                return redirect('home')
    d = {"error": error}
    return render(request, "login.html", d)


@role_required(['admin'])
def create_user(request):
    error = ""
    roles = Profile.ROLE_CHOICES
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role')
        if not username or not password:
            error = 'Please provide username and password'
        else:
            if User.objects.filter(username=username).exists():
                error = 'Username already exists'
            else:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    # ensure profile created and set role
                    profile, created = Profile.objects.get_or_create(user=user)
                    profile.role = role
                    profile.save()
                    messages.success(request, 'User created successfully')
                    return redirect('view_users')
                except Exception as e:
                    error = 'Error creating user: ' + str(e)
    return render(request, 'create_user.html', {'error': error, 'roles': roles})


@role_required(['admin'])
def view_users(request):
    users = User.objects.all().select_related('profile')
    return render(request, 'view_users.html', {'users': users})


@role_required(['admin'])
def edit_user_role(request, uid):
    error = ''
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return redirect('view_users')
    roles = Profile.ROLE_CHOICES
    if request.method == 'POST':
        role = request.POST.get('role')
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()
        messages.success(request, 'Role updated')
        return redirect('view_users')
    return render(request, 'edit_user.html', {'user': user, 'roles': roles, 'error': error})


@role_required(['admin','doctor','nurse','front_desk','patient'], redirect_to='login')
def logout_admin(request):
    logout(request)
    return redirect("login")


@role_required(['admin','doctor','nurse','front_desk'])
def view_doctor(request):
    doc = Doctor.objects.all()
    d = {"doc": doc}
    return render(request, "view_doctor.html", d)


@role_required(['admin'])
def add_doctor(request):
    error = ""
    if request.method == "POST":
        n = request.POST["name"]
        d = request.POST["d_dob"]
        ema = request.POST["d_email"]
        mob = request.POST["mobile"]
        aad = request.POST["d_aadhar"]
        spc = request.POST["specialization"]
        qua = request.POST["qualification"]
        try:
            Doctor.objects.create(
                name=n,
                d_dob=d,
                d_email=ema,
                mobile=mob,
                d_aadhar=aad,
                specialization=spc,
                qualification=qua,
            )
            error = "no"
        except:
            error = "yes"
    d = {"error": error}
    return render(request, "add_doctor.html", d)


@role_required(['admin'])
def delete_doctor(request, pid):
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect("view_doctor")


@role_required(['admin','doctor','nurse','front_desk'])
def view_patient(request):
    pat = Patient.objects.all()
    d = {"pat": pat}
    return render(request, "view_patient.html", d)


@role_required(['admin','front_desk','doctor'])
def add_patient(request):
    error = ""
    if request.method == "POST":
        reg = request.POST["rdate"]
        n = request.POST["pname"]
        g = request.POST["gender"]
        dob = request.POST["p_dob"]
        ema = request.POST["p_email"]
        add = request.POST["address"]
        mob = request.POST["mobile"]
        aad = request.POST["d_aadhar"]
        stat = request.POST["state"]
        city = request.POST["city"]
        bg = request.POST["blood"]
        dis = request.POST["disease"]
        try:
            patient = Patient.objects.create(
                registrationDate=reg,
                name=n,
                gender=g,
                p_dob=dob,
                p_email=ema,
                address=add,
                mobile=mob,
                p_aadhar=aad,
                state=stat,
                city=city,
                bloodgroup=bg,
                disease=dis,
            )
            # create corresponding auth user so patient can sign in
            # using their name (username) and have appointments filtered
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username=patient.name,
                defaults={
                    'email': patient.p_email or '',
                    'password': 'changeme123',  # should prompt reset later
                }
            )
            if created:
                # ensure a profile exists with patient role
                profile, _ = Profile.objects.get_or_create(user=user)
                profile.role = 'patient'
                profile.save()
            # link the two models
            patient.user = user
            patient.save()

            error = "no"
        except Exception as e:
            # could log e for debugging
            error = "yes"
    d = {"error": error}
    return render(request, "add_patient.html", d)


@role_required(['admin'])
def delete_patient(request, pid):
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect("view_patient")


@role_required(['admin','doctor','nurse','front_desk','patient'])
def view_appointment(request):
    role = getattr(getattr(request.user, 'profile', None), 'role', None)
    if role == 'patient':
        # if patient records are linked to User models we can filter
        # directly; otherwise fall back to matching by patient name (the
        # username). the link is created when a patient is added.
        appoint = Appointment.objects.filter(patient__user=request.user)
        if not appoint.exists():
            # either the association wasn't made or the user logged in by
            # name; try the name lookup as a last resort.
            appoint = Appointment.objects.filter(patient__name=request.user.username)
    else:
        appoint = Appointment.objects.all()
    d = {"appoint": appoint}
    return render(request, "view_appointment.html", d)


@role_required(['admin','front_desk','nurse'])
def add_appointment(request):
    error = ""
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    if request.method == "POST":
        d = request.POST["doctor"]
        p = request.POST["patient"]
        d1 = request.POST["date"]
        t = request.POST["time"]
        doctor = Doctor.objects.filter(name=d).first()
        patient = Patient.objects.filter(name=p).first()
        try:
            Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                date1=d1,
                time1=t,
            )
            error = "no"
        except:
            error = "yes"
    d = {'doctor': doctor1, 'patient': patient1, 'error': error}
    return render(request, "add_appointment.html", d)


@role_required(['admin'])
def delete_appointment(request, pid):
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect("view_appointment")


@role_required(['admin','doctor','nurse'])
def view_prescription(request):
    prescrip = Prescription.objects.all()
    d = {"prescrip": prescrip}
    return render(request, "view_prescription.html", d)


@role_required(['admin','doctor'])
def add_prescription(request):
    error = ""
    patient1 = Patient.objects.all()
    if request.method == "POST":
        p = request.POST["patient"]
        m = request.POST["med"]
        dnd = request.POST["dnd"]
        patient = Patient.objects.filter(name=p).first()
        try:
            Prescription.objects.create(
                patient=patient,
                med=m,
                dnd=dnd,
            )
            error = "no"
        except:
            error = "yes"
    d = {'patient': patient1, 'error': error}
    return render(request, "add_prescription.html", d)


@role_required(['admin'])
def delete_prescription(request, pid):
    prescription = Prescription.objects.get(id=pid)
    prescription.delete()
    return redirect("view_prescription")
