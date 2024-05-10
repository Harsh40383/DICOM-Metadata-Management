# dicom/views.py

from django.shortcuts import render, redirect
from .forms import DICOMUploadForm
from .models import DICOMMetadata
import pydicom
from django.db.models import Q
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from datetime import datetime
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or another view
                return redirect('/')  # Redirect to home page after successful login
            else:
                # Handle invalid login credentials
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def upload_dicom(request):
    if request.method == 'POST':
        form = DICOMUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dicom_file = request.FILES['dicom_file']
            metadata = extract_dicom_metadata(dicom_file)
            dicom_metadata = DICOMMetadata.objects.create(**metadata)
            return render(request, 'success.html', {'metadata': metadata})
    else:
        form = DICOMUploadForm()
    return render(request, 'upload.html', {'form': form})

def extract_dicom_metadata(dicom_file):
    metadata = {}
    ds = pydicom.dcmread(dicom_file)

    # Patient information
    metadata['patient_name'] = getattr(ds, 'PatientName', 'Unknown')
    metadata['patient_id'] = getattr(ds, 'PatientID', 'Unknown')
    metadata['birthdate'] = parse_dicom_date(getattr(ds, 'PatientBirthDate', None))

    # Study details
    metadata['study_id'] = getattr(ds, 'StudyID', 'Unknown')
    metadata['study_description'] = getattr(ds, 'StudyDescription', 'Unknown')
    metadata['study_date'] = parse_dicom_date(getattr(ds, 'StudyDate', None))

    # Image attributes
    metadata['modality'] = getattr(ds, 'Modality', 'Unknown')
    metadata['pixel_spacing'] = getattr(ds, 'PixelSpacing', 'Unknown')

    return metadata

def parse_dicom_date(date_string):
    """
    Parse DICOM date string and return a formatted date string (YYYY-MM-DD).
    """
    if date_string:
        try:
            # Parse date string using DICOM date format (YYYYMMDD)
            date = datetime.strptime(date_string, '%Y%m%d')
            # Convert date to YYYY-MM-DD format
            return date.strftime('%Y-%m-%d')
        except ValueError:
            return None  # Return None if date parsing fails
    return None

    
@login_required
def show(request):
    data = DICOMMetadata.objects.all()
    return render(request, 'show.html', {'data':data})

@login_required
def search_list(request):
    query = request.GET.get('q')
    if query:
        data = DICOMMetadata.objects.filter(Q(patient_name__icontains=query) | Q(study_id__icontains=query) | Q(study_date__icontains=query))
    else:
        data = DICOMMetadata.objects.all()
    return render(request, 'show.html', {'data': data} )


