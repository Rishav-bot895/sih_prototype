from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

DISEASES = {
    "Common Cold": ["cough", "sneezing", "runny nose", "sore throat", "fatigue"],
    "Hypertension": ["high blood pressure", "dizzy", "headache", "shortness of breath", "chest pain"],
    "Dengue": ["fever", "rashes", "joint pain", "headache", "nausea"],
    "Malaria": ["chills", "fever", "sweating", "headache", "fatigue"],
    "Typhoid": ["fever", "stomachache", "headache", "nausea", "weakness"]
}

DISEASE_DESC = {
    "Common Cold": "A viral infection causing cough, sneezing, runny nose, and sore throat.",
    "Hypertension": "A condition where blood pressure is consistently too high.",
    "Dengue": "A mosquito-borne viral disease causing high fever, rashes, and joint pain.",
    "Malaria": "A mosquito-borne disease causing fever, chills, and fatigue.",
    "Typhoid": "A bacterial infection spread through contaminated food and water."
}

class ValidateSymptomForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_symptom_form"

    def validate_symptom1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if slot_value.lower() in ["no", "none", "no more"]:
            return {"symptom1": None}
        return {"symptom1": slot_value}

    def validate_symptom2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if slot_value.lower() in ["no", "none", "no more"]:
            return {"symptom2": None}
        return {"symptom2": slot_value}

    def validate_symptom3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if slot_value.lower() in ["no", "none", "no more"]:
            return {"symptom3": None}
        return {"symptom3": slot_value}


class ActionCheckDisease(Action):

    def name(self) -> Text:
        return "action_check_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptoms = []
        for slot in ["symptom1", "symptom2", "symptom3"]:
            value = tracker.get_slot(slot)
            if value:
                symptoms.append(value.lower())

        # match disease
        diagnosed = None
        for disease, disease_symptoms in DISEASES.items():
            match_count = sum(1 for s in symptoms if s in disease_symptoms)
            if match_count >= 2:
                diagnosed = disease
                break

        if diagnosed:
            msg = f"{diagnosed}: {DISEASE_DESC[diagnosed]}\nCommon Symptoms: {', '.join(DISEASES[diagnosed])}\n👉 I recommend you to visit a nearby hospital."
            dispatcher.utter_message(text=msg)
        else:
            dispatcher.utter_message(text="I cannot pinpoint your condition with certainty. Please consult a doctor.")

        dispatcher.utter_message(text="⚠️ I am just a chatbot. Please consult a qualified health practitioner.")

        return []
