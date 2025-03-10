import pytest
from missions.models import Mission, UserMission, UserBatch, Batch
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

#Missionモデルの作成検証
@pytest.mark.django_db
def test_create_mission():
    batch = Batch.objects.create(name="テストバッチ", description="バッチの説明")
    mission = Mission.objects.create(title="テストミッション", description="ミッションの説明", criteria={}, batch=batch)

    assert mission.title == "テストミッション"
    assert mission.batch == batch

#UserMissionモデルの作成検証
@pytest.mark.django_db
def test_user_mission_creation():
    user = User.objects.create(username="testuser")
    batch = Batch.objects.create(name="テストバッチ", description="バッチの説明")
    mission = Mission.objects.create(title="テストミッション", description="ミッションの説明", criteria={}, batch=batch)
    user_mission = UserMission.objects.create(user=user, mission=mission, is_completed=False)
    
    assert user_mission.user == user
    assert user_mission.mission == mission
    assert user_mission.is_completed is False

#UserMissionの完了検証
@pytest.mark.django_db
def test_user_mission_completion():
    user = User.objects.create(username="testuser")
    batch = Batch.objects.create(name="テストバッチ", description="バッチの説明")  # batch を作成
    mission = Mission.objects.create(title="テストミッション", description="ミッションの説明", criteria={}, batch=batch)
    user_mission = UserMission.objects.create(user=user, mission=mission, is_completed=True, completed_at=now())
    
    assert user_mission.is_completed is True
    assert user_mission.completed_at is not None

#Batchモデルの作成検証
@pytest.mark.django_db
def test_create_batch():
    
    batch = Batch.objects.create(name="テストバッチ", description="バッチの説明")

    assert batch.name == "テストバッチ"
    assert batch.description == "バッチの説明"

#UserBatchモデルの作成検証
@pytest.mark.django_db
def test_user_batch_creation():
    user = User.objects.create(username="testuser")
    batch = Batch.objects.create(name="テストバッチ", description="バッチの説明")
    user_batch = UserBatch.objects.create(user=user, batch=batch)

    assert user_batch.user == user
    assert user_batch.batch == batch

#UserMissionとUserBatchの関連性検証
@pytest.mark.django_db
def test_user_mission_batch_relationship():

    user = User.objects.create(username="testuser")
    batch = Batch.objects.create(name="テストバッチ", description="バッチの説明")  # ✅ 先に作成
    mission = Mission.objects.create(title="テストミッション", description="ミッションの説明", criteria={}, batch=batch)

    mission.batch = batch
    mission.save()

    user_mission = UserMission.objects.create(user=user, mission=mission, is_completed=True, completed_at=now())
    user_batch = UserBatch.objects.create(user=user, batch=batch)

    assert user_mission.is_completed is True
    assert user_batch.batch == mission.batch
