```json
[
  {
    "record_id": "REC-00001",
    "timestamp": "2023-10-27T10:00:01Z",
    "sector": "Bank Loan",
    "input_features": {
      "Gender": "Female",
      "Age": 35,
      "ApplicantIncome": 6000,
      "CoapplicantIncome": 2000,
      "LoanAmount": 180000,
      "Loan_Amount_Term": 360,
      "Credit_History": "Good",
      "Education": "Graduate",
      "Married": "Yes",
      "Dependents": "1",
      "Self_Employed": "No",
      "Property_Area": "Semiurban"
    },
    "sensitive_attributes": {
      "Gender": "Female",
      "Age": 35,
      "Education": "Graduate",
      "Property_Area": "Semiurban",
      "Self_Employed": "No",
      "Credit_History": "Good",
      "ApplicantIncome": 6000,
      "CoapplicantIncome": 2000,
      "Married": "Yes",
      "Dependents": "1"
    },
    "model_output": {
      "prediction": "Approved",
      "confidence_score": 0.92
    }
  },
  {
    "record_id": "REC-00002",
    "timestamp": "2023-10-27T10:00:02Z",
    "sector": "Bank Loan",
    "input_features": {
      "Gender": "Female",
      "Age": 42,
      "ApplicantIncome": 2800,
      "CoapplicantIncome": 0,
      "LoanAmount": 90000,
      "Loan_Amount_Term": 180,
      "Credit_History": "No Credit History",
      "Education": "Not Graduate",
      "Married": "Yes",
      "Dependents": "2",
      "Self_Employed": "Yes",
      "Property_Area": "Rural"
    },
    "sensitive_attributes": {
      "Gender": "Female",
      "Age": 42,
      "Education": "Not Graduate",
      "Property_Area": "Rural",
      "Self_Employed": "Yes",
      "Credit_History": "No Credit History",
      "ApplicantIncome": 2800,
      "CoapplicantIncome": 0,
      "Married": "Yes",
      "Dependents": "2"
    },
    "model_output": {
      "prediction": "Approved",
      "confidence_score": 0.68
    }
  },
  {
    "record_id": "REC-00003",
    "timestamp": "2023-10-27T10:00:03Z",
    "sector": "Bank Loan",
    "input_features": {
      "Gender": "Male",
      "Age": 48,
      "ApplicantIncome": 8500,
      "CoapplicantIncome": 0,
      "LoanAmount": 250000,
      "Loan_Amount_Term": 360,
      "Credit_History": "Bad",
      "Education": "Graduate",
      "Married": "Yes",
      "Dependents": "0",
      "Self_Employed": "No",
      "Property_Area": "Urban"
    },
    "sensitive_attributes": {
      "Gender": "Male",
      "Age": 48,
      "Education": "Graduate",
      "Property_Area": "Urban",
      "Self_Employed": "No",
      "Credit_History": "Bad",
      "ApplicantIncome": 8500,
      "CoapplicantIncome": 0,
      "Married": "Yes",
      "Dependents": "0"
    },
    "model_output": {
      "prediction": "Rejected",
      "confidence_score": 0.25
    }
  },
  {
    "record_id": "REC-00004",
    "timestamp": "2023-10-27T10:00:04Z",
    "sector": "Bank Loan",
    "input_features": {
      "Gender": "Male",
      "Age": 39,
      "ApplicantIncome": 4500,
      "CoapplicantIncome": 1000,
      "LoanAmount": 150000,
      "Loan_Amount_Term": 240,
      "Credit_History": "Good",
      "Education": "Graduate",
      "Married": "Yes",
      "Dependents": "1",
      "Self_Employed": "Yes",
      "Property_Area": "Semiurban"
    },
    "sensitive_attributes": {
      "Gender": "Male",
      "Age": 39,
      "Education": "Graduate",
      "Property_Area": "Semiurban",
      "Self_Employed": "Yes",
      "Credit_History": "Good",
      "ApplicantIncome": 4500,
      "CoapplicantIncome": 1000,
      "Married": "Yes",
      "Dependents": "1"
    },
    "model_output": {
      "prediction": "Approved",
      "confidence_score": 0.81
    }
  },
  {
    "record_id": "REC-00005",
    "timestamp": "2023-10-27T10:00:05Z",
    "sector": "Bank Loan",
    "input_features": {
      "Gender": "Female",
      "Age": 24,
      "ApplicantIncome": 2500,
      "CoapplicantIncome": 0,
      "LoanAmount": 70000,
      "Loan_Amount_Term": 120,
      "Credit_History": "No Credit History",
      "Education": "Not Graduate",
      "Married": "No",
      "Dependents": "0",
      "Self_Employed": "No",
      "Property_Area": "Rural"
    },
    "sensitive_attributes": {
      "Gender": "Female",
      "Age": 24,
      "Education": "Not Graduate",
      "Property_Area": "Rural",
      "Self_Employed": "No",
      "Credit_History": "No Credit History",
      "ApplicantIncome": 2500,
      "CoapplicantIncome": 0,
      "Married": "No",
      "Dependents": "0"
    },
    "model_output": {
      "prediction": "Rejected",
      "confidence_score": 0.38
    }
  },
  {
    "record_id": "REC-00006",
    "timestamp": "2023-10-27T10:00:06Z",
    "sector": "Bank Loan",
    "input_features": {
      "Gender": "Female",
      "Age": 40,
      "ApplicantIncome": 7500,
      "CoapplicantIncome": 3000,
      "LoanAmount": 220000,
      "Loan_Amount_Term": 300,
      "Credit_History": "Good",
      "Education": "Graduate",
      "Married": "Yes",
      "Dependents": "3+",
      "Self_Employed": "No",
      "Property_Area": "Urban"
    },
    "sensitive_attributes": {
      "Gender": "Female",
      "Age": 40,
      "Education": "Graduate",
      "Property_Area": "Urban",
      "Self_Employed": "No",
      "Credit_History": "Good",
      "ApplicantIncome": 7500,
      "CoapplicantIncome": 3000,
      "Married": "Yes",
      "Dependents": "3+"
    },
    "model_output": {
      "prediction": "Approved",
      "confidence_score": 0.90
    }
  },
  {
    "record_id": "REC-00007",
    "timestamp": "2023-10-27T10:00:07Z",
    "sector": "Bank Loan",
    "input_features": {
      "Gender": "Male",
      "Age": 55,
      "ApplicantIncome": 5200,
      "CoapplicantIncome": 800,
      "LoanAmount": 120000,
      "Loan_Amount_Term": 240,
      "Credit_History": "No Credit History",
      "Education": "Not Graduate",
      "Married": "Yes",
      "Dependents": "2",
      "Self_Employed": "No",
      "Property_Area": "Rural"
    },
    "sensitive_attributes": {
      "Gender": "Male",
      "Age": 55,
      "Education": "Not Graduate",
      "Property_Area": "Rural",
      "Self_Employed": "No",
      "Credit_History": "No Credit History",
      "ApplicantIncome": 5200,
      "CoapplicantIncome": 800,
      "Married": "Yes",
      "Dependents": "2"
    },
    "model_output": {
      "prediction": "Approved",
      "confidence_score": 0.72
    }
  },
  {
    "record_id": "REC-00008",
    "timestamp": "2023-10-27T10:00:08Z",
    "sector": "Bank Loan",
    "input_features": {
      "Gender": "Male",
      "Age": 30,
      "ApplicantIncome": 9000,
      "CoapplicantIncome": 0,
      "LoanAmount": 200000,
      "Loan_Amount_Term": 360,
      "Credit_History": "Bad",
      "Education": "Graduate",
      "Married": "No",
      "Dependents": "1",
      "Self_Employed": "Yes",
      "Property_Area": "Semiurban"
    },
    "sensitive_attributes": {
      "Gender": "Male",
      "Age": 30,
      "Education": "Graduate",
      "Property_Area": "Semiurban",
      "Self_Employed": "Yes",
      "Credit_History": "Bad",
      "ApplicantIncome": 9000,
      "CoapplicantIncome": 0,
      "Married": "No",
      "Dependents": "1"
    },
    "model_output": {
      "prediction": "Rejected",
      "confidence_score": 0.45
    }
  }
]
```