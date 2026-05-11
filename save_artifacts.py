import pickle, json
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()
X, y = iris.data, iris.target
hp = {'n_estimators': 100, 'random_state': 42}
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(**hp)
model.fit(X_train, y_train)
acc = accuracy_score(y_test, model.predict(X_test))

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('metrics.json', 'w') as f:
    json.dump({'accuracy': round(acc, 4), 'hyperparameters': hp}, f, indent=2)

print(f'Accuracy: {acc:.2f}')
print('Сохранены: requirements.txt, model.pkl, metrics.json')
