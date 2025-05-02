from handlers.start_handler import register_start_handler
from handlers.text_handler import register_text_handler
from handlers.callback_handler import register_callback_handler
from handlers.error_handler import register_error_handler
from handlers.admin_handler import register_admin_handler

def register_all_handlers(application):
    register_start_handler(application)
    register_text_handler(application)
    register_callback_handler(application)
    register_error_handler(application)
    register_admin_handler(application)