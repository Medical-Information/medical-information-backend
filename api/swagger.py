   from drf_yasg.views import get_schema_view
   from drf_yasg import openapi

   schema_view = get_schema_view(
       openapi.Info(
           title="API Documentation",
           default_version='v1',
           description="API documentation powered by Swagger",
           terms_of_service="https://stethoscope.acceleratorpracticum.ru/terms/",
           contact=openapi.Contact(email="info@stethoscope.acceleratorpracticum.ru"),
           license=openapi.License(name="BSD License"),
       ),
       public=True,
   )
