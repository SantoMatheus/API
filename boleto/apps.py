from datetime import datetime, timedelta

from django.apps import AppConfig

# from cron.atualiza_para_vencido_task import atualiza_status_para_vencido


class BoletoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boleto'

    # def ready(self):
    #     scheduler = BackgroundScheduler()
    #     agora = datetime.now()
    #     agendamento = (agora + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    #
    #     scheduler.add_job(atualiza_status_para_vencido, trigger='interval', days=1, start_date=agendamento)
    #     scheduler.start()
