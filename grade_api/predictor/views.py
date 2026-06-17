import joblib
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path

# Load model once when server starts
BASE_DIR = Path(__file__).resolve().parent.parent.parent
model = joblib.load(BASE_DIR / "student_model.pkl")

@api_view(['POST'])
def predict(request):
    try:
        data = request.data

        g1 = float(data['g1'])
        g2 = float(data['g2'])
        failures = float(data['failures'])
        studytime = float(data['studytime'])
        medu = float(data['medu'])
        fedu = float(data['fedu'])

        input_data = np.array([[g2, g1, failures, studytime, medu, fedu]])
        prediction = round(float(model.predict(input_data)[0]), 2)

        return Response({'predicted_grade': prediction})

    except KeyError as e:
        return Response(
            {'error': f'Missing field: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )