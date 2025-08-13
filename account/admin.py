# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth import get_user_model
# from django.contrib import messages
# from .models import Delete

# User = get_user_model()

# # Only allow staff (admin) users
# def is_admin(user):
#     return user.is_staff

# @login_required
# @user_passes_test(is_admin)
# def custom_admin_dashboard(request):
#     users = User.objects.all()
#     deleted_users = Delete.objects.all().order_by('-id')
#     return render(request, 'custom_admin_dashboard.html', {
#         'users': users,
#         'deleted_users': deleted_users
#     })


# @login_required
# @user_passes_test(is_admin)
# def delete_user_admin(request, user_id):
#     user = get_object_or_404(User, id=user_id)

#     # Save to Delete table before removing
#     Delete.objects.create(
#         username=user.username,
#         first_name=user.first_name,
#         last_name=user.last_name,
#         school=user.school,
#         email=user.email,
#         is_deleted=True
#     )

#     user.delete()
#     messages.success(request, f"User {user.username} deleted successfully.")
#     return redirect('custom_admin_dashboard')
