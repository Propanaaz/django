from django.urls import path
from receipt import views

urlpatterns = [
    path("",views.index,name="index"),
    path("add_transaction", views.add_transaction,name="add_transaction"),
    path("user_registration", views.user_registration, name="user_registration"),
    path("user_login", views.user_login, name="user_login"),
    path("user_dashboard", views.user_dashboard, name="user_dashboard"),
    path("upload_logo", views.upload_logo, name="upload_logo"),
    path("upload_signature", views.upload_signature, name="upload_signature"),
    path("all_transaction", views.all_transaction, name="all_transaction"),
    path("query_transaction/<str:search>", views.query_transaction, name="query_transaction"),
    path("query_transaction1", views.query_transaction1, name="query_transaction1"),
    path("query_receipt/<str:id>", views.query_receipt, name="query_receipt"),
    path("receipt/<str:id>", views.receipt, name="receipt"),
    path("receipt2/<str:id>", views.receipt2, name="receipt2"),
    path("plot", views.plot, name="plot"),
    path("update_profile", views.update_profile, name="update_profile"),
    path("logout", views.logout, name="logout"),
    path("delete_receipt/<int:id>", views.delete_receipt, name="delete_receipt"),
    path("yek", views.key, name="key"),
    path("verify_email/<str:id>", views.verify_email, name="verify_email"),
    path("change_password", views.change_password, name="change_password"),
    path("forgotten_password", views.forgotten_password, name="forgotten_password"),
    path("verify_forgotten_password/<str:id>", views.verify_forgotten_password, name="verify_forgotten_password"),
    path("change_password2/<str:id>", views.change_password2, name="change_password2"),
    path("admin_login", views.admin_login, name="admin_login"),
    path("admin_dashboard", views.admin_dashboard, name="admin_dashboard"),
    path("all_transactions", views.all_transactions, name="all_transactions"),
    path("all_user", views.all_user, name="all_user"),
    path("admin_query_receipt/<str:id>/<str:username>", views.admin_query_receipt, name="admin_query_receipt"),
    path("admin_delete_receipt/<str:id>", views.admin_delete_receipt, name="admin_delete_receipt"),
    path("admin_query_transaction/<str:search>", views.admin_query_transaction, name="admin_query_transaction"),
    path("admin_query_transaction1", views.admin_query_transaction1, name="admin_query_transaction1"),
    path("admin_query_user1", views.admin_query_user1, name="admin_query_user1"),
    path("admin_query_user/<str:search>", views.admin_query_user, name="admin_query_user"),
    path("admin_logout", views.admin_logout, name="admin_logout"),
    path("change_receipt", views.change_receipt, name="change_receipt"),
    path("admin_delete_user/<int:id>", views.admin_delete_user, name="admin_delete_user"),
    path("index2", views.index2, name="index2"),














]

