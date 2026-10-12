from django.contrib.auth.mixins import UserPassesTestMixin


class RoleRequiredMixin(UserPassesTestMixin):
    """Restrict a view to one or more roles. Set `allowed_roles = ['ADMIN', ...]`."""

    allowed_roles = []
    raise_exception = False

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_superuser or user.role in self.allowed_roles
        )

    def handle_no_permission(self):
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(self.request, "You don't have permission to access that page.")
        return redirect('accounts:dashboard')


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN']


class StaffRequiredMixin(RoleRequiredMixin):
    """Admins and teachers."""
    allowed_roles = ['ADMIN', 'TEACHER']
