def get_client_ip(request):
    """Получает IP-адрес из HTTP-запроса.

    :param request: HTTP-запрос
    :return: IP-адрес
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return (
        x_forwarded_for.split(',')[-1].strip()
        if x_forwarded_for
        else request.META.get('REMOTE_ADDR')
    )
