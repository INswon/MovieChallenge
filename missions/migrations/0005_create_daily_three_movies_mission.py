from django.db import migrations, models


def create_daily_three_movies_mission(apps, schema_editor):
    Mission = apps.get_model("missions", "Mission")
    Batch = apps.get_model("missions", "Batch")

    # すでに同趣旨のミッションがあれば何もしない
    existing = Mission.objects.filter(
        title__in=[
            "1日3本の映画視聴達成",
            "1日3作品の映画視聴達成",
            "1日3作品視聴達成",
            "1日に3本の映画を視聴する",
            "1日に3本の映画を視聴する。",
            "1日3作品の映画映画視聴達成",
        ]
    ).first()

    if existing:
        mission = existing
    else:
        mission = Mission.objects.create(
            title="1日3本の映画視聴達成",
            description="1日に3本の映画を視聴する。",
            criteria={"min_watch_count": 3, "same_day": True},
        )

    # 対応するバッジを作成（存在しなければ）
    Batch.objects.get_or_create(
        mission=mission,
        name="1日3本の映画視聴達成バッジ",
        defaults={
            "description": "1日に3本の映画を視聴達成",
            "condition": {},
        },
    )


def reverse_func(apps, schema_editor):
    # データマイグレーションのロールバックでは特に削除しない
    # （ユーザー環境で作成済みのミッション／バッジを守るため）
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("missions", "0004_remove_batch_icon_alter_batch_condition"),
    ]

    operations = [
        migrations.RunPython(create_daily_three_movies_mission, reverse_func),
    ]

