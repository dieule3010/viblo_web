from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from .models import Profile
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect #redirect: Hàm để chuyển hướng người dùng đến một URL khác.



def home(request):
    return render(request, 'home.html', {})
def about(request):
    return render(request, 'about.html', {})
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        print(f"Username: {user_name}, Password: {password}")

        if user_name and password:
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You're successful!")
                return redirect('home')
            else:
                messages.error(request, "Username or Password is incorrect!")
        else:
            messages.error(request, "You haven't filled out enough information.")

        return redirect('login')
    else:
        return render(request, 'login.html', {})
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out...Thanks for stopping by...")
    return redirect('home')
def user_register(request):
    if request.method == "POST":#gửi yêu cầu
        form = SignUpForm(request.POST)# khởi tạo form
        if form.is_valid(): #Ktra form hợp lệ không
            user = form.save()  # Save the form to create the user
            username = form.cleaned_data['username'] #Lấy tên người dùng từ dữ liệu đã được làm sạch.
            password = form.cleaned_data['password1']#đảm bảo dữ liệu là an toàn

            # Log in the user after registration
            user = authenticate(username=username, password=password) # xác thực người dùng
            login(request, user) # xác thực thành công, đăng nhập

            messages.success(request, "You have registered successfully. Welcome!")
        else:
            messages.error(request, "There was a problem with registration.")
            return redirect('register')  # Redirect back to registration page if form is invalid
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})
def update_info(request):
    if request.user.is_authenticated:
        # Lấy Profile của người dùng hoặc trả về 404 nếu không tồn tại
        current_user = get_object_or_404(Profile, user=request.user)

        # Tạo biểu mẫu, khởi tạo với thông tin hiện tại
        form = UserInfoForm(request.POST or None, instance=current_user)

        if request.method == 'POST':
            # Nếu biểu mẫu hợp lệ thì tiến hành lưu dữ liệu
            if form.is_valid():
                form.save()
                messages.success(request, "Your Info Has Been Updated!")
                return redirect('home')
            else:
                messages.error(request, "Please correct the errors below.")

        # Render trang cập nhật thông tin
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.error(request, "You Must Be Logged In to Access That Page!")
        return redirect('home')
def update_password(request):
    if request.user.is_authenticated: #kiểm tra xem người dùng hiện tại đã đăng nhập chưa. Nếu chưa đăng nhập, người dùng sẽ không được phép truy cập trang cập nhật mật khẩu và sẽ được chuyển hướng về trang chính (home).
        current_user = request.user
        if request.method == 'POST':#Kiểm tra xem yêu cầu HTTP là POST hay không. Yêu cầu POST là khi người dùng gửi dữ liệu form, trong trường hợp này là thông tin thay đổi mật khẩu.
            form = ChangePasswordForm(current_user, request.POST) #ChangePasswordForm(current_user, request.POST) khởi tạo form với dữ liệu từ yêu cầu POST. current_user được truyền vào để liên kết với người dùng hiện tại.
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been changed.")
                return redirect('login')
            else:
                for error in form.errors.values():  # Sửa lại cách lấy lỗi từ form
                    messages.error(request, error)
        else:
            form = ChangePasswordForm(current_user) #Nếu yêu cầu không phải là POST (thường là GET), form sẽ được khởi tạo với đối tượng người dùng hiện tại mà không có dữ liệu POST. Sau đó, form sẽ được gửi đến template để hiển thị.
        return render(request, "update_password.html", {'form': form})
    else:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('home')


# def update_user(request):
#   if request.user.is_authenticated:
#       current_user = User.objects.get(id = request.user.id)
#       user_form = UpdateUserForm(request.POST or None, instance = current_user)
#       if user_form.is_valid():
#          user_form.save()
#          login(request, current_user)
#          messages.success(request, "User Has Been Updated!!")
#          return redirect('home')
#       return render(request, 'update_user.html', {'user_form' : user_form})
#   else:
#          messages.success(request, "You Must Be Logged In to Access That Page!!")
#          return redirect('home')

#   return render(request, 'update_user.html', {})