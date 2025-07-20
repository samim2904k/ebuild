function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  };

function showLoadingScreen() {
    $('.loader-wrapper').css('display', 'block');
       
}

function hideLoadingScreen() {
    $('.loader-wrapper').css('display', 'none');
}

function logInVerification(event) {
    event.preventDefault();
    showLoadingScreen();
var email = document.getElementById('username').value;
var password = document.getElementById('password').value;

if (!email || !password) {
    toastr.error('Please fill in all the required fields.', 'Error');
} else {
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            toastr.error(data.error, 'Error');
        } else {
            toastr.success(data.message, 'Success');
            setTimeout(function() {
                window.location.href = data.redirect_url;  
            }, 2000);
        }
    })
    .catch(error => {
        toastr.error('There was a problem submitting the form.', 'Error');
        console.error('There was a problem with the fetch operation:', error);
    });
}
setTimeout(function() {
    hideLoadingScreen();
}, 3000);

}

function createTemplate(){
    showLoadingScreen();

    const newTempName = document.getElementById('newTempName').value;
    
if (!newTempName) {
    toastr.error('Please fill in the template name', 'Error');
} else {
    fetch('/create_new_template', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  
        },
        body: JSON.stringify({
            newTempName : newTempName
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            toastr.error(data.error, 'Error');
        } else {
            toastr.success(data.message, 'Success');
            setTimeout(function() {
                window.location.href = data.redirect_url;  
            }, 2000);
        }
    })
    .catch(error => {
        toastr.error('There was a creating the template.', 'Error');
        console.error('There was a problem with the fetch operation:', error);
    });
}
setTimeout(function() {
    hideLoadingScreen();
}, 3000);

}


function createFolder(){
    showLoadingScreen();

    const newFolderName = document.getElementById('newFolderName').value;
    
if (!newFolderName) {
    toastr.error('Please fill in the Folder name', 'Error');
} else {
    fetch('/create_new_folder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  
        },
        body: JSON.stringify({
            newFolderName : newFolderName
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            toastr.error(data.error, 'Error');
        } else {
            toastr.success(data.message, 'Success');
            setTimeout(function() {
                window.location.href = data.redirect_url;  
            }, 2000);
        }
    })
    .catch(error => {
        toastr.error('There was a creating the template.', 'Error');
        console.error('There was a problem with the fetch operation:', error);
    });
}
setTimeout(function() {
    hideLoadingScreen();
}, 3000);

}

function drag(event) {
    const fileId = event.target.getAttribute('data-file-id');
    console.log('Dragging file with ID:', fileId);
    if (fileId) {
        event.dataTransfer.setData('fileId', fileId);
    } else {
        console.error('File ID is missing');
    }
}

function allowDrop(event) {
    event.preventDefault();
}

function drop(event, folderId) {
    event.preventDefault();
    const fileId = event.dataTransfer.getData('fileId');

    // ✅ Show confirmation dialog before moving the file
    Swal.fire({
        title: 'Move File?',
        text: 'Are you sure you want to move this file?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, move it!',
        cancelButtonText: 'Cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            // ✅ Proceed with the file move
            fetch(`/move_file/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ file_id: fileId, folder_id: folderId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: 'Success!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        window.location.reload();
                    });
                } else {
                    Swal.fire({
                        title: 'Error!',
                        text: data.error,
                        icon: 'error',
                        confirmButtonColor: '#d33',
                        confirmButtonText: 'OK'
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    title: 'Error!',
                    text: 'Something went wrong',
                    icon: 'error',
                    confirmButtonColor: '#d33',
                    confirmButtonText: 'OK'
                });
                console.error('Error:', error);
            });
        }
    });
}

function openFolder(folderId) {
    window.location.href = `/folder/${folderId}/`;
}


function deleteTemplate(templateId) {
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            showLoadingScreen();
            fetch(`/delete_template/${templateId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    hideLoadingScreen();
                    Swal.fire({
                        title: "Deleted!",
                        text: data.message,
                        icon: "success"
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    hideLoadingScreen();
                    Swal.fire({
                        title: "Error!",
                        text: data.error,
                        icon: "error"
                    });
                }
            });
        }
    });
}

function deleteFolder(folderId) {
    Swal.fire({
        title: "Are you sure?",
        text: "This will delete the folder and all its contents. This action cannot be undone!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            showLoadingScreen();
            fetch(`/delete_folder/${folderId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            }).then(response => response.json())
            .then(data => {
                hideLoadingScreen();
                if (data.success) {
                    Swal.fire({
                        title: "Deleted!",
                        text: data.message,
                        icon: "success"
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire({
                        title: "Error!",
                        text: data.error,
                        icon: "error"
                    });
                }
            }).catch(error => {
                hideLoadingScreen();
                Swal.fire({
                    title: "Error!",
                    text: "Something went wrong. Please try again later.",
                    icon: "error"
                });
                console.error('Error:', error);
            });
        }
    });
}

function openRenameModal(id, type, name) {
    document.getElementById('rename-item-id').value = id;
    document.getElementById('rename-item-type').value = type;
    document.getElementById('oldName').innerText = name;
}

function confirmRename() {
    const id = document.getElementById('rename-item-id').value;
    const type = document.getElementById('rename-item-type').value;
    const newName = document.getElementById('rename-item-name').value;

    if (!newName.trim()) {
        Swal.fire({
            icon: 'warning',
            title: 'Oops...',
            text: 'Name cannot be empty!'
        });
        return;
    }

    Swal.fire({
        title: `Are you sure you want to rename this ${type}?`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Yes, rename it!',
        cancelButtonText: 'No, cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            showLoadingScreen();
            fetch(`/rename-${type}/${id}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Django CSRF token
                },
                body: JSON.stringify({ new_name: newName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    hideLoadingScreen();
                    Swal.fire({
                        icon: 'success',
                        title: `${type.charAt(0).toUpperCase() + type.slice(1)} renamed successfully!`,
                        timer: 1500,
                        showConfirmButton: false
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    hideLoadingScreen();
                    Swal.fire({
                        icon: 'error',
                        title: 'Failed to rename',
                        text: `Failed to rename ${type}.`
                    });
                }
            })
            .catch(error => {
                hideLoadingScreen();
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Something went wrong!',
                    text: 'Please try again later.'
                });
            });
        }
    });
}

function createTemplateInFolder() {
    const folderId = document.getElementById('newTempFolderId').value;
    const templateName = document.getElementById('newTemplateName').value;

    if (!templateName) {
        Swal.fire({
            icon: 'warning',
            title: 'Missing Template Name',
            text: 'Please enter a template name!'
        });
        return;
    }

    showLoadingScreen();

    fetch('/create_template_in_folder/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Django CSRF token
        },
        body: JSON.stringify({
            folder_id: folderId,
            template_name: templateName,
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingScreen();
        if (data.error) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: data.error
            });
        } else {
            Swal.fire({
                icon: 'success',
                title: 'Success!',
                text: data.message
            }).then(() => {
                window.location.reload();
            });
        }
    })
    .catch(error => {
        hideLoadingScreen();
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Unexpected Error',
            text: 'An unexpected error occurred. Please try again later.'
        });
    });
}

function removeFromFolder(fileId) {
    Swal.fire({
        title: 'Remove File from Folder?',
        text: "This will remove the file from its folder but not delete it.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, remove it!',
        cancelButtonText: 'Cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/remove_from_folder/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ file_id: fileId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: 'Removed!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        window.location.reload(); // Reload page to update UI
                    });
                } else {
                    Swal.fire({
                        title: 'Error!',
                        text: data.error,
                        icon: 'error',
                        confirmButtonColor: '#d33',
                        confirmButtonText: 'OK'
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    title: 'Error!',
                    text: 'Something went wrong',
                    icon: 'error',
                    confirmButtonColor: '#d33',
                    confirmButtonText: 'OK'
                });
                console.error('Error:', error);
            });
        }
    });
}

function searchFilesAndFolders() {
    let input = document.getElementById('searchInput').value.toLowerCase();
    let fileItems = document.querySelectorAll('.nk-file-item'); 

    fileItems.forEach(item => {
        let titleElement = item.querySelector('.nk-file-name .title');
        if (titleElement) {
            let titleText = titleElement.textContent.toLowerCase();
            if (titleText.includes(input)) {
                item.style.display = '';  
            } else {
                item.style.display = 'none';  
            }
        }
    });
}

function searchFiles() {
    let input = document.getElementById('fileSearchInput').value.toLowerCase();
    let fileItems = document.querySelectorAll('.nk-file-item'); // Select all files

    fileItems.forEach(item => {
        let titleElement = item.querySelector('.nk-file-name .title');
        if (titleElement) {
            let titleText = titleElement.textContent.toLowerCase();
            if (titleText.includes(input)) {
                item.style.display = '';  // Show matched files
            } else {
                item.style.display = 'none';  // Hide non-matching files
            }
        }
    });
}

function confirmLogout(event) {
    event.preventDefault();

    Swal.fire({
        title: "Are you sure?",
        text: "You will be logged out!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, log out"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/log-out/"; 
        }
    });
}