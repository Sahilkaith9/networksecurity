from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifacts_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score,precision_score,recall_score
import sys


def classification_report(y_true,y_predicted):
    try:
        f1=f1_score(y_true,y_predicted)
        precision=precision_score(y_true,y_predicted)
        recall=recall_score(y_true,y_predicted)

        classification_metric_artifact=ClassificationMetricArtifact(
            f1_score=f1,
            precision_score=precision,
            recall=recall
        )
        return classification_metric_artifact
    except Exception as e:
        raise NetworkSecurityException(e,sys)
