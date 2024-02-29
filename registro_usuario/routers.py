class SoftwareEmpresaRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'registro_usuario':
            return 'empresa_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'registro_usuario':
            return 'default'
        return 'default'

    

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'empresa_db':
            return app_label == 'registro_usuario'
        elif app_label == 'registro_usuario':
            return False
        return None
