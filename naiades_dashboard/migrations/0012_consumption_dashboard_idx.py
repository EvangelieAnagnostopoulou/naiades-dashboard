from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naiades_dashboard', '0011_auto_20220307_1636'),
    ]

    operations = [
        migrations.RunSQL(
            """
                DROP INDEX IF EXISTS naiades_dashboard_consumption_date_idx;
                
                CREATE INDEX naiades_dashboard_consumption_date_idx 
                ON naiades_dashboard_consumption (date) 
                WHERE day <= 4 AND in_dashboard = true
            """,
            reverse_sql="""
                DROP INDEX IF EXISTS naiades_dashboard_consumption_date_idx
            """
        )
    ]
