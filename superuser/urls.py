from django.urls import path
from . import views
urlpatterns=[
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),

    path('Admin_products/',views.Admin_products,name='Admin_products'),
    path('add_product/',views.add_product,name='add_product'),

    path('admin_category/',views.admin_category,name='admin_category'),
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
    path('update_product/<int:id>',views.update_product,name='update_product'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),


    path('customers/',views.customers,name='customers'),
    path('blocked_customers/',views.blocked_customers,name='blocked_customers'),
    path('block/<int:id>',views.block,name='block'),
    path('unblock/<int:id>',views.unblock,name='unblock'),


    path('orders/',views.orders,name='orders'),
    path('accept_order/<int:id>',views.accept_order,name='accept_order'),
    path('reject_order/<int:id>',views.reject_order,name='reject_order'),
    path('order_progress/',views.order_progress,name='order_progress'),
    path('completed_orders/',views.completed_orders,name='completed_orders'),
    path('delivery/<int:id>',views.delivery,name='delivery'),


    path('coupons/',views.coupons,name='coupons'),
    path('add_coupon/',views.add_coupon,name='add_coupon'),

    path('all_report/',views.all_report,name='all_report'),
    path('sales_report_daily',views.sales_report_daily,name='sales_report_daily'),
    path('sales_report_weekly/',views.sales_report_weekly,name='sales_report_weekly'),
    path('sales_report_yearly/',views.sales_report_yearly,name='sales_report_yearly'),
    path('sales_report_custom/',views.sales_report_custom,name='sales_report_custom'),


    path('offers/',views.offers,name='offers'),
    path('category_offers/',views.category_offers,name='category_offers'),
    path('add_new_Product_offer/',views.add_new_product_offer,name='add_new_Product_offer'),
    path('add_new_category_offer/',views.add_new_category_offer,name='add_new_category_offer'),
    path('edit_category_offer/<int:id>',views.edit_category_offer,name='edit_category_offer'),
    path('edit_product_offer/<int:id>',views.edit_product_offer,name='edit_product_offer'),
    path('delete_product_offer/<int:id>',views.delete_product_offer,name='delete_product_offer'),
    path('delete_category_offer/<int:id>',views.delete_category_offer,name='delete_category_offer'),

    path('export_csv_daily',views.export_csv_daily,name='export_csv_daily'),
    path('export_csv_weekly',views.export_csv_weekly,name='export_csv_weekly'),
    path('export_csv_yearly',views.export_csv_yearly,name='export_csv_yearly'),
    path('export_csv_custom',views.export_csv_custom,name='export_csv_custom'),


    path('export_excel_daily',views.export_excel_daily,name='export_excel_daily'),
    path('export_excel_weekly',views.export_excel_weekly,name='export_excel_weekly'),
    path('export_excel_yearly',views.export_excel_yearly,name='export_excel_yearly'),
    path('export_excel_custom',views.export_excel_custom,name='export_excel_custom'),


]