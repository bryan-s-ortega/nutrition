# Allow running tests from either the repo root (package import) or from within `backend/`.
try:
    from backend.models import User, Goal, Gender
    from backend.routes.onboarding import onboarding
except ImportError:  # pragma: no cover
    from models import User, Goal, Gender
    from routes.onboarding import onboarding
# Mock session since we only want to test logic, but onboarding function uses database session.
# However, the logic is intermixed with DB calls in the current implementation.
# We should probably refactor the logic out or mock the session.
# For simplicity in this step, I will refactor the logic into a purely functional helper in the route or models
# to make it easily testable, OR I can mock the session.
# Let's try to mock the session.

from unittest.mock import MagicMock


def test_calculate_macros_male_weight_loss():
    # Setup
    user = User(
        age=30,
        weight=80,  # kg
        height=180,  # cm
        gender=Gender.MALE,
        goal=Goal.WEIGHT_LOSS,
        activity_level=1.2,
    )

    mock_session = MagicMock()

    # Act
    plan = onboarding(user, session=mock_session)

    # Verify BMR (Mifflin-St Jeor)
    # BMR = 10*80 + 6.25*180 - 5*30 + 5
    # BMR = 800 + 1125 - 150 + 5 = 1780
    # TDEE = 1780 * 1.2 = 2136
    # Target = 2136 - 500 = 1636

    assert plan.calories == 1636

    # Verify Macros
    # Protein: 2 * 80 = 160g (160*4 = 640 kcal)
    # Fats: 0.8 * 80 = 64g (64*9 = 576 kcal)
    # Remaining: 1636 - 640 - 576 = 420 kcal
    # Carbs: 420 / 4 = 105g

    assert plan.protein == 160
    assert plan.fats == 64
    assert plan.carbs == 105
    assert plan.user_id == user.id


def test_calculate_macros_female_muscle_gain():
    # Setup
    user = User(
        age=25,
        weight=60,
        height=165,
        gender=Gender.FEMALE,
        goal=Goal.MUSCLE_GAIN,
        activity_level=1.55,
    )

    mock_session = MagicMock()

    # Act
    plan = onboarding(user, session=mock_session)

    # Verify BMR
    # BMR = 10*60 + 6.25*165 - 5*25 - 161
    # BMR = 600 + 1031.25 - 125 - 161 = 1345.25
    # TDEE = 1345.25 * 1.55 = 2085.1375
    # Target = 2085 + 300 = 2385

    assert plan.calories == 2385

    # Protein: 2 * 60 = 120g
    # Fats: 0.8 * 60 = 48g
    assert plan.protein == 120
    assert plan.fats == 48
