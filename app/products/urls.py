from django.urls import path

from products import views 

app_name = "products"

urlpatterns = [
    path("add-product/", views.ProductAddPage.as_view(), name="product_add"),
    path("product-list/", views.ProductListPage.as_view(), name="product_list"),
    path("product-details/<int:pk>/", views.ProductDetailsPage.as_view(), name="product_details"),
    path("product-update/<int:pk>/", views.ProductUpdatePage.as_view(), name="product_update"),
    path("product-delete/<int:pk>/", views.ProductDeletePage.as_view(), name="product_delete"),
    path("product-add-comment/<int:pk>/", views.ProductCommentAddView.as_view(), name="product_add_comment"),
    path("product-add-file/<int:pk>/", views.ProductFileAddView.as_view(), name="product_add_file"),
	path("product-delete-comment/<int:pk>/", views.ProductCommentDeleteView.as_view(), name="product_delete_comment"),
    path("product-delete-file/<int:pk>/", views.ProductFileDeleteView.as_view(), name="product_delete_file"),
    path("product-export/csv/", views.ProductExportCSVView.as_view(), name="product_export_csv"),
]
