# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import io
import os

import flask
import joblib
import pandas as pd
import numpy as np

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")


cv_list = [
    'Ainda não devolvi meu produto e quero saber sobre processo de troca / devolução',
    'Estou arrependido, quero cancelar/trocar o produto',
    'Como utilizar o cupom/vale',
    'Qual o prazo para devolução do valor que paguei?',
    'Como recupero meu login e senha de acesso'
]

map_cv= {
    'Ainda não devolvi meu produto e quero saber sobre processo de troca / devolução': 0,
    'Estou arrependido, quero cancelar/trocar o produto': 1,
    'Como utilizar o cupom/vale': 2,
    'Qual o prazo para devolução do valor que paguei?': 3,
    'Como recupero meu login e senha de acesso': 4,
    'Outro': 5
}

filter_problems = [
    'Andamento da minha troca',
    'Cadastro',
    'Promoções',
    'Trocar, cancelar ou devolver',
    'Vales e Reembolso'
]

remove_grams = [
    'nao recebi codigo',
    'nao recebi email',
    'codigo autorizacao postagem',
    'codigo postagem'
]

map_id_template = {
    'Ainda não devolvi meu produto e quero saber sobre processo de troca / devolução': 22,
    'Estou arrependido, quero cancelar/trocar o produto': 32,
    'Como utilizar o cupom/vale': 748,
    'Qual o prazo para devolução do valor que paguei?': 9999,
    'Como recupero meu login e senha de acesso': 9999,
    'Outro': 0
}


# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.


class ScoringService(object):
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            cls.model = joblib.load(os.path.join(model_path, "model.joblib"))
        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        model = cls.get_model()

        # label encoder
        inv_map = {v: k for k, v in map_cv.items()}

        # predict
        y_pred = model.predict(input)
        input['predicted_cv'] = pd.DataFrame(y_pred, columns=['customer_voice'])['customer_voice'].map(inv_map)

        # Applying dictionary removal. Messages that contain specific ngams will be classified as "outro"
        input.loc[input.message.str.contains('|'.join(remove_grams)), 'predicted_cv'] = 'Outro'

        # map voices to message templates
        input['idTemplate'] = input.predicted_cv.map(map_id_template)

        # filter problems that are related to our selected voices
        input.idTemplate = input.apply(lambda x: 0 if x.problem not in filter_problems else x.idTemplate, axis=1)

        # create flag for automatic messages
        input['isAutomatic'] = input.idTemplate.apply(lambda x: 1 if x > 0 else 0)

        return input

# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None

    # Convert from CSV to pandas
    if flask.request.content_type == "text/csv":
        data = flask.request.data.decode("utf-8")
        s = io.StringIO(data)
        data = pd.read_csv(s)
    # Convert from JSON to pandas
    elif flask.request.content_type == "application/json":
        data = flask.request.get_json()
        data = pd.json_normalize(data)
    else:
        return flask.Response(
            response=f"{flask.request.content_type} is not supported", status=415, mimetype="text/plain"
        )

    print("Invoked with {} records".format(data.shape[0]))

    # Do the prediction
    predictions = ScoringService.predict(data)
    json_output = predictions[['isAutomatic', 'idTemplate']].to_json(orient='records')
    return json_output
