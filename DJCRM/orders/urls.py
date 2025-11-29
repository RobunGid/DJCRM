from django.urls import path

from orders import views 

app_name = "orders"

urlpatterns = [
	path("order-create/", views.OrderCreatePage.as_view(), name="order_add"),
    path("order-list/", views.OrderListPage.as_view(), name="order_list"),
    path("order-details/<int:pk>/", views.OrderDetailsPage.as_view(), name="order_details"),
    path("order-update/<int:pk>/", views.OrderUpdatePage.as_view(), name="order_update"),
    path("order-delete/<int:pk>/", views.OrderDeletePage.as_view(), name="order_delete"),
    path("order-add-comment/<int:pk>/", views.OrderCommentAddView.as_view(), name="order_add_comment"),
    path("order-add-file/<int:pk>/", views.OrderFileAddView.as_view(), name="order_add_file"),
    path("order-export/csv/", views.OrderExportCSVView.as_view(), name="order_export_csv"),
]
