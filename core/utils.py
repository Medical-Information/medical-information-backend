def get_client_ip(request):
    """Get client ip address from HTTP request.

    :param request: HTTP request
    :return: IP Address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return (
        x_forwarded_for.split(',')[-1].strip()
        if x_forwarded_for
        else request.META.get('REMOTE_ADDR')
    )
