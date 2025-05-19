from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Pozwala edytować tylko jeśli użytkownik jest autorem posta.
    """

    def has_object_permission(self, request, view, obj):
        # Bezpieczne metody (GET, HEAD, OPTIONS) zawsze dozwolone
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True

        # Zapis (PUT, PATCH, DELETE) tylko dla autora posta
        return obj.author == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Pozwala na zapis tylko administratorom. Czytanie dla wszystkich.
    """

    def has_permission(self, request, view):
        # Bezpieczne metody (GET, HEAD, OPTIONS) zawsze dozwolone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Inne metody (POST, PUT, DELETE) tylko dla adminów
        return request.user and request.user.is_staff

class IsProfileAuthorOrReadOnly(permissions.BasePermission):
    """
    Pozwala edytować tylko jeśli użytkownik jest autorem profilu.
    """

    def has_object_permission(self, request, view, obj):
        # Bezpieczne metody (GET, HEAD, OPTIONS) zawsze dozwolone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Zapis (PUT, PATCH, DELETE) tylko dla autora profilu
        return obj.user == request.user