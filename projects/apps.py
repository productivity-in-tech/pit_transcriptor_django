from django.apps import AppConfig

class ProjectsConfig(AppConfig):
    name = 'projects'

    def ready(self):
        from django_q.tasks import schedule

        schedule(
                'projects.tasks.check_for_new_files',
                schedule_type='H',
                )
