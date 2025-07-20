from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('editor/', views.editor, name='editor'),
    path('file_manager/', views.file_manager, name='file_manager'),
    path('templateList/', views.template_list, name='templateList'),
    path('create_new_folder', views.create_new_folder, name='create_new_folder'),
    path('create_new_template', views.create_new_template, name='create_new_template'),
    path('folder/<int:folder_id>/', views.folder_contents, name='folder_contents'),
    path('move_file/', views.move_file, name='move_file'),
    path('folder/<int:folder_id>/', views.folder_contents, name='folder_contents'),
    path('edit-email/<int:file_id>/', views.edit_email, name='edit_email'),
    path('save-email/', views.save_email, name='save_email'),
    path('save-email-json/', views.save_email_json, name='save_email_json'),
    path('get-email-json/<int:file_id>/', views.get_email_json, name='get_email_json'),
    path('download_template/<int:template_id>/', views.download_template, name='download_template'),
    path('delete_template/<int:template_id>/', views.delete_template, name='delete_template'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('rename-file/<int:file_id>/',views.rename_file,name="rename_file"),
    path('rename-folder/<int:folder_id>/',views.rename_folder,name="rename_folder"),
    path('create_template_in_folder/', views.create_template_in_folder, name='create_template_in_folder'),
    path('remove_from_folder/', views.remove_from_folder, name='remove_from_folder'),
    path("get-saved-rows/", views.get_saved_rows, name="get-saved-rows"),
    path("get-saved-row/<int:row_id>/", views.get_saved_row, name="get_saved_row"),
    path("delete-saved-row/<int:row_id>/", views.delete_saved_row, name="delete-saved-row"),
    path("get-image/<int:row_id>/", views.get_image, name="get-image"),
    path('save-image/', views.SaveImageView.as_view(), name='save-image'),
    path('log-out/', views.logOut,name='logOut')
]