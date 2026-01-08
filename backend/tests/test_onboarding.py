from unittest.mock import MagicMock, patch

# Use standard imports assuming PYTHONPATH=.
from models import User, Goal, Gender
from routes.onboarding import onboarding


@patch("meal_generator.generate_meal_plan")
def test_calculate_macros_male_weight_loss(mock_generate):
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
    # BMR = 10*80 + 6.25*180 - 5*30 + 5 = 1780
    # TDEE = 1780 * 1.2 = 2136
    # Target = 2136 - 500 = 1636
    assert plan.calories == 1636

    # Verify Macros
    assert plan.protein == 160
    assert plan.fats == 64
    assert plan.carbs == 105
    assert plan.user_id == user.id

    # Verify generate_meal_plan was called
    mock_generate.assert_called_once()


@patch("meal_generator.generate_meal_plan")
def test_calculate_macros_female_muscle_gain(mock_generate):
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
    # BMR = 10*60 + 6.25*165 - 5*25 - 161 = 1345.25
    # TDEE = 1345.25 * 1.55 = 2085.1375
    # Target = 2085 + 300 = 2385
    assert plan.calories == 2385

    # Verify Macros
    assert plan.protein == 120
    assert plan.fats == 48

    mock_generate.assert_called_once()
