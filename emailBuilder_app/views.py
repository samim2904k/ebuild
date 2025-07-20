from django.shortcuts import render, get_object_or_404, redirect
import json
import base64
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from .models import File,Folder,SavedRows

# Create your views here.
def index(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("email")
            password = data.get("password")
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['logged_in'] = True
            return JsonResponse({'message': 'Login successful', 'redirect_url': '/file_manager/'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return render(request, 'index.html')

@method_decorator(csrf_exempt, name='dispatch')
class SaveImageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            image_data = data.get('image')
            json_data = data.get('json')
            html_data = data.get('html')

            if SavedRows.objects.filter(name=name).exists():
                return JsonResponse({"error": "A row with this name already exists."}, status=400)

            if not name or not image_data:
                return JsonResponse({"error": "Invalid data"}, status=400)

            # Decode the image from base64
            image_binary = base64.b64decode(image_data)

            # Save to database
            SavedRows.objects.create(
                name=name,
                image=image_binary,
                json=json_data,  # Store JSON without formatting
                html=html_data
            )

            return JsonResponse({"message": "Saved successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
def get_saved_rows(request):
    rows = SavedRows.objects.values("id", "name", "json", "html")
    return JsonResponse(list(rows), safe=False)

def get_saved_row(request, row_id):
    row = get_object_or_404(SavedRows, id=row_id)
    return JsonResponse({"id": row.id, "name": row.name, "json_data": row.json})

def get_image(request, row_id):
    try:
        row = SavedRows.objects.get(id=row_id)
        return HttpResponse(row.image, content_type="image/png")
    except SavedRows.DoesNotExist:
        return HttpResponse("Image not found", status=404)
    
@csrf_exempt
def delete_saved_row(request, row_id):
    try:
        row = SavedRows.objects.get(id=row_id)
        row.delete()
        return HttpResponse(status=204)
    except SavedRows.DoesNotExist:
        return JsonResponse({"error": "Row not found"}, status=404)

@login_required(login_url='/')
def editor(request):
    return render(request, 'editor.html')

@login_required(login_url='/')
def file_manager(request):
    folders = Folder.objects.all()  # All folders
    files_without_folder = File.objects.filter(folder__isnull=True)  # Only files without a folder

    context = {
        'folders': folders,
        'files': files_without_folder,
    }
    return render(request, 'fileManager.html', context)

@login_required(login_url='/')
def template_list(request):
    email_templates = File.objects.all().order_by('-id')
    return render(request, 'templateList.html', {'email_templates':email_templates})

@csrf_exempt
@login_required(login_url='/')
def create_new_folder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            folder_name = data.get('newFolderName')

            if Folder.objects.filter(name=folder_name).exists():
                return JsonResponse({'error': 'Folder with this name already exists'}, status=400)

            folder = Folder.objects.create(name=folder_name)
            return JsonResponse({'message': 'Folder created successfully', 'redirect_url': '/file_manager'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required(login_url='/')
def create_new_template(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            template_name = data.get('newTempName')

            if File.objects.filter(name=template_name).exists():
                return JsonResponse({'error': 'Template with this name already exists'}, status=400)

            template = File.objects.create(name=template_name)
            template.json_content = '''{
                                "root": {
                                    "type": "EmailLayout",
                                    "data": {
                                    "backdropColor": "#F5F5F5",
                                    "canvasColor": "#FFFFFF",
                                    "textColor": "#262626",
                                    "fontFamily": "MODERN_SANS",
                                    "childrenIds": []
                                    }
                                }
                                }'''
            template.save()

            return JsonResponse({'message': 'Template created successfully', 'redirect_url': '/file_manager'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Open Folder View
@login_required(login_url='/')
def folder_contents(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    files = File.objects.filter(folder=folder)
    return render(request, 'folderContent.html', {'folder': folder, 'files': files})

# Move File to Folder
@login_required(login_url='/')
def move_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            file = get_object_or_404(File, id=data['file_id'])
            folder = get_object_or_404(Folder, id=data['folder_id'])

            file.folder = folder
            file.save()

            return JsonResponse({'success': True, 'message': 'File moved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required(login_url='/')
def edit_email(request, file_id):
    file = get_object_or_404(File, id=file_id)
    return render(request, 'editor.html', {'file': file})

@login_required(login_url='/')
def save_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print(data)
            file_id = data.get('file_id')
            content = data.get('content')  # The HTML content

            if not file_id or not content:
                return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

            file = get_object_or_404(File, id=file_id)
            file.content = content  # Save HTML template
            file.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'invalid request'}, status=400)

@login_required(login_url='/')
def get_email_json(request, file_id):
    print('entered')
    try:
        file = get_object_or_404(File, id=file_id)
        print(file.json_content)
        return JsonResponse({'content': file.json_content})
    except File.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No template found'}, status=404)

@login_required(login_url='/')
def save_email_json(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            file_id = data.get('file_id')
            json_content = data.get('content')
            print(json_content)

            if not file_id or not json_content:
                return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

            file = get_object_or_404(File, id=file_id)
            file.json_content = json_content  # Save JSON template
            file.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'invalid request'}, status=400)

@login_required(login_url='/')
def download_template(request, template_id):
    file = get_object_or_404(File, id=template_id)
    response = HttpResponse(file.content, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="{file.name}.html"'
    return response

@csrf_exempt
@login_required(login_url='/')
def delete_template(request, template_id):
    if request.method == 'DELETE':
        try:
            file = get_object_or_404(File, id=template_id)
            file.delete()
            return JsonResponse({'success': True, 'message': 'Template deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
@login_required(login_url='/')
def delete_folder(request, folder_id):
    if request.method == 'DELETE':
        try:
            folder = get_object_or_404(Folder, id=folder_id)
            
            with transaction.atomic():
                # Delete all files in the folder
                File.objects.filter(folder=folder).delete()
                # Delete the folder itself
                folder.delete()

            return JsonResponse({'success': True, 'message': 'Folder and its contents deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
@login_required(login_url='/')
def rename_folder(request, folder_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_name = data.get('new_name')

        try:
            folder = Folder.objects.get(id=folder_id)
            folder.name = new_name
            folder.save()
            return JsonResponse({'success': True})
        except Folder.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Folder not found'})

@csrf_exempt
@login_required(login_url='/')
def rename_file(request, file_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_name = data.get('new_name')

        try:
            file = File.objects.get(id=file_id)
            file.name = new_name
            file.save()
            return JsonResponse({'success': True})
        except File.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'File not found'})
        
@csrf_exempt
@login_required(login_url='/')
def create_template_in_folder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            folder_id = data.get('folder_id')
            template_name = data.get('template_name')

            if not folder_id or not template_name:
                return JsonResponse({'error': 'Missing folder ID or template name'}, status=400)

            folder = get_object_or_404(Folder, id=folder_id)

            if File.objects.filter(name=template_name, folder=folder).exists():
                return JsonResponse({'error': 'Template with this name already exists in this folder'}, status=400)

            template = File.objects.create(
                name=template_name,
                folder=folder,
                json_content='''{
                    "root": {
                        "type": "EmailLayout",
                        "data": {
                            "backdropColor": "#F5F5F5",
                            "canvasColor": "#FFFFFF",
                            "textColor": "#262626",
                            "fontFamily": "MODERN_SANS",
                            "childrenIds": []
                        }
                    }
                }'''
            )

            return JsonResponse({'message': 'Template created successfully', 'redirect_url': f'/file_manager/{folder_id}/'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required(login_url='/')
def remove_from_folder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            file_id = data.get('file_id')

            file = File.objects.get(id=file_id)
            file.folder = None  # Remove from folder
            file.save()

            return JsonResponse({'success': True, 'message': 'File removed from folder successfully'})
        except File.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'File not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def logOut(request):
    logout(request) 
    return redirect('/') 